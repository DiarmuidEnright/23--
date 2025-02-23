import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip

class SubtitleGenerator:
    def __init__(self, api_key=None):
        self.recognizer = sr.Recognizer()

    def _extract_audio(self, video_path):
        """Extract audio from video file"""
        video = VideoFileClip(video_path)
        audio_path = video_path.replace('.mp4', '.wav')
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        return audio_path

    def extract_text(self, video_path):
        """
        Extracts text from video audio and saves it to a file
        Returns the path to the text file and the transcript
        """
        # Extract audio
        audio_path = self._extract_audio(video_path)
        
        # Transcribe audio using local speech recognition
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                transcript = self.recognizer.recognize_google(audio)
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            transcript = ""
        
        # If transcript is empty or indicates no audio, provide a clear message
        if not transcript or "do not have audio" in transcript:
            message = "No audio content detected in the video."
            output_path = video_path.replace('.mp4', '_transcript.txt')
            with open(output_path, 'w') as f:
                f.write(message)
            
            # Clean up
            os.remove(audio_path)
            
            return output_path, message
        else:
            # Save transcript to file
            output_path = video_path.replace('.mp4', '_transcript.txt')
            with open(output_path, 'w') as f:
                f.write(transcript)
            
            # Clean up
            os.remove(audio_path)
            
            return output_path, transcript
