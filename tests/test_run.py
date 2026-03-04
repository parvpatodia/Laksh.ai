import json
import subprocess
from pathlib import Path

import cv2
import numpy as np


def test_run_summary(tmp_path):
    # Create a tiny synthetic video
    video_path = tmp_path / "tiny.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(video_path), fourcc, 5, (64, 64))
    for _ in range(10):
        frame = 255 * np.ones((64, 64, 3), dtype=np.uint8)
        out.write(frame)
    out.release()

    out_dir = tmp_path / "out"
    result = subprocess.run(
        [
            "python",
            str(Path(__file__).parents[1] / "scripts" / "laksh.py"),
            "run",
            "--video",
            str(video_path),
            "--out",
            str(out_dir),
            "--max-frames",
            "5",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    summary_file = out_dir / "summary.json"
    assert summary_file.exists()
    data = json.loads(summary_file.read_text())
    assert set(data) == {"frame_count_used", "fps", "width", "height"}
