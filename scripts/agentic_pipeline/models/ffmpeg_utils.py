"""
ffmpeg_utils.py — Robust discovery and verification of FFmpeg and FFprobe binaries.
"""

import os
import shutil
import logging

logger = logging.getLogger("FFmpegUtils")

_FFMPEG_PATH = None
_FFPROBE_PATH = None


def get_ffmpeg_path() -> str:
    global _FFMPEG_PATH
    if _FFMPEG_PATH and os.path.exists(_FFMPEG_PATH):
        return _FFMPEG_PATH

    # 1. Check virtualenv bin
    venv_ffmpeg = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.venv/bin/ffmpeg"))
    if os.path.exists(venv_ffmpeg):
        _FFMPEG_PATH = venv_ffmpeg
        return _FFMPEG_PATH

    # 2. Check imageio_ffmpeg
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            _FFMPEG_PATH = exe
            return _FFMPEG_PATH
    except Exception:
        pass

    # 3. Check system path
    sys_path = shutil.which("ffmpeg")
    if sys_path:
        _FFMPEG_PATH = sys_path
        return _FFMPEG_PATH

    return "ffmpeg"


def get_ffprobe_path() -> str:
    global _FFPROBE_PATH
    if _FFPROBE_PATH and os.path.exists(_FFPROBE_PATH):
        return _FFPROBE_PATH

    venv_ffprobe = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.venv/bin/ffprobe"))
    if os.path.exists(venv_ffprobe):
        _FFPROBE_PATH = venv_ffprobe
        return _FFPROBE_PATH

    sys_path = shutil.which("ffprobe")
    if sys_path:
        _FFPROBE_PATH = sys_path
        return _FFPROBE_PATH

    return "ffprobe"
