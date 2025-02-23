import base64
import tempfile
import wave
from pathlib import Path

import ffmpeg
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from tqdm import tqdm


class AudioAnalyzer:
    """
    A class for analyzing audio files, including MP4 to WAV conversion and OpenAI analysis.
    """

    def __init__(self, openai_client: OpenAI):
        """
        Initializes the AudioAnalyzer with an OpenAI client.

        Args:
            openai_client: An instance of the OpenAI client.
        """
        self.client = openai_client
        self.CHUNK_DURATION = 120  # 2 minutes in seconds

    def extract_audio_bytes(self, mp4_path: str) -> bytes:
        """
        Extracts audio bytes from an MP4 file using ffmpeg.

        Args:
            mp4_path: The path to the MP4 file.

        Returns:
            The audio data in bytes.

        Raises:
            AssertionError: If the MP4 file does not exist.
        """
        assert Path(mp4_path).exists(), "Incorrect filepath provided."

        out, _ = (
            ffmpeg.input(mp4_path)
            .output("pipe:", format="wav")
            .run(capture_stdout=True, capture_stderr=True)
        )

        return out

    def get_audio_duration(self, wav_bytes: bytes) -> float:
        """
        Get the duration of audio in seconds from WAV bytes.

        Args:
            wav_bytes: The audio data in bytes.

        Returns:
            Duration in seconds.
        """
        with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:
            temp_file.write(wav_bytes)
            temp_file.flush()

            with wave.open(temp_file.name, "rb") as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)
                return duration

    def chunk_audio(self, wav_bytes: bytes) -> list[bytes]:
        """
        Split audio into chunks of CHUNK_DURATION seconds.

        Args:
            wav_bytes: The audio data in bytes.

        Returns:
            List of audio chunks in bytes.
        """
        chunks = []
        with tempfile.NamedTemporaryFile(suffix=".wav") as input_file:
            input_file.write(wav_bytes)
            input_file.flush()

            probe = ffmpeg.probe(input_file.name)
            duration = float(probe["format"]["duration"])

            for start_time in range(0, int(duration), self.CHUNK_DURATION):
                with tempfile.NamedTemporaryFile(suffix=".wav") as chunk_file:
                    stream = (
                        ffmpeg.input(
                            input_file.name, ss=start_time, t=self.CHUNK_DURATION
                        )
                        .output(chunk_file.name, acodec="pcm_s16le", ac=1, ar=16000)
                        .overwrite_output()
                    )
                    ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)

                    with open(chunk_file.name, "rb") as f:
                        chunks.append(f.read())

        return chunks

    def parse_audio_file(self, wav_path: str) -> bytes:
        """
        Parses a WAV audio file and returns its byte data.

        Args:
            wav_path: The path to the WAV file.

        Returns:
            The audio data in bytes.

        Raises:
            AssertionError: If the WAV file does not exist.
        """
        assert Path(wav_path).exists(), "Incorrect filepath provided."

        with open(wav_path, "rb") as f:
            wav_data = f.read()

        return wav_data

    def analyze_audio(self, audio_bytes: bytes) -> ChatCompletionMessage:
        """
        Analyzes audio bytes using the OpenAI API.

        Args:
            audio_bytes: The audio data in bytes.

        Returns:
            The ChatCompletionMessage object containing the model's response.
        """
        encoded_string = base64.b64encode(audio_bytes).decode("utf-8")

        completion = self.client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "wav"},
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is in this recording? Give brief tonal cues and evaluations too along with the transcription. Cut out the fluff - just give what I want.",
                        },
                        {
                            "type": "input_audio",
                            "input_audio": {"data": encoded_string, "format": "wav"},
                        },
                    ],
                },
            ],
        )

        return completion.choices[0].message

    def analyze_audio_with_chunking(self, audio_bytes: bytes) -> str:
        """
        Analyzes audio with automatic chunking for long files.

        Args:
            audio_bytes: The audio data in bytes.

        Returns:
            Combined transcription string from all chunks.
        """
        duration = self.get_audio_duration(audio_bytes)

        if duration <= self.CHUNK_DURATION:
            response = self.analyze_audio(audio_bytes)
            return response.content[0].text

        chunks = self.chunk_audio(audio_bytes)
        transcriptions = []

        for chunk in tqdm(chunks):
            response = self.analyze_audio(chunk)
            transcriptions.append(response.to_dict()['audio']['transcript'])

        return " ".join(transcriptions)

    def analyze_mp4_audio(self, mp4_path: str) -> str:
        """
        Analyzes audio from an MP4 file using the OpenAI API with chunking support.

        Args:
            mp4_path: The path to the MP4 file.

        Returns:
            Combined transcription string.
        """
        audio_bytes = self.extract_audio_bytes(mp4_path)
        return self.analyze_audio_with_chunking(audio_bytes)

    def analyze_wav_audio(self, wav_path: str) -> str:
        """
        Analyzes audio from a wav file using the OpenAI API with chunking support.

        Args:
            wav_path: The path to the wav file.

        Returns:
            Combined transcription string.
        """
        audio_bytes = self.parse_audio_file(wav_path)
        return self.analyze_audio_with_chunking(audio_bytes)


if __name__ == "__main__":
    client = OpenAI()
    analyzer = AudioAnalyzer(client)

    transcription: str = analyzer.analyze_wav_audio("./police_encounter.wav")

    print(f"Transcription: {transcription}")
