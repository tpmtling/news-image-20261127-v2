#!/usr/bin/env python3
"""news-image-20261127 entrypoint: copy the pre-rendered front page to the output.

Standard library only, so it runs unchanged in the scorer's python:3.13-slim
image (no Pillow there). The image itself is rendered offline by render.py.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    # entry.png ships in this repository; resolve it from this file, not the
    # working directory, so the scorer's clean-directory run still finds it.
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
