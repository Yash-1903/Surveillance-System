"""
Resource optimization and deployment manager
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass
from enum import Enum

class ResourceType(Enum):
    SECURITY_GUARD = "SECURITY_GUARD"
    CAMERA = "CAMERA"
    SENSOR = "SENSOR"
    RESPONSE_TEAM = "RESPONSE_TEAM"

@dataclass
class Resource:
    id: str
    type: ResourceType
    location: tuple
    status: str
    capabilities: List[str]
    current_assignment: str = None

class ResourceOptimizer:
    def __init__(self):
        self.resources = {}
        self.assignments = {}
        self.coverage_map = {}
        self.historical_data = []
        
    def optimize_deployment(self, threat_assessment: Dict[str, Any], 
                          analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize resource deployment based on current situation"""
        optimization_result = {
            'resource_assignments': {},
            'coverage_analysis': {},
            'recommendations': []
        }
        
        try:
            # Analyze current situation
            priority_zones = self._identify_priority_zones(threat_assessment, analytics_data)
            
            # Optimize resource allocation
            new_assignments = self._allocate_resources(priority_zones)
            
            # Update assignments
            self.assignments.update(new_assignments)
            optimization_result['resource_assignments'] = new_assignments
            
            # Analyze coverage
            coverage_analysis = self._analyze_coverage(new_assignments, priority_zones)
            optimization_result['coverage_analysis'] = coverage_analysis
            
            # Generate recommendations
            optimization_result['recommendations'] = self._generate_recommendations(
                coverage_analysis, priority_zones
            )
            
            return optimization_result
            
        except Exception as e:
            print(f"Error in resource optimization: {str(e)}")
            return optimization_result
    
    def add_resource(self, resource: Resource):
        """Add new resource to the system"""
        self.resources[resource.id] = resource
        self._update_coverage_map()
    
    def update_resource_status(self, resource_id: str, 
                             status: str, location: tuple = None):
        """Update resource status and location"""
        if resource_id in self.resources:
            resource = self.resources[resource_id]
            resource.status = status
            if location:
                resource.location = location
            self._update_coverage_map()
    
    def _identify_priority_zones(self, threat_assessment: Dict[str, Any], 
                               analytics_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify zones requiring priority coverage"""
        priority_zones = []
        
        # Add high-threat areas
        for threat in threat_assessment.get('immediate_threats', []):
            if threat['level'] > 0.6:
                priority_zones.append({
                    'location': threat.get('location', (0, 0)),
                    'priority': threat['level'],
                    'reason': f"Active {threat['type']} threat"
                })
        
        # Add analytics-based hotspots
        for hotspot in analytics_data.get('hotspots', []):
            if hotspot['avg_severity'] > 0.5:
                priority_zones.append({
                    'location': hotspot['location'],
                    'priority': hotspot['avg_severity'],
                    'reason': 'Historical hotspot'
                })
        
        return sorted(priority_zones, key=lambda x: x['priority'], reverse=True)
    
    def _allocate_resources(self, priority_zones: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Allocate resources to priority zones"""
        assignments = {}
        available_resources = {
            r_id: r for r_id, r in self.resources.items()
            if r.status == 'available' and not r.current_assignment
        }
        
        for zone in priority_zones:
            zone_location = zone['location']
            needed_resources = self._determine_resource_needs(zone)
            
            for resource_type, count in needed_resources.items():
                # Find nearest available resources of required type
                suitable_resources = [
                    (r_id, r) for r_id, r in available_resources.items()
                    if r.type == ResourceType(resource_type)
                ]
                
                if suitable_resources:
                    # Sort by distance to zone
                    sorted_resources = sorted(
                        suitable_resources,
                        key=lambda x: self._calculate_distance(x[1].location, zone_location)
                    )
                    
                    # Assign resources
                    for _ in range(min(count, len(sorted_resources))):
                        r_id, resource = sorted_resources.pop(0)
                        assignments[r_id] = {
                            'zone_location': zone_location,
                            'priority': zone['priority'],
                            'reason': zone['reason']
                        }
                        resource.current_assignment = str(zone_location)
                        del available_resources[r_id]
        
        return assignments
    
    def _determine_resource_needs(self, zone: Dict[str, Any]) -> Dict[str, int]:
        """Determine required resources for a zone"""
        priority = zone['priority']
        
        if priority > 0.8:
            return {
                'SECURITY_GUARD': 2,
                'CAMERA': 3,
                'SENSOR': 4,
                'RESPONSE_TEAM': 1
            }
        elif priority > 0.6:
            return {
                'SECURITY_GUARD': 1,
                'CAMERA': 2,
                'SENSOR': 3,
                'RESPONSE_TEAM': 1
            }
        else:
            return {
                'SECURITY_GUARD': 1,
                'CAMERA': 1,
                'SENSOR': 2
            }
    
    def _analyze_coverage(self, assignments: Dict[str, Any], 
                         priority_zones: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze coverage effectiveness"""
        coverage = {
            'overall_coverage': 0,
            'priority_zone_coverage': {},
            'gaps': [],
            'redundancies': []
        }
        
        # Analyze each priority zone
        for zone in priority_zones:
            zone_location = zone['location']
            zone_coverage = self._calculate_zone_coverage(zone_location, assignments)
            
            coverage['priority_zone_coverage'][str(zone_location)] = zone_coverage
            
            # Identify gaps
            if zone_coverage < 0.7:  # Less than 70% coverage
                coverage['gaps'].append({
                    'location': zone_location,
                    'coverage': zone_coverage,
                    'priority': zone['priority']
                })
        
        # Calculate overall coverage
        if coverage['priority_zone_coverage']:
            coverage['overall_coverage'] = sum(coverage['priority_zone_coverage'].values()) / \
                                         len(coverage['priority_zone_coverage'])
        
        # Identify redundancies
        coverage['redundancies'] = self._identify_redundancies(assignments)
        
        return coverage
    
    def _calculate_zone_coverage(self, location: tuple, 
                               assignments: Dict[str, Any]) -> float:
        """Calculate coverage level for a specific zone"""
        assigned_resources = [
            r_id for r_id, assignment in assignments.items()
            if self._calculate_distance(assignment['zone_location'], location) < 100  # Within 100 units
        ]
        
        # Weight different resource types
        weights = {
            'SECURITY_GUARD': 0.3,
            'CAMERA': 0.25,
            'SENSOR': 0.15,
            'RESPONSE_TEAM': 0.3
        }
        
        coverage = 0
        for r_id in assigned_resources:
            resource = self.resources[r_id]
            coverage += weights[resource.type.value]
        
        return min(coverage, 1.0)  # Cap at 100%
    
    def _identify_redundancies(self, assignments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify areas with resource redundancy"""
        redundancies = []
        assigned_locations = {}
        
        # Group assignments by location
        for r_id, assignment in assignments.items():
            location = str(assignment['zone_location'])
            if location not in assigned_locations:
                assigned_locations[location] = []
            assigned_locations[location].append(r_id)
        
        # Check for redundancies
        for location, resources in assigned_locations.items():
            if len(resources) > 3:  # More than 3 resources in same location
                resource_types = [self.resources[r_id].type.value for r_id in resources]
                redundancies.append({
                    'location': eval(location),  # Convert string back to tuple
                    'resource_count': len(resources),
                    'resource_types': resource_types
                })
        
        return redundancies
    
    def _generate_recommendations(self, coverage_analysis: Dict[str, Any],
                                priority_zones: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Address coverage gaps
        for gap in coverage_analysis['gaps']:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Increase coverage',
                'details': f"Coverage gap detected at {gap['location']} "
                          f"(current coverage: {gap['coverage']:.2%})"
            })
        
        # Address redundancies
        for redundancy in coverage_analysis['redundancies']:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Optimize resource distribution',
                'details': f"Resource redundancy at {redundancy['location']} "
                          f"({redundancy['resource_count']} resources)"
            })
        
        # General coverage recommendations
        if coverage_analysis['overall_coverage'] < 0.8:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Increase overall coverage',
                'details': f"Overall coverage is below target "
                          f"({coverage_analysis['overall_coverage']:.2%})"
            })
        
        return recommendations
    
    def _update_coverage_map(self):
        """Update the coverage map based on current resource positions"""
        self.coverage_map = {}
        
        for resource in self.resources.values():
            x, y = resource.location
            coverage_radius = self._get_coverage_radius(resource.type)
            
            # Update coverage in radius
            for dx in range(-coverage_radius, coverage_radius + 1):
                for dy in range(-coverage_radius, coverage_radius + 1):
                    if dx*dx + dy*dy <= coverage_radius*coverage_radius:
                        point = (x + dx, y + dy)
                        if point not in self.coverage_map:
                            self.coverage_map[point] = 0
                        self.coverage_map[point] += 1
    
    def _get_coverage_radius(self, resource_type: ResourceType) -> int:
        """Get coverage radius for resource type"""
        coverage_radii = {
            ResourceType.SECURITY_GUARD: 50,
            ResourceType.CAMERA: 100,
            ResourceType.SENSOR: 75,
            ResourceType.RESPONSE_TEAM: 150
        }
        return coverage_radii.get(resource_type, 50)
    
    def _calculate_distance(self, point1: tuple, point2: tuple) -> float:
        """Calculate distance between two points"""
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)