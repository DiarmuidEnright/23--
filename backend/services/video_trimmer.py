from moviepy.editor import VideoFileClip
import openai

class VideoTrimmer:
    def __init__(self, api_key=None):
        if api_key:
            openai.api_key = api_key

    def trim_video(self, video_path, timestamp, duration=25):
        """
        Extracts a segment of video centered around the key timestamp
        Duration is split evenly before and after the timestamp
        """
        video = VideoFileClip(video_path)
        half_duration = duration / 2
        
        start_time = max(0, timestamp - half_duration)
        end_time = min(video.duration, timestamp + half_duration)
        
        trimmed = video.subclip(start_time, end_time)
        output_path = video_path.replace('.mp4', '_trimmed.mp4')
        trimmed.write_videofile(output_path)
        
        return output_path

from action_detector import ActionDetector

def trim_most_active_clip(video_path, duration=25, detector_api_key=None):
    """
    Analyzes the video to find the most active and aggressive moment and trims the video around that moment.
    """
    detector = ActionDetector(api_key=detector_api_key) if detector_api_key else ActionDetector()
    moments = detector.detect_key_moment(video_path)
    best_timestamp = moments[0][0]  # highest scoring moment
    trimmer = VideoTrimmer()
    return trimmer.trim_video(video_path, best_timestamp, duration)
