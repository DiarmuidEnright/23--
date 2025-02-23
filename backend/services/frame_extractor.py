import time

import cv2
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

device = torch.device("cpu")

def rescale_frame(frame_input, percent: int = 50):
    """Downsample the frame dimensions by a specified percentage."""

    width = int(frame_input.shape[1] * percent / 100)
    height = int(frame_input.shape[0] * percent / 100)
    dim = (width, height)

    return cv2.resize(frame_input, dim, interpolation=cv2.INTER_AREA)


def load_video(video_path: str) -> list[Image.Image]:
    """Load a video, process frames, and return as list of PIL Images."""

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    if original_fps <= 0:
        print("Warning - FPS not correctly detected")
        original_fps = 30.0  # Default assumption if FPS unavailable

    desired_fps = 1
    frame_interval = 1.0 / desired_fps
    current_time = 0.0
    frames = []

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Calculate frame timing
        frame_pos = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1  # Current frame index
        frame_time = frame_pos / original_fps

        if frame_time >= current_time:
            resized_frame = rescale_frame(frame)
            pil_image = Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB))
            frames.append(pil_image)
            current_time += frame_interval

    cap.release()
    return frames

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32",
    torch_dtype=torch.float16,
    attn_implementation="sdpa",
)
model = model.to(device)

processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", device=device)


if __name__ == '__main__':
    frames = load_video("police_encounter.mp4")
    print("Processing - this may take a while...")

    start = time.time()

    inputs = processor(
        text=[
            "Officer taking gunpoint at bushes",
            "Police officer",
            "Gun",
            "Incidence",
            "Migrant",
            "Shooting",
            "Aggression",
        ],
        images=frames,
        return_tensors="pt",
        padding=True,
    ).to(device)

    output = model(**inputs)

    print("Time Taken:", time.time() - start)

    probs = torch.max(torch.softmax(output["logits_per_image"], -1), -1)

    print(f"The frames with the higest probs for prompts: {probs}")
