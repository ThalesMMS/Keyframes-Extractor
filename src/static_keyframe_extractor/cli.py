"""Command-line interface for the static keyframe extractor."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .extractor import extract_static_keyframes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract static keyframes from a video by detecting periods of stability.",
    )
    parser.add_argument(
        "video_path",
        type=Path,
        help="Path to the input video file.",
    )
    parser.add_argument(
        "output_folder",
        type=Path,
        help="Directory where extracted keyframes will be stored.",
    )
    parser.add_argument(
        "--diff-threshold",
        type=float,
        default=12.0,
        help="Average grayscale difference threshold for considering consecutive frames as stable (default: 12.0).",
    )
    parser.add_argument(
        "--stability-frames",
        type=int,
        default=15,
        help="Minimum number of consecutive stable frames required before saving a keyframe (default: 15).",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=0,
        help="Starting index used for naming output files (default: 0).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        result = extract_static_keyframes(
            args.video_path,
            args.output_folder,
            diff_threshold=args.diff_threshold,
            stability_frames=args.stability_frames,
            start_index=args.start_index,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Processing video: {args.video_path}")
    print(
        f"Parameters - diff_threshold: {args.diff_threshold}, stability_frames: {args.stability_frames}, start_index: {args.start_index}"
    )
    print(f"Saving keyframes to: {args.output_folder}")

    if not result.keyframes:
        print("No stable segments detected with the current parameters.")
    else:
        for keyframe in result.keyframes:
            if keyframe.timestamp is not None:
                print(
                    f"Saved {keyframe.path.name} at frame {keyframe.frame_index} (~{keyframe.timestamp:.2f}s)"
                )
            else:
                print(
                    f"Saved {keyframe.path.name} at frame {keyframe.frame_index}"
                )
        print(f"Done. Extracted {len(result.keyframes)} keyframe(s) from {result.total_frames} frame(s).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
