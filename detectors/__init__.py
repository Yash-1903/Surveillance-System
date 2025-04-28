"""
Initialize detectors package
"""
from .frame_processor import FrameProcessor
from .base_detector import BaseDetector
from .motion_detector import MotionDetector
from .fire_detector import FireDetector
from .weapon_detector import WeaponDetector
from .accident_detector import AccidentDetector
from .crowd_analyzer import CrowdAnalyzer

__all__ = [
    'FrameProcessor',
    'BaseDetector',
    'MotionDetector',
    'FireDetector',
    'WeaponDetector',
    'AccidentDetector',
    'CrowdAnalyzer'
]