from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from static_keyframe_extractor.extractor import extract_static_keyframes


class ExtractStaticKeyframesTests(unittest.TestCase):
    def _write_video(self, path: Path, frames: list[np.ndarray], fps: float = 5.0) -> None:
        height, width = frames[0].shape[:2]
        writer = cv2.VideoWriter(
            str(path),
            cv2.VideoWriter_fourcc(*"MJPG"),
            fps,
            (width, height),
        )
        self.assertTrue(writer.isOpened(), "OpenCV could not create the synthetic test video.")
        try:
            for frame in frames:
                writer.write(frame)
        finally:
            writer.release()

    def test_extracts_one_keyframe_per_stable_sequence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            video_path = tmp / "stable-scenes.avi"
            output_dir = tmp / "frames"

            black = np.zeros((32, 32, 3), dtype=np.uint8)
            white = np.full((32, 32, 3), 255, dtype=np.uint8)
            frames = [black.copy() for _ in range(4)] + [white.copy() for _ in range(4)]
            self._write_video(video_path, frames)

            result = extract_static_keyframes(
                video_path,
                output_dir,
                diff_threshold=5.0,
                stability_frames=3,
                start_index=5,
            )

            self.assertEqual(result.total_frames, 8)
            self.assertEqual(len(result.keyframes), 2)
            self.assertEqual([item.path.name for item in result.keyframes], [
                "keyframe_000005.jpg",
                "keyframe_000006.jpg",
            ])
            self.assertEqual([item.frame_index for item in result.keyframes], [2, 6])
            self.assertAlmostEqual(result.keyframes[0].timestamp or 0.0, 0.4, places=2)
            self.assertAlmostEqual(result.keyframes[1].timestamp or 0.0, 1.2, places=2)

    def test_returns_no_keyframes_when_frames_never_stabilize(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            video_path = tmp / "alternating.avi"
            output_dir = tmp / "frames"

            black = np.zeros((24, 24, 3), dtype=np.uint8)
            white = np.full((24, 24, 3), 255, dtype=np.uint8)
            frames = [black, white, black, white, black, white]
            self._write_video(video_path, frames)

            result = extract_static_keyframes(
                video_path,
                output_dir,
                diff_threshold=5.0,
                stability_frames=3,
            )

            self.assertEqual(result.total_frames, 6)
            self.assertEqual(result.keyframes, [])
            self.assertEqual(list(output_dir.glob("*.jpg")), [])

    def test_rejects_invalid_arguments_before_opening_video(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            output_dir = tmp / "frames"
            missing_video = tmp / "missing.avi"

            with self.assertRaisesRegex(ValueError, "diff_threshold must be positive"):
                extract_static_keyframes(missing_video, output_dir, diff_threshold=0)

            with self.assertRaisesRegex(ValueError, "stability_frames must be greater than zero"):
                extract_static_keyframes(missing_video, output_dir, stability_frames=0)

            with self.assertRaisesRegex(ValueError, "start_index must be zero or positive"):
                extract_static_keyframes(missing_video, output_dir, start_index=-1)

            with self.assertRaisesRegex(ValueError, "Video file not found"):
                extract_static_keyframes(missing_video, output_dir)


if __name__ == "__main__":
    unittest.main()
