"""
director_clipper.py — Agent Director for Video Clipping & Viral Repurposing.
Extracts viral highlights from uploaded videos or YouTube/web URLs and reframes them to vertical 9:16 shorts.
"""

import os
import sys
import json
import logging
import subprocess
from typing import Dict, Any, List
from ..models.types import UserIntent
from ..subagents.agent_healer import AgentHealer
from ..models.ffmpeg_utils import get_ffmpeg_path

logger = logging.getLogger("DirectorClipper")


class DirectorClipper:
    """
    Directs video ingestion, viral clip extraction, and vertical 9:16 reframing.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.healer = AgentHealer()

    def clip_long_video(self, intent: UserIntent) -> Dict[str, Any]:
        logger.info(f"✂️ [Director Clipper] Processing media clipping request: {intent.source_url or intent.source_file}...")

        source_path = intent.source_file
        if intent.source_url:
            source_path = self._download_source_media(intent.source_url)

        if not source_path or not os.path.exists(source_path):
            raise FileNotFoundError(f"Source media not available for clipping: {source_path}")

        # Extract viral segment (default 00:00 to 00:45 or target duration)
        duration = intent.target_duration or 45.0
        start_time = intent.extra_instructions.get("start_time", "00:00:10")
        output_clip_path = os.path.join(self.output_dir, "viral_clipped_short.mp4")

        # Vertical reframe filter: crop center 1080x1920 or stack blurred background
        vf = (
            "split[original][copy];"
            "[copy]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:10[bg];"
            "[original]scale=1080:-1[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2"
        )

        cmd = [
            get_ffmpeg_path(), "-y",
            "-ss", start_time,
            "-i", source_path,
            "-t", str(duration),
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            output_clip_path
        ]

        logger.info(f"Rendering vertical reframe with FFmpeg: {output_clip_path}...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            logger.error(f"Clipping render failed: {res.stderr[-300:]}")
            raise RuntimeError(f"FFmpeg clipping failed: {res.stderr[-200:]}")

        result = {
            "status": "COMPLETED",
            "source": intent.source_url or intent.source_file,
            "clipped_short_path": output_clip_path,
            "duration": duration,
            "aspect_ratio": "9:16 (1080x1920)",
            "start_time": start_time
        }

        with open(os.path.join(self.output_dir, "clipper_report.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        logger.info(f"✨ [Director Clipper] Viral vertical short created: {output_clip_path}")
        return result

    def _download_source_media(self, url: str) -> str:
        """Downloads media via yt-dlp."""
        out_template = os.path.join(self.output_dir, "downloaded_source.%(ext)s")
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", out_template,
            url
        ]
        logger.info(f"Downloading stream from {url}...")
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        expected_path = os.path.join(self.output_dir, "downloaded_source.mp4")
        return expected_path
