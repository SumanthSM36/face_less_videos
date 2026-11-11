"""
video_renderer.py — Agent Video Renderer.
Final video assembly, subtitle burning, 35mm grain / lens vignette fingerprinting, and thumbnail extraction.
"""

import os
import sys
import logging
import subprocess
from typing import Dict, Any
from ..models.types import RenderResult
from ..models.ffmpeg_utils import get_ffmpeg_path, get_ffprobe_path

logger = logging.getLogger("VideoRenderer")


class VideoRenderer:
    """
    Renders 1080x1920 vertical MP4 videos with burned kinetic subtitles, 35mm grain, and lens vignette.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def render_final_short(self, motion_video: str, mastered_audio: str, ass_subtitles: str, output_mp4: str) -> RenderResult:
        logger.info(f"⚡ Agent Video Renderer: Executing final FFmpeg assembly & visual fingerprinting...")

        escaped_ass = ass_subtitles.replace(":", "\\:").replace("'", "\\'")

        # Filtergraph: scale 1080x1920 + burn subtitles + 35mm film grain + vignette
        vf = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            f"ass='{escaped_ass}',"
            "noise=c1s=7:c0s=7:allf=t,"
            "vignette=PI/4"
        )

        cmd = [
            get_ffmpeg_path(), "-y",
            "-i", motion_video,
            "-i", mastered_audio,
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "19",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "48000",
            "-shortest",
            output_mp4
        ]

        logger.debug(f"Executing render command: {' '.join(cmd[:10])}...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            logger.error(f"Render failed: {res.stderr[-400:]}")
            raise RuntimeError(f"FFmpeg assembly failed: {res.stderr[-250:]}")

        # Extract Frame 0 thumbnail
        thumb_path = output_mp4.replace(".mp4", "_thumb.jpg")
        thumb_cmd = [
            get_ffmpeg_path(), "-y",
            "-ss", "00:00:01",
            "-i", output_mp4,
            "-vframes", "1",
            "-q:v", "2",
            thumb_path
        ]
        subprocess.run(thumb_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        duration = self._probe_duration(output_mp4)
        file_size = os.path.getsize(output_mp4)

        result = RenderResult(
            video_path=output_mp4,
            thumbnail_path=thumb_path,
            duration_seconds=duration,
            resolution="1080x1920",
            file_size_bytes=file_size,
            fingerprint_applied=True
        )

        logger.info(f"✨ Agent Video Renderer: Final short rendered -> {output_mp4} ({duration:.2f}s, {file_size/1024/1024:.1f}MB)")
        return result

    def _probe_duration(self, video_path: str) -> float:
        try:
            cmd = [
                get_ffprobe_path(), "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                video_path
            ]
            out = subprocess.check_output(cmd, text=True).strip()
            return float(out)
        except Exception:
            return 45.0
