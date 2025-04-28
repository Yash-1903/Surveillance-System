"""
Enterprise incident management and response system
"""
from typing import Dict, List, Any
from datetime import datetime
import json
from dataclasses import dataclass
from enum import Enum

class IncidentPriority(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class IncidentStatus(Enum):
    NEW = "NEW"
    INVESTIGATING = "INVESTIGATING"
    RESPONDING = "RESPONDING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

@dataclass
class IncidentResponse:
    action_taken: str
    timestamp: datetime
    responder: str
    outcome: str
    notes: str = ""

class IncidentManager:
    def __init__(self):
        self.active_incidents = {}
        self.incident_history = []
        self.response_templates = self._load_response_templates()
        
    def create_incident(self, detection_data: Dict[str, Any], 
                       threat_assessment: Dict[str, Any]) -> str:
        """Create new security incident"""
        incident_id = self._generate_incident_id()
        
        incident = {
            'id': incident_id,
            'timestamp': datetime.now(),
            'type': detection_data.get('type', 'UNKNOWN'),
            'priority': self._determine_priority(detection_data, threat_assessment),
            'status': IncidentStatus.NEW,
            'location': detection_data.get('location', None),
            'detection_data': detection_data,
            'threat_assessment': threat_assessment,
            'responses': [],
            'resolution': None
        }
        
        self.active_incidents[incident_id] = incident
        return incident_id
    
    def update_incident(self, incident_id: str, 
                       status: IncidentStatus = None,
                       response: IncidentResponse = None) -> bool:
        """Update incident status and add response"""
        if incident_id not in self.active_incidents:
            return False
            
        incident = self.active_incidents[incident_id]
        
        if status:
            incident['status'] = status
            
        if response:
            incident['responses'].append({
                'action': response.action_taken,
                'timestamp': response.timestamp,
                'responder': response.responder,
                'outcome': response.outcome,
                'notes': response.notes
            })
        
        return True
    
    def resolve_incident(self, incident_id: str, resolution: Dict[str, Any]) -> bool:
        """Resolve and archive incident"""
        if incident_id not in self.active_incidents:
            return False
            
        incident = self.active_incidents[incident_id]
        incident['status'] = IncidentStatus.RESOLVED
        incident['resolution'] = {
            'timestamp': datetime.now(),
            'details': resolution
        }
        
        # Archive incident
        self.incident_history.append(incident)
        del self.active_incidents[incident_id]
        
        return True
    
    def get_response_plan(self, incident_id: str) -> List[Dict[str, Any]]:
        """Generate response plan for incident"""
        if incident_id not in self.active_incidents:
            return []
            
        incident = self.active_incidents[incident_id]
        incident_type = incident['type']
        threat_level = incident['threat_assessment'].get('threat_level', 0)
        
        # Get relevant response template
        template = self.response_templates.get(incident_type, [])
        
        # Customize response based on threat level
        response_plan = []
        for step in template:
            if step['min_threat_level'] <= threat_level:
                response_plan.append({
                    'action': step['action'],
                    'priority': step['priority'],
                    'responders': step['responders'],
                    'instructions': step['instructions']
                })
        
        return response_plan
    
    def get_incident_statistics(self) -> Dict[str, Any]:
        """Generate incident statistics"""
        all_incidents = self.incident_history + list(self.active_incidents.values())
        
        stats = {
            'total_incidents': len(all_incidents),
            'active_incidents': len(self.active_incidents),
            'resolved_incidents': len(self.incident_history),
            'by_priority': {
                'CRITICAL': 0,
                'HIGH': 0,
                'MEDIUM': 0,
                'LOW': 0
            },
            'by_type': {},
            'average_resolution_time': self._calculate_avg_resolution_time(),
            'response_effectiveness': self._analyze_response_effectiveness()
        }
        
        # Calculate distributions
        for incident in all_incidents:
            stats['by_priority'][incident['priority'].value] += 1
            incident_type = incident['type']
            stats['by_type'][incident_type] = stats['by_type'].get(incident_type, 0) + 1
        
        return stats
    
    def _generate_incident_id(self) -> str:
        """Generate unique incident ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        count = len(self.active_incidents) + len(self.incident_history)
        return f"INC-{timestamp}-{count:04d}"
    
    def _determine_priority(self, detection_data: Dict[str, Any], 
                          threat_assessment: Dict[str, Any]) -> IncidentPriority:
        """Determine incident priority"""
        threat_level = threat_assessment.get('threat_level', 0)
        
        if threat_level > 0.8:
            return IncidentPriority.CRITICAL
        elif threat_level > 0.6:
            return IncidentPriority.HIGH
        elif threat_level > 0.4:
            return IncidentPriority.MEDIUM
        else:
            return IncidentPriority.LOW
    
    def _load_response_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load incident response templates"""
        return {
            'weapon': [
                {
                    'action': 'Immediate lockdown',
                    'priority': 'CRITICAL',
                    'min_threat_level': 0.8,
                    'responders': ['security', 'law_enforcement'],
                    'instructions': 'Initiate facility lockdown and contact law enforcement'
                },
                {
                    'action': 'Evacuate area',
                    'priority': 'HIGH',
                    'min_threat_level': 0.6,
                    'responders': ['security'],
                    'instructions': 'Clear immediate area and establish security perimeter'
                }
            ],
            'fire': [
                {
                    'action': 'Fire response',
                    'priority': 'CRITICAL',
                    'min_threat_level': 0.7,
                    'responders': ['fire_department', 'security'],
                    'instructions': 'Activate fire alarm and contact fire department'
                },
                {
                    'action': 'Evacuation',
                    'priority': 'HIGH',
                    'min_threat_level': 0.5,
                    'responders': ['security'],
                    'instructions': 'Begin evacuation procedures'
                }
            ],
            'accident': [
                {
                    'action': 'Emergency response',
                    'priority': 'HIGH',
                    'min_threat_level': 0.6,
                    'responders': ['medical', 'security'],
                    'instructions': 'Contact emergency services and secure area'
                }
            ]
        }
    
    def _calculate_avg_resolution_time(self) -> float:
        """Calculate average incident resolution time"""
        if not self.incident_history:
            return 0
            
        total_time = 0
        count = 0
        
        for incident in self.incident_history:
            if incident.get('resolution'):
                start_time = incident['timestamp']
                end_time = incident['resolution']['timestamp']
                duration = (end_time - start_time).total_seconds() / 3600  # hours
                total_time += duration
                count += 1
        
        return total_time / count if count > 0 else 0
    
    def _analyze_response_effectiveness(self) -> Dict[str, float]:
        """Analyze effectiveness of incident responses"""
        effectiveness = {
            'response_time': 0,
            'resolution_rate': 0,
            'escalation_rate': 0
        }
        
        if not self.incident_history:
            return effectiveness
            
        total_incidents = len(self.incident_history)
        response_times = []
        escalations = 0
        
        for incident in self.incident_history:
            # Calculate response time
            if incident['responses']:
                first_response = incident['responses'][0]['timestamp']
                response_time = (first_response - incident['timestamp']).total_seconds() / 60
                response_times.append(response_time)
            
            # Check for escalations
            responses = incident['responses']
            initial_priority = responses[0]['priority'] if responses else None
            final_priority = responses[-1]['priority'] if responses else None
            
            if initial_priority and final_priority and \
               IncidentPriority[final_priority].value > IncidentPriority[initial_priority].value:
                escalations += 1
        
        # Calculate metrics
        effectiveness['response_time'] = sum(response_times) / len(response_times) if response_times else 0
        effectiveness['resolution_rate'] = len([i for i in self.incident_history if i['status'] == IncidentStatus.RESOLVED]) / total_incidents
        effectiveness['escalation_rate'] = escalations / total_incidents
        
        return effectiveness