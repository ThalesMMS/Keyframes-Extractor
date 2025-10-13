"""Core static keyframe extraction logic."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np


@dataclass(frozen=True)
class Keyframe:
    """Represents a saved keyframe output."""

    path: Path
    frame_index: int
    timestamp: Optional[float]


@dataclass(frozen=True)
class ExtractionResult:
    """Summary of a keyframe extraction run."""

    keyframes: List[Keyframe]
    total_frames: int
    fps: Optional[float]


def extract_static_keyframes(
    video_path: Path,
    output_folder: Path,
    *,
    diff_threshold: float = 12.0,
    stability_frames: int = 15,
    start_index: int = 0,
) -> ExtractionResult:
    """
    Detect stable scenes in a video and save a representative frame for each.

    Args:
        video_path: Input video file.
        output_folder: Destination directory for extracted keyframes.
        diff_threshold: Maximum average grayscale difference to consider frames stable.
        stability_frames: Number of consecutive frames under the threshold before saving a keyframe.
        start_index: Starting index used in the output filename counter.

    Returns:
        ExtractionResult containing the saved keyframes and video metadata.

    Raises:
        ValueError: If the inputs are invalid or the video cannot be processed.
    """
    video_path = video_path.expanduser()
    output_folder = output_folder.expanduser()

    if diff_threshold <= 0:
        raise ValueError("diff_threshold must be positive.")
    if stability_frames <= 0:
        raise ValueError("stability_frames must be greater than zero.")
    if start_index < 0:
        raise ValueError("start_index must be zero or positive.")
    if not video_path.exists() or not video_path.is_file():
        raise ValueError(f"Video file not found: {video_path}")

    output_folder.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Unable to open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    fps = fps if fps and fps > 0 else None

    keyframes: List[Keyframe] = []
    stable_count = 0
    saved_in_sequence = False
    frame_index = -1
    next_index = start_index
    prev_gray: Optional[np.ndarray] = None
    last_stable_frame: Optional[np.ndarray] = None

    try:
        while True:
            has_frame, frame = cap.read()
            if not has_frame:
                break

            frame_index += 1

            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            except cv2.error as exc:
                raise ValueError(f"Unable to convert frame {frame_index} to grayscale") from exc

            if prev_gray is None:
                prev_gray = gray
                stable_count = 1
                last_stable_frame = frame
                continue

            diff_value = float(cv2.absdiff(gray, prev_gray).mean())

            if diff_value < diff_threshold:
                stable_count += 1
                last_stable_frame = frame

                if stable_count >= stability_frames and not saved_in_sequence:
                    output_path = output_folder / f"keyframe_{next_index:06d}.jpg"
                    if not cv2.imwrite(str(output_path), last_stable_frame):
                        raise ValueError(f"Failed to write keyframe to {output_path}")
                    timestamp = (frame_index / fps) if fps else None
                    keyframes.append(
                        Keyframe(
                            path=output_path,
                            frame_index=frame_index,
                            timestamp=timestamp,
                        )
                    )
                    saved_in_sequence = True
                    next_index += 1
            else:
                stable_count = 1
                saved_in_sequence = False
                last_stable_frame = frame

            prev_gray = gray
    finally:
        cap.release()

    return ExtractionResult(
        keyframes=keyframes,
        total_frames=frame_index + 1 if frame_index >= 0 else 0,
        fps=fps,
    )
