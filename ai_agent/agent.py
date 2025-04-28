"""
Advanced AI Agent for Smart Surveillance System
"""
from typing import Dict, List, Any
import numpy as np
import cv2
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DetectionEvent:
    type: str
    confidence: float
    timestamp: datetime
    location: tuple  # (x, y, width, height)
    metadata: Dict[str, Any]

class SurveillanceAgent:
    def __init__(self):
        self.detection_history: List[DetectionEvent] = []
        self.threat_level = 0.0
        self.active_threats: Dict[str, List[DetectionEvent]] = {}
        
    def analyze_frame(self, frame, detections: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze frame and detections to make intelligent decisions"""
        analysis_result = {
            'threat_level': 0.0,
            'recommendations': [],
            'priority_areas': [],
            'required_actions': []
        }
        
        try:
            # Process all detections
            for det_type, det_data in detections.items():
                if det_data:
                    event = self._create_detection_event(det_type, det_data)
                    self.detection_history.append(event)
                    self._update_threat_analysis(event, analysis_result)
            
            # Analyze patterns and update recommendations
            self._analyze_patterns(analysis_result)
            
            # Clean up old history
            self._cleanup_history()
            
            return analysis_result
            
        except Exception as e:
            print(f"Error in AI analysis: {str(e)}")
            return analysis_result
    
    def _create_detection_event(self, det_type: str, det_data: Any) -> DetectionEvent:
        """Create a detection event from raw detection data"""
        if isinstance(det_data, list):
            # Multiple detections of same type
            confidence = max(d.get('score', 0.0) for d in det_data)
            location = det_data[0].get('box', (0, 0, 0, 0))
        else:
            confidence = det_data.get('score', 0.0)
            location = det_data.get('box', (0, 0, 0, 0))
        
        return DetectionEvent(
            type=det_type,
            confidence=confidence,
            timestamp=datetime.now(),
            location=location,
            metadata=det_data
        )
    
    def _update_threat_analysis(self, event: DetectionEvent, result: Dict[str, Any]):
        """Update threat analysis based on new detection"""
        # Threat level weights for different detection types
        threat_weights = {
            'weapon': 0.9,
            'fire': 0.8,
            'accident': 0.7,
            'crowd': 0.5,
            'motion': 0.2
        }
        
        # Update threat level
        weight = threat_weights.get(event.type, 0.3)
        threat_contribution = weight * event.confidence
        result['threat_level'] = max(result['threat_level'], threat_contribution)
        
        # Add recommendations based on detection type
        if event.type == 'weapon':
            result['recommendations'].append({
                'priority': 'HIGH',
                'action': 'Alert security personnel immediately',
                'details': f'Weapon detected with {event.confidence:.2f} confidence'
            })
        elif event.type == 'fire':
            result['recommendations'].append({
                'priority': 'HIGH',
                'action': 'Activate fire response protocol',
                'details': 'Fire detected - evacuate area'
            })
        elif event.type == 'crowd' and event.metadata.get('count', 0) > 20:
            result['recommendations'].append({
                'priority': 'MEDIUM',
                'action': 'Monitor crowd density',
                'details': f'Large crowd of {event.metadata["count"]} people detected'
            })
    
    def _analyze_patterns(self, result: Dict[str, Any]):
        """Analyze detection patterns for advanced insights"""
        recent_events = [e for e in self.detection_history 
                        if (datetime.now() - e.timestamp).seconds < 300]
        
        # Analyze event frequency
        event_counts = {}
        for event in recent_events:
            event_counts[event.type] = event_counts.get(event.type, 0) + 1
        
        # Check for suspicious patterns
        if event_counts.get('motion', 0) > 10 and event_counts.get('crowd', 0) > 5:
            result['recommendations'].append({
                'priority': 'MEDIUM',
                'action': 'Investigate unusual activity',
                'details': 'High frequency of motion and crowd detections'
            })
        
        # Identify priority monitoring areas
        if recent_events:
            locations = np.array([event.location for event in recent_events])
            if len(locations) > 0:
                center_x = np.mean(locations[:, 0])
                center_y = np.mean(locations[:, 1])
                result['priority_areas'].append({
                    'center': (int(center_x), int(center_y)),
                    'radius': 100,
                    'reason': 'High activity area'
                })
    
    def _cleanup_history(self):
        """Clean up old detection history"""
        current_time = datetime.now()
        self.detection_history = [
            event for event in self.detection_history
            if (current_time - event.timestamp).seconds < 3600  # Keep last hour
        ]
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate a comprehensive status report"""
        return {
            'current_threat_level': self.threat_level,
            'active_threats': self.active_threats,
            'detection_summary': self._generate_detection_summary(),
            'system_recommendations': self._generate_recommendations()
        }
    
    def _generate_detection_summary(self) -> Dict[str, int]:
        """Generate summary of recent detections"""
        summary = {}
        recent_events = [e for e in self.detection_history 
                        if (datetime.now() - e.timestamp).seconds < 3600]
        
        for event in recent_events:
            summary[event.type] = summary.get(event.type, 0) + 1
        
        return summary
    
    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate system recommendations based on analysis"""
        recommendations = []
        
        # Analyze detection patterns
        if len(self.detection_history) > 100:
            recommendations.append({
                'type': 'system',
                'message': 'Consider increasing processing capacity'
            })
        
        # Check for recurring detections
        detection_summary = self._generate_detection_summary()
        for det_type, count in detection_summary.items():
            if count > 20:
                recommendations.append({
                    'type': 'security',
                    'message': f'High frequency of {det_type} detections - investigate area'
                })
        
        return recommendations