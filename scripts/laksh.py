#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

def _ensure_src_on_path() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    src_path = repo_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


def _version_command(args: argparse.Namespace) -> None:
    print("lakshai v0.1.0")

def _smoke_command(args: argparse.Namespace) -> None:
    # trivial smoke test
    print("smoke ok")

def _run_command(args: argparse.Namespace) -> None:
    _ensure_src_on_path()
    from lakshai.io import read_video
    video_path = Path(args.video)
    out_path = Path(args.out)
    max_frames = args.max_frames

    if not video_path.exists():
        print(f"Error: video file not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    out_path.mkdir(parents=True, exist_ok=True)

    try:
        frames, metadata = read_video(str(video_path), max_frames)
    except Exception as e:
        print(f"Error reading video: {e}", file=sys.stderr)
        sys.exit(1)

    summary = {
        "frame_count_used": len(frames),
        "fps": metadata["fps"],
        "width": metadata["width"],
        "height": metadata["height"],
    }
    summary_file = out_path / "summary.json"
    with summary_file.open("w") as f:
        json.dump(summary, f)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    version_parser = subparsers.add_parser("version", help="Show version")
    version_parser.set_defaults(func=_version_command)

    smoke_parser = subparsers.add_parser("smoke", help="Run smoke test")
    smoke_parser.set_defaults(func=_smoke_command)

    run_parser = subparsers.add_parser("run", help="Run video pipeline")
    run_parser.add_argument("--video", required=True, help="Path to the video file")
    run_parser.add_argument("--out", required=True, help="Directory to write summary")
    run_parser.add_argument("--max-frames", type=int, default=1, help="Max number of frames")
    run_parser.set_defaults(func=_run_command)

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()