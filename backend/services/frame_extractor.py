import cv2
import os
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part

#this is currently used to take the frames from the trimme 

class KeyFrameExtractor:
    def __init__(self, api_key=None):
        if api_key:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key
        vertexai.init(project="hackathon-413912", location="us-central1")
        self.model = GenerativeModel("gemini-pro-vision")

    def extract_key_frames(self, video_path):
        """Extract multiple frames evenly spaced across the video."""
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        # Extract 8 frames evenly spaced across the video
        num_frames = 8
        sample_interval = max(total_frames // num_frames, 1)
        frame_data = []
        
        for i in range(0, total_frames, sample_interval):
            if len(frame_data) >= num_frames:
                break
                
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                continue
                
            # Save the frame
            frame_path = f"{os.path.splitext(video_path)[0]}_frame_{i}.jpg"
            cv2.imwrite(frame_path, frame)
            
            # Encode for GPT analysis
            retval, buffer = cv2.imencode('.jpg', frame)
            if not retval:
                continue
            encoded_image = base64.b64encode(buffer).decode('utf-8')
            
            timestamp = i / fps  # Convert frame number to seconds
            frame_data.append({
                'path': frame_path,
                'frame_number': i,
                'timestamp': timestamp,
                'encoded': encoded_image
            })
            
        cap.release()
        return frame_data
