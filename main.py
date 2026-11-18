#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261117.

Writes the pre-rendered front-page image to /output/entry.png.
Deterministic: no network, no timestamps, no randomness — it copies the
bundled image byte-for-byte, so repeated runs produce identical output.

The image itself was rendered programmatically (see render.py, PIL +
DejaVu fonts) from real, researched news of Tuesday 17 November 2026.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    print(f"wrote {DST}")


if __name__ == "__main__":
    main()
