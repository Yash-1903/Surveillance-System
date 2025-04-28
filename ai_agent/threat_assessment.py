"""
Advanced threat assessment and prediction module
"""
from typing import Dict, List, Any
import numpy as np
from datetime import datetime
from sklearn.ensemble import IsolationForest

class ThreatAssessment:
    def __init__(self):
        self.threat_history = []
        self.anomaly_detector = IsolationForest(contamination=0.1)
        self.threat_patterns = {}
        
    def assess_threat(self, detections: Dict[str, Any], 
                     analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive threat assessment"""
        threat_data = self._process_detections(detections)
        threat_data.update(self._analyze_patterns(analytics_data))
        
        # Store for historical analysis
        self.threat_history.append({
            'timestamp': datetime.now(),
            'data': threat_data
        })
        
        # Detect anomalies
        anomalies = self._detect_anomalies(threat_data)
        
        # Generate threat assessment
        assessment = {
            'threat_level': self._calculate_threat_level(threat_data, anomalies),
            'immediate_threats': self._identify_immediate_threats(threat_data),
            'potential_threats': self._predict_potential_threats(threat_data),
            'anomalies': anomalies,
            'recommendations': self._generate_recommendations(threat_data, anomalies)
        }
        
        return assessment
    
    def _process_detections(self, detections: Dict[str, Any]) -> Dict[str, float]:
        """Process current detections"""
        threat_scores = {
            'weapon': 0.9,
            'fire': 0.8,
            'accident': 0.7,
            'crowd': 0.5,
            'motion': 0.2
        }
        
        processed_data = {}
        for det_type, det_info in detections.items():
            if isinstance(det_info, list):
                # Multiple detections
                confidence = max(d.get('score', 0) for d in det_info)
            else:
                confidence = det_info.get('score', 0)
            
            processed_data[det_type] = confidence * threat_scores.get(det_type, 0.3)
        
        return processed_data
    
    def _analyze_patterns(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze threat patterns"""
        patterns = {
            'recurring_threats': [],
            'escalating_threats': [],
            'combined_threats': []
        }
        
        # Analyze recent history
        recent_history = self.threat_history[-100:] if len(self.threat_history) > 100 else self.threat_history
        
        if recent_history:
            # Check for recurring threats
            threat_counts = {}
            for entry in recent_history:
                for threat_type, level in entry['data'].items():
                    if level > 0.5:  # Significant threats only
                        threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
            
            # Identify recurring threats
            for threat_type, count in threat_counts.items():
                if count > 5:  # More than 5 occurrences
                    patterns['recurring_threats'].append({
                        'type': threat_type,
                        'count': count
                    })
            
            # Check for escalating threats
            for threat_type in set().union(*(entry['data'].keys() for entry in recent_history)):
                levels = [entry['data'].get(threat_type, 0) for entry in recent_history]
                if len(levels) > 5 and all(a <= b for a, b in zip(levels[-5:], levels[-4:])):
                    patterns['escalating_threats'].append(threat_type)
            
            # Analyze combined threats
            current_threats = set(k for k, v in analytics_data.items() if v > 0.5)
            if len(current_threats) > 1:
                patterns['combined_threats'] = list(current_threats)
        
        return patterns
    
    def _detect_anomalies(self, threat_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect anomalous threat patterns"""
        if len(self.threat_history) < 10:
            return []
        
        # Prepare data for anomaly detection
        recent_data = np.array([
            list(entry['data'].values()) 
            for entry in self.threat_history[-100:]
        ])
        
        # Fit and predict
        self.anomaly_detector.fit(recent_data)
        current_data = np.array(list(threat_data.values())).reshape(1, -1)
        prediction = self.anomaly_detector.predict(current_data)
        
        anomalies = []
        if prediction[0] == -1:  # Anomaly detected
            # Analyze which aspects are anomalous
            for threat_type, value in threat_data.items():
                historical_values = [
                    entry['data'].get(threat_type, 0) 
                    for entry in self.threat_history[-100:]
                ]
                if value > np.mean(historical_values) + 2 * np.std(historical_values):
                    anomalies.append({
                        'type': threat_type,
                        'value': value,
                        'normal_range': {
                            'mean': np.mean(historical_values),
                            'std': np.std(historical_values)
                        }
                    })
        
        return anomalies
    
    def _calculate_threat_level(self, threat_data: Dict[str, Any], 
                              anomalies: List[Dict[str, Any]]) -> float:
        """Calculate overall threat level"""
        base_threat = max(threat_data.values(), default=0)
        
        # Adjust for anomalies
        anomaly_factor = len(anomalies) * 0.1
        
        # Adjust for patterns
        pattern_factor = 0
        if threat_data.get('recurring_threats'):
            pattern_factor += 0.1
        if threat_data.get('escalating_threats'):
            pattern_factor += 0.2
        if threat_data.get('combined_threats'):
            pattern_factor += 0.15
        
        return min(1.0, base_threat + anomaly_factor + pattern_factor)
    
    def _identify_immediate_threats(self, threat_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify immediate threats requiring attention"""
        immediate_threats = []
        
        for threat_type, level in threat_data.items():
            if level > 0.7:  # High threat level
                immediate_threats.append({
                    'type': threat_type,
                    'level': level,
                    'priority': 'HIGH',
                    'required_action': self._get_required_action(threat_type, level)
                })
            elif level > 0.4:  # Medium threat level
                immediate_threats.append({
                    'type': threat_type,
                    'level': level,
                    'priority': 'MEDIUM',
                    'required_action': self._get_required_action(threat_type, level)
                })
        
        return immediate_threats
    
    def _predict_potential_threats(self, threat_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict potential future threats"""
        predictions = []
        
        # Analyze patterns for prediction
        if len(self.threat_history) > 10:
            for threat_type in threat_data.keys():
                historical_values = [
                    entry['data'].get(threat_type, 0) 
                    for entry in self.threat_history[-10:]
                ]
                
                # Simple trend analysis
                trend = np.polyfit(range(len(historical_values)), historical_values, 1)[0]
                
                if trend > 0.1:  # Increasing trend
                    predictions.append({
                        'type': threat_type,
                        'likelihood': min(1.0, trend * 5),
                        'timeframe': 'next 30 minutes',
                        'basis': 'Increasing trend in activity'
                    })
        
        return predictions
    
    def _get_required_action(self, threat_type: str, level: float) -> str:
        """Get required action based on threat type and level"""
        actions = {
            'weapon': 'Alert security and law enforcement immediately',
            'fire': 'Activate emergency protocols and contact fire department',
            'accident': 'Alert emergency services and secure the area',
            'crowd': 'Monitor crowd movement and ensure adequate security',
            'motion': 'Investigate suspicious activity'
        }
        
        return actions.get(threat_type, 'Investigate and assess situation')
    
    def _generate_recommendations(self, threat_data: Dict[str, Any], 
                                anomalies: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate intelligent recommendations"""
        recommendations = []
        
        # Handle immediate threats
        immediate_threats = self._identify_immediate_threats(threat_data)
        for threat in immediate_threats:
            recommendations.append({
                'priority': threat['priority'],
                'action': threat['required_action'],
                'details': f"Threat Level: {threat['level']:.2f}"
            })
        
        # Handle anomalies
        for anomaly in anomalies:
            recommendations.append({
                'priority': 'HIGH',
                'action': f"Investigate anomalous {anomaly['type']} activity",
                'details': f"Value: {anomaly['value']:.2f}, Expected: {anomaly['normal_range']['mean']:.2f}"
            })
        
        # Add predictive recommendations
        potential_threats = self._predict_potential_threats(threat_data)
        for threat in potential_threats:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': f"Prepare for potential {threat['type']} incident",
                'details': f"Likelihood: {threat['likelihood']:.2f}, Timeframe: {threat['timeframe']}"
            })
        
        return recommendations