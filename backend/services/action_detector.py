import os
import cv2
from moviepy.editor import VideoFileClip
from google.cloud import vision
import numpy as np

class ActionDetector:
    def __init__(self, api_key=None):
        if not api_key:
            raise ValueError("API key path is required")
            
        # Ensure the key file exists
        if not os.path.exists(api_key):
            raise FileNotFoundError(f"Google Cloud key file not found at: {api_key}")
            
        # Set the environment variable
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key
        
        try:
            # Create the client after setting environment variable
            self.client = vision.ImageAnnotatorClient()
        except Exception as e:
            print(f"Error initializing Vision API client: {str(e)}")
            raise

    def detect_key_moment(self, video_path):
        """
        Uses Google Cloud Vision to analyze frames and find the most active moments
        Returns list of (timestamp, score) tuples sorted by activity level
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found at: {video_path}")

        video = VideoFileClip(video_path)
        fps = video.fps
        duration = video.duration
        total_frames = int(fps * duration)
        
        # Sample frames throughout video
        sample_interval = max(total_frames // 20, 1)  # 20 samples
        moments = []
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file: {video_path}")
        
        for frame_num in range(0, total_frames, sample_interval):
            timestamp = frame_num / fps
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            
            if not ret:
                continue
                
            # Encode frame for Vision API
            success, buffer = cv2.imencode('.jpg', frame)
            if not success:
                print(f"Failed to encode frame at {timestamp:.2f}s")
                continue
            content = buffer.tobytes()
            
            try:
                # Create image object and feature
                image = vision.Image(content=content)
                features = [
                    vision.Feature(type_=vision.Feature.Type.OBJECT_LOCALIZATION),
                    vision.Feature(type_=vision.Feature.Type.FACE_DETECTION)
                ]
                request = vision.AnnotateImageRequest(image=image, features=features)
                response = self.client.batch_annotate_images(requests=[request])
                
                # Get annotations
                result = response.responses[0]
                objects = result.localized_object_annotations
                faces = result.face_annotations
                
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
        return moments
