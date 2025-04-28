"""
Advanced reporting and visualization module
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Dict, List, Any
import seaborn as sns
import io
import base64

class ReportGenerator:
    def __init__(self):
        self.style_config = {
            'figure.figsize': (12, 8),
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10
        }
        plt.style.use('seaborn')
        for key, value in self.style_config.items():
            plt.rcParams[key] = value
    
    def generate_report(self, analytics_data: Dict[str, Any], 
                       threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        report = {
            'summary': self._generate_summary(analytics_data, threat_data),
            'threat_analysis': self._analyze_threats(threat_data),
            'activity_analysis': self._analyze_activity(analytics_data),
            'visualizations': self._generate_visualizations(analytics_data, threat_data),
            'recommendations': self._compile_recommendations(analytics_data, threat_data)
        }
        
        return report
    
    def _generate_summary(self, analytics_data: Dict[str, Any], 
                         threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary"""
        return {
            'period': {
                'start': analytics_data['period']['start'],
                'end': analytics_data['period']['end']
            },
            'total_events': analytics_data['summary']['total_events'],
            'high_severity_events': analytics_data['summary']['high_severity_events'],
            'current_threat_level': threat_data.get('threat_level', 0),
            'active_threats': len(threat_data.get('immediate_threats', [])),
            'key_findings': self._identify_key_findings(analytics_data, threat_data)
        }
    
    def _analyze_threats(self, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze threat patterns and trends"""
        immediate_threats = threat_data.get('immediate_threats', [])
        potential_threats = threat_data.get('potential_threats', [])
        
        return {
            'current_threats': {
                'count': len(immediate_threats),
                'high_priority': len([t for t in immediate_threats if t['priority'] == 'HIGH']),
                'details': immediate_threats
            },
            'potential_threats': {
                'count': len(potential_threats),
                'likelihood_summary': {
                    'high': len([t for t in potential_threats if t['likelihood'] > 0.7]),
                    'medium': len([t for t in potential_threats if 0.4 <= t['likelihood'] <= 0.7]),
                    'low': len([t for t in potential_threats if t['likelihood'] < 0.4])
                },
                'details': potential_threats
            },
            'threat_patterns': self._analyze_threat_patterns(threat_data)
        }
    
    def _analyze_activity(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze activity patterns and trends"""
        return {
            'hourly_distribution': analytics_data.get('trends', {}).get('peak_hours', {}),
            'event_correlations': analytics_data.get('trends', {}).get('event_correlations', []),
            'hotspots': self._analyze_hotspots(analytics_data.get('hotspots', []))
        }
    
    def _generate_visualizations(self, analytics_data: Dict[str, Any], 
                               threat_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate data visualizations"""
        visualizations = {}
        
        # Threat Level Timeline
        fig, ax = plt.subplots()
        threat_timeline = pd.Series(analytics_data.get('trends', {}).get('severity_trend', {}))
        threat_timeline.plot(ax=ax)
        ax.set_title('Threat Level Timeline')
        ax.set_xlabel('Date')
        ax.set_ylabel('Threat Level')
        visualizations['threat_timeline'] = self._fig_to_base64(fig)
        plt.close(fig)
        
        # Event Distribution
        fig, ax = plt.subplots()
        event_types = analytics_data.get('summary', {}).get('event_types', {})
        if event_types:
            pd.Series(event_types).plot(kind='bar', ax=ax)
            ax.set_title('Event Type Distribution')
            ax.set_xlabel('Event Type')
            ax.set_ylabel('Count')
            plt.xticks(rotation=45)
            visualizations['event_distribution'] = self._fig_to_base64(fig)
        plt.close(fig)
        
        # Hotspot Map
        fig, ax = plt.subplots()
        hotspots = analytics_data.get('hotspots', [])
        if hotspots:
            x = [h['location'][0] for h in hotspots]
            y = [h['location'][1] for h in hotspots]
            sizes = [h['event_count'] * 100 for h in hotspots]
            colors = [h['avg_severity'] for h in hotspots]
            
            scatter = ax.scatter(x, y, s=sizes, c=colors, cmap='YlOrRd', alpha=0.6)
            plt.colorbar(scatter, label='Average Severity')
            ax.set_title('Security Hotspot Map')
            ax.set_xlabel('X Coordinate')
            ax.set_ylabel('Y Coordinate')
            visualizations['hotspot_map'] = self._fig_to_base64(fig)
        plt.close(fig)
        
        return visualizations
    
    def _compile_recommendations(self, analytics_data: Dict[str, Any], 
                               threat_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Compile and prioritize recommendations"""
        recommendations = []
        
        # Add threat-based recommendations
        threat_recs = threat_data.get('recommendations', [])
        recommendations.extend(threat_recs)
        
        # Add analytics-based recommendations
        analytics_recs = analytics_data.get('recommendations', [])
        recommendations.extend(analytics_recs)
        
        # Prioritize and deduplicate
        unique_recs = {}
        for rec in recommendations:
            key = f"{rec['priority']}_{rec['action']}"
            if key not in unique_recs or rec['priority'] == 'HIGH':
                unique_recs[key] = rec
        
        # Sort by priority
        priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        sorted_recs = sorted(unique_recs.values(), 
                           key=lambda x: priority_order.get(x['priority'], 3))
        
        return sorted_recs
    
    def _identify_key_findings(self, analytics_data: Dict[str, Any], 
                             threat_data: Dict[str, Any]) -> List[str]:
        """Identify key findings from the data"""
        findings = []
        
        # Threat-related findings
        if threat_data.get('threat_level', 0) > 0.7:
            findings.append("HIGH threat level detected")
        
        immediate_threats = threat_data.get('immediate_threats', [])
        if immediate_threats:
            findings.append(f"{len(immediate_threats)} active threats identified")
        
        # Analytics-related findings
        summary = analytics_data.get('summary', {})
        if summary.get('high_severity_events', 0) > 0:
            findings.append(f"{summary['high_severity_events']} high-severity events recorded")
        
        hotspots = analytics_data.get('hotspots', [])
        if hotspots:
            findings.append(f"{len(hotspots)} security hotspots identified")
        
        return findings
    
    def _analyze_threat_patterns(self, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns in threat data"""
        patterns = {
            'recurring': [],
            'escalating': [],
            'correlated': []
        }
        
        # Analyze immediate threats
        immediate_threats = threat_data.get('immediate_threats', [])
        threat_types = [t['type'] for t in immediate_threats]
        
        # Find recurring threats
        from collections import Counter
        type_counts = Counter(threat_types)
        patterns['recurring'] = [
            {'type': t, 'count': c}
            for t, c in type_counts.items()
            if c > 1
        ]
        
        # Identify escalating threats
        for threat in immediate_threats:
            if threat['level'] > 0.8:
                patterns['escalating'].append(threat['type'])
        
        # Find correlated threats
        if len(immediate_threats) > 1:
            patterns['correlated'] = [
                (t1['type'], t2['type'])
                for i, t1 in enumerate(immediate_threats)
                for t2 in immediate_threats[i+1:]
                if abs(t1['level'] - t2['level']) < 0.2
            ]
        
        return patterns
    
    def _analyze_hotspots(self, hotspots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze security hotspots"""
        if not hotspots:
            return {}
        
        return {
            'total_hotspots': len(hotspots),
            'high_risk_zones': len([h for h in hotspots if h['avg_severity'] > 0.7]),
            'most_active': {
                'location': hotspots[0]['location'],
                'event_count': hotspots[0]['event_count'],
                'event_types': hotspots[0]['event_types']
            },
            'risk_distribution': {
                'high': len([h for h in hotspots if h['avg_severity'] > 0.7]),
                'medium': len([h for h in hotspots if 0.4 <= h['avg_severity'] <= 0.7]),
                'low': len([h for h in hotspots if h['avg_severity'] < 0.4])
            }
        }
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode('utf-8')