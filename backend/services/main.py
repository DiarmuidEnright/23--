import os
import cv2
import base64
from dotenv import load_dotenv
from action_detector import ActionDetector
from video_trimmer import VideoTrimmer
from subtitle_generator import SubtitleGenerator
from frame_extractor import KeyFrameExtractor
from openai import OpenAI

class BodycamAnalysisWorkflow:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
        google_cloud_key = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config/hackathon-key-7e5ce787d8e4.json')
        self.action_detector = ActionDetector(google_cloud_key)
        self.video_trimmer = VideoTrimmer(os.getenv('OPENAI_API_KEY'))
        self.subtitle_generator = SubtitleGenerator(google_cloud_key)
        self.frame_extractor = KeyFrameExtractor(google_cloud_key)
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def analyze_footage(self, video_path):
        print("Detecting key moment...")
        key_moments = self.action_detector.detect_key_moment(video_path)
        if not key_moments:
            print("No significant moments detected")
            return None
        key_timestamp, highest_score = key_moments[0]
        print("Trimming video around most significant moment...")
        trimmed_video = self.video_trimmer.trim_video(video_path, key_timestamp)
        print("Extracting text from video...")
        transcript_path, transcript = self.subtitle_generator.extract_text(trimmed_video)
        print("Extracting and analyzing key frames...")
        frame_data = self.frame_extractor.extract_key_frames(trimmed_video)
        print("Analyzing protocol compliance...")
        analysis = self._analyze_protocol(frame_data, transcript)
        return {
            'trimmed_video': trimmed_video,
            'transcript_path': transcript_path,
            'key_frames': [frame['path'] for frame in frame_data],
            'frame_timestamps': [frame['timestamp'] for frame in frame_data],
            'transcript': transcript,
            'analysis': analysis
        }

    def _analyze_protocol(self, frame_data, transcript):
        frame_analyses = []
        context = "" # Suneet
        if transcript and transcript != "No audio content detected in the video.":
            context = f"\n\nContext - Audio transcript: {transcript}"
        for i, frame in enumerate(frame_data):
            time_desc = f"Frame {i+1} (at {frame['timestamp']:.2f}s)"
            try:
                img = cv2.imread(frame['path'])
                resized = cv2.resize(img, (224, 224))
                _, buffer = cv2.imencode('.jpg', resized, [cv2.IMWRITE_JPEG_QUALITY, 50])
                encoded = base64.b64encode(buffer).decode('utf-8')
                messages = [
                    {"role": "system", "content": "You are analyzing bodycam footage. Focus on assessing the level of aggression and concerning behavior in the scene."},
                    {"role": "user", "content": f"This is a frame from a bodycam video. {time_desc}. Focus ONLY on assessing the level of aggression and concerning behavior in this specific frame. Be concise.{context}\n\nImage: data:image/jpeg;base64,{encoded}"}
                ]
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=100
                )
                if response.choices[0].message.content:
                    frame_analyses.append(f"{time_desc}: {response.choices[0].message.content.strip()}")
                    print(f"Analyzed {time_desc}")
                else:
                    raise Exception("Empty response from model")
            except Exception as e:
                print(f"Error analyzing {time_desc}: {str(e)}")
                frame_analyses.append(f"{time_desc}: Analysis failed")
        try:
            summary_messages = [
                {"role": "system", "content": "You are summarizing a sequence of bodycam footage analyses."},
                {"role": "user", "content": "Based on these frame analyses, provide a BRIEF summary of how the level of aggression progresses. Focus on changes in behavior and tension:\n\n" + "\n\n".join(frame_analyses)}
            ]
            summary_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=summary_messages,
                max_tokens=200
            )
            if not summary_response.choices[0].message.content:
                return "Analysis failed: No summary generated"
            return summary_response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return "Analysis failed: Could not generate summary"

def main():
    workflow = BodycamAnalysisWorkflow()
    video_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "video_trimmed.mp4")
    if os.path.exists(video_path):
        results = workflow.analyze_footage(video_path)
        print("\nAnalysis Results:")
        print(results['analysis'])
        for frame_path in results['key_frames']:
            if os.path.exists(frame_path):
                os.remove(frame_path)
                print(f"Cleaned up temporary file: {frame_path}")
    else:
        print(f"Error: Video file not found at {video_path}")

if __name__ == "__main__":
    main()
