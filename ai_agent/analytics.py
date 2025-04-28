"""
Advanced analytics module for surveillance system
"""
from typing import Dict, List, Any
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from dataclasses import dataclass

@dataclass
class AnalyticsEvent:
    event_type: str
    timestamp: datetime
    severity: float
    location: tuple
    metadata: Dict[str, Any]

class AdvancedAnalytics:
    def __init__(self):
        self.events_history = []
        self.daily_stats = {}
        self.zone_analytics = {}
        
    def process_event(self, event: AnalyticsEvent):
        """Process and analyze new events"""
        self.events_history.append(event)
        self._update_daily_stats(event)
        self._update_zone_analytics(event)
        
    def _update_daily_stats(self, event: AnalyticsEvent):
        """Update daily statistics"""
        date_key = event.timestamp.date()
        if date_key not in self.daily_stats:
            self.daily_stats[date_key] = {
                'total_events': 0,
                'events_by_type': {},
                'severity_sum': 0,
                'high_severity_events': 0
            }
        
        stats = self.daily_stats[date_key]
        stats['total_events'] += 1
        stats['events_by_type'][event.event_type] = \
            stats['events_by_type'].get(event.event_type, 0) + 1
        stats['severity_sum'] += event.severity
        
        if event.severity > 0.7:
            stats['high_severity_events'] += 1
    
    def _update_zone_analytics(self, event: AnalyticsEvent):
        """Update zone-based analytics"""
        x, y = event.location[0], event.location[1]
        zone_key = f"zone_{x//100}_{y//100}"
        
        if zone_key not in self.zone_analytics:
            self.zone_analytics[zone_key] = {
                'event_count': 0,
                'event_types': set(),
                'avg_severity': 0,
                'last_event': None
            }
        
        zone = self.zone_analytics[zone_key]
        zone['event_count'] += 1
        zone['event_types'].add(event.event_type)
        zone['avg_severity'] = ((zone['avg_severity'] * (zone['event_count'] - 1) + 
                               event.severity) / zone['event_count'])
        zone['last_event'] = event.timestamp
    
    def generate_report(self, days: int = 7) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        report = {
            'period': {
                'start': start_date,
                'end': end_date
            },
            'summary': self._generate_summary(start_date, end_date),
            'trends': self._analyze_trends(start_date, end_date),
            'hotspots': self._identify_hotspots(),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_summary(self, start_date, end_date) -> Dict[str, Any]:
        """Generate summary statistics"""
        relevant_events = [
            e for e in self.events_history 
            if start_date <= e.timestamp <= end_date
        ]
        
        if not relevant_events:
            return {'total_events': 0}
        
        event_types = {}
        total_severity = 0
        high_severity_count = 0
        
        for event in relevant_events:
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
            total_severity += event.severity
            if event.severity > 0.7:
                high_severity_count += 1
        
        return {
            'total_events': len(relevant_events),
            'event_types': event_types,
            'avg_severity': total_severity / len(relevant_events),
            'high_severity_events': high_severity_count
        }
    
    def _analyze_trends(self, start_date, end_date) -> Dict[str, Any]:
        """Analyze event trends over time"""
        events_df = pd.DataFrame([
            {
                'timestamp': e.timestamp,
                'type': e.event_type,
                'severity': e.severity
            }
            for e in self.events_history
            if start_date <= e.timestamp <= end_date
        ])
        
        if events_df.empty:
            return {}
        
        # Daily trends
        daily_counts = events_df.resample('D', on='timestamp').size()
        severity_trend = events_df.resample('D', on='timestamp')['severity'].mean()
        
        return {
            'daily_event_counts': daily_counts.to_dict(),
            'severity_trend': severity_trend.to_dict(),
            'peak_hours': self._identify_peak_hours(events_df),
            'event_correlations': self._analyze_correlations(events_df)
        }
    
    def _identify_peak_hours(self, events_df) -> Dict[int, int]:
        """Identify hours with highest activity"""
        if events_df.empty:
            return {}
            
        hourly_counts = events_df['timestamp'].dt.hour.value_counts()
        return hourly_counts.nlargest(5).to_dict()
    
    def _analyze_correlations(self, events_df) -> List[Dict[str, Any]]:
        """Analyze correlations between different event types"""
        if events_df.empty:
            return []
            
        correlations = []
        event_types = events_df['type'].unique()
        
        for type1 in event_types:
            for type2 in event_types:
                if type1 < type2:
                    type1_times = events_df[events_df['type'] == type1]['timestamp']
                    type2_times = events_df[events_df['type'] == type2]['timestamp']
                    
                    # Check for events occurring within 5 minutes of each other
                    correlated_events = 0
                    for t1 in type1_times:
                        if any(abs((t2 - t1).total_seconds()) <= 300 for t2 in type2_times):
                            correlated_events += 1
                    
                    if correlated_events > 0:
                        correlations.append({
                            'types': (type1, type2),
                            'correlation_count': correlated_events
                        })
        
        return correlations
    
    def _identify_hotspots(self) -> List[Dict[str, Any]]:
        """Identify high-activity zones"""
        hotspots = []
        
        for zone_key, zone_data in self.zone_analytics.items():
            if zone_data['event_count'] > 10 or zone_data['avg_severity'] > 0.6:
                x, y = map(lambda x: int(x) * 100, zone_key.split('_')[1:])
                hotspots.append({
                    'location': (x, y),
                    'event_count': zone_data['event_count'],
                    'event_types': list(zone_data['event_types']),
                    'avg_severity': zone_data['avg_severity'],
                    'last_activity': zone_data['last_event']
                })
        
        return sorted(hotspots, key=lambda x: x['event_count'], reverse=True)
    
    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate intelligent recommendations based on analytics"""
        recommendations = []
        
        # Analyze high-activity zones
        hotspots = self._identify_hotspots()
        if hotspots:
            recommendations.append({
                'type': 'security',
                'priority': 'HIGH',
                'message': f'Increase monitoring in {len(hotspots)} identified hotspots'
            })
        
        # Check for patterns in recent events
        recent_events = [e for e in self.events_history 
                        if (datetime.now() - e.timestamp).days < 7]
        
        event_types = {}
        for event in recent_events:
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
        
        for event_type, count in event_types.items():
            if count > 20:
                recommendations.append({
                    'type': 'operations',
                    'priority': 'MEDIUM',
                    'message': f'High frequency of {event_type} events - review prevention measures'
                })
        
        return recommendations