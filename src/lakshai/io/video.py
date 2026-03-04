# lakshai/io/video.py
from __future__ import annotations
from typing import List, Tuple, Dict

try:
    import cv2
except ImportError:
    cv2 = None


def read_video(video_path: str, max_frames: int) -> Tuple[List, Dict[str, float]]:
    """
    Read up to max_frames evenly spaced frames from a video file.

    :param video_path: Path to the video file.
    :param max_frames: Maximum number of frames to extract.
    :return: (frames, metadata) where metadata has keys fps, width, height.
    :raises RuntimeError: if OpenCV is not installed.
    """
    if cv2 is None:
        raise RuntimeError(
            "OpenCV is required. Install opencv-python-headless in your environment."
        )

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video file: {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = float(cap.get(cv2.CAP_PROP_FPS)) or 0.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if max_frames < 1 or total_frames == 0:
        return [], {"fps": fps, "width": width, "height": height}

    step = max(1, total_frames // max_frames)
    frame_indices = [i for i in range(0, min(total_frames, step * max_frames), step)]

    frames = []
    for i in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()
    return frames, {"fps": fps, "width": width, "height": height}
