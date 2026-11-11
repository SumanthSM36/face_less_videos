"""
media_ingestor.py — Ingestion Engine for Video Clipper.
Downloads YouTube & web video streams via yt-dlp, extracts metadata & subtitles,
and handles local file inputs.
"""

import os
import sys
import json
import logging
import subprocess
from typing import Dict, Any, Optional, List
from ..models.ffmpeg_utils import get_ffprobe_path

logger = logging.getLogger("MediaIngestor")


class MediaIngestor:
    """
    Handles ingestion of local and remote video files.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def probe_media(self, file_path: str) -> Dict[str, Any]:
        """Probes video metadata via ffprobe."""
        ffprobe = get_ffprobe_path()
        cmd = [
            ffprobe, "-v", "error",
            "-show_entries", "format=duration,size,bit_rate:stream=width,height,codec_name,r_frame_rate,codec_type",
            "-of", "json",
            file_path
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(res.stdout)
            video_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
            audio_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), {})
            return {
                "duration": float(data.get("format", {}).get("duration", 0.0)),
                "size_bytes": int(data.get("format", {}).get("size", 0)),
                "width": int(video_stream.get("width", 1920)),
                "height": int(video_stream.get("height", 1080)),
                "video_codec": video_stream.get("codec_name", "h264"),
                "audio_codec": audio_stream.get("codec_name", "aac")
            }
        except Exception as e:
            logger.warning(f"ffprobe failed on {file_path}: {e}")
            return {"duration": 60.0, "width": 1920, "height": 1080}

    def fetch_youtube_metadata(self, url: str) -> Dict[str, Any]:
        """Fetches video title, chapters, and description without downloading."""
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--extractor-args", "youtube:player_client=android",
            "--dump-json",
            "--skip-download",
            "--no-warnings",
            url
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            info = json.loads(res.stdout)
            return {
                "id": info.get("id"),
                "title": info.get("title", "Video Clip"),
                "description": info.get("description", ""),
                "duration": float(info.get("duration", 0)),
                "chapters": info.get("chapters", []) or [],
                "tags": info.get("tags", []) or [],
                "subtitles": list(info.get("subtitles", {}).keys()),
                "auto_subtitles": list(info.get("automatic_captions", {}).keys())
            }
        except Exception as e:
            logger.warning(f"Could not extract full YouTube metadata: {e}")
            return {"title": "YouTube Clip", "duration": 300.0, "chapters": []}

    def download_section(self, url: str, start_time: str, duration: float, out_filename: str = "clipped_raw.mp4") -> str:
        """
        Fast-downloads ONLY the requested section using yt-dlp section download,
        saving bandwidth and processing time.
        """
        target_path = os.path.join(self.output_dir, out_filename)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        end_time_sec = self._parse_timestamp_to_seconds(start_time) + duration
        end_time_str = self._format_seconds_to_timestamp(end_time_sec)

        section_spec = f"*{start_time}-{end_time_str}"
        logger.info(f"📥 Fast-downloading section {section_spec} from {url}...")

        from ..models.ffmpeg_utils import get_ffmpeg_path
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--ffmpeg-location", get_ffmpeg_path(),
            "--extractor-args", "youtube:player_client=android",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--download-sections", section_spec,
            "--force-keyframes-at-cuts",
            "-o", target_path,
            url
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if os.path.exists(target_path):
                return target_path
        except Exception as e:
            logger.warning(f"Section download failed ({e}), falling back to standard download...")

        # Fallback standard download
        return self.download_full(url, out_filename)

    def download_full(self, url: str, out_filename: str = "source_full.mp4") -> str:
        """Full download fallback."""
        target_path = os.path.join(self.output_dir, out_filename)
        from ..models.ffmpeg_utils import get_ffmpeg_path
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--ffmpeg-location", get_ffmpeg_path(),
            "--extractor-args", "youtube:player_client=android",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", target_path,
            url
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return target_path

    def download_subtitles(self, url: str) -> Optional[str]:
        """Downloads YouTube captions as SRT for synchronized kinetic typography."""
        sub_prefix = os.path.join(self.output_dir, "yt_subtitles")
        from ..models.ffmpeg_utils import get_ffmpeg_path
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--ffmpeg-location", get_ffmpeg_path(),
            "--extractor-args", "youtube:player_client=android",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--convert-subs", "srt",
            "--skip-download",
            "-o", sub_prefix,
            url
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            import glob
            cands = glob.glob(f"{sub_prefix}*.srt")
            if cands:
                return cands[0]
        except Exception as e:
            logger.info(f"No direct subtitles retrieved: {e}")
        return None

    def _parse_timestamp_to_seconds(self, ts: str) -> float:
        parts = ts.strip().split(":")
        if len(parts) == 3:
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:
            return float(parts[0]) * 60 + float(parts[1])
        return float(parts[0])

    def _format_seconds_to_timestamp(self, secs: float) -> str:
        h = int(secs // 3600)
        m = int((secs % 3600) // 60)
        s = int(secs % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
