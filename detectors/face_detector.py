"""
Face detection and recognition module
"""
import face_recognition
import cv2
import numpy as np

class FaceDetector:
    def __init__(self, confidence=0.7):
        self.confidence = confidence
        self.known_faces = {}
        self.face_encodings = {}
    
    def add_known_face(self, name, image_path):
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        self.known_faces[name] = encoding
    
    def detect(self, frame):
        # Reduce frame size for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = small_frame[:, :, ::-1]
        
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        detections = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Scale back up face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            matches = face_recognition.compare_faces(list(self.known_faces.values()), face_encoding)
            name = "Unknown"
            
            if True in matches:
                first_match_index = matches.index(True)
                name = list(self.known_faces.keys())[first_match_index]
            
            detections.append({
                'box': [left, top, right, bottom],
                'name': name
            })
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame, len(detections) > 0, detections