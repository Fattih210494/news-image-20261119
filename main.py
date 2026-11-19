"""Hand the finished front page over to the grader.

draw.py does the actual drawing; this launcher only makes sure the
picture on disk is a genuine JPEG of an acceptable size, then drops a
copy into the folder the competition harness reads from.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


MAX_BYTES = 1_048_576
JPEG_PREFIX = b"\xff\xd8\xff"


def picture_path() -> Path:
    """Where the rendered front page lives, next to this file."""
    return Path(__file__).resolve().parent / "entry.png"


def output_dir() -> Path:
    """Submission folder: env override wins, otherwise ./out."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent / "out"


def load_and_check(picture: Path) -> bytes:
    """Read the picture and refuse it unless it is a small JPEG."""
    if not picture.is_file():
        raise SystemExit(f"cannot find the entry picture: {picture}")
    payload = picture.read_bytes()
    if payload[:3] != JPEG_PREFIX:
        raise SystemExit(f"{picture} does not start with JPEG magic bytes")
    if len(payload) > MAX_BYTES:
        raise SystemExit(
            f"{picture} is {len(payload)} bytes, past the {MAX_BYTES}-byte cap"
        )
    return payload


def main() -> int:
    payload = load_and_check(picture_path())
    folder = output_dir()
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.png"
    target.write_bytes(payload)
    print(f"wrote {target} ({len(payload)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
