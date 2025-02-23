import os
import cv2
import base64
from moviepy.editor import VideoFileClip
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import numpy as np

class ActionDetector:
    def __init__(self, api_key=None):
        if api_key:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key
            try:
                # Force credentials to be loaded from the file
                self.client = vision_v1.ImageAnnotatorClient.from_service_account_json(api_key)
            except Exception as e:
                print(f"Error initializing Vision API client: {str(e)}")
                raise

    def detect_key_moment(self, video_path):
        """
        Uses Google Cloud Vision to analyze frames and find the most active moments
        Returns list of (timestamp, score) tuples sorted by activity level
        """
        video = VideoFileClip(video_path)
        fps = video.fps
        duration = video.duration
        total_frames = int(fps * duration)
        
        # Sample frames throughout video
        sample_interval = max(total_frames // 20, 1)  # 20 samples
        moments = []
        
        cap = cv2.VideoCapture(video_path)
        
        for frame_num in range(0, total_frames, sample_interval):
            timestamp = frame_num / fps
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            
            if not ret:
                continue
                
            # Encode frame for Vision API
            _, buffer = cv2.imencode('.jpg', frame)
            content = buffer.tobytes()
            
            try:
                # Create image object and feature
                image = types.Image(content=content)
                features = [
                    types.Feature(type_=vision_v1.Feature.Type.OBJECT_LOCALIZATION),
                    types.Feature(type_=vision_v1.Feature.Type.FACE_DETECTION)
                ]
                request = types.AnnotateImageRequest(image=image, features=features)
                response = self.client.batch_annotate_images(requests=[request])
                
                # Get annotations
                objects = response.responses[0].localized_object_annotations
                faces = response.responses[0].face_annotations
                
                # Calculate activity score based on:
                # - Number of detected objects (movement/activity)
                # - Face detection results (expressions, angles)
                # - Object positions and sizes
                
                object_score = min(len(objects) / 5, 1.0) * 4  # Up to 4 points for objects
                
                face_score = 0
                for face in faces:
                    # Add points for non-neutral expressions
                    if face.anger_likelihood >= 3: face_score += 2
                    if face.surprise_likelihood >= 3: face_score += 1
                    if abs(face.pan_angle) > 30: face_score += 1  # Quick head movement
                
                face_score = min(face_score, 6)  # Cap face score at 6 points
                
                total_score = object_score + face_score
                normalized_score = max(1, min(10, total_score))  # Scale to 1-10
                
                moments.append((timestamp, normalized_score))
                print(f"Analyzed frame at {timestamp:.2f}s - Activity Score: {normalized_score:.1f}")
                
            except Exception as e:
                print(f"Error analyzing frame at {timestamp:.2f}s: {str(e)}")
        
        cap.release()
        
        if not moments:
            # If no moments detected, return middle of video with neutral score
            return [(duration/2, 5)]
            
        # Sort moments by score in descending order
        moments.sort(key=lambda x: x[1], reverse=True)
        return moments
