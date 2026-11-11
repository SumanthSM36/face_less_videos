"""
director_clipper.py — Master Director for Video Clipping & Viral Repurposing.
Coordinates ingestion, viral hook detection, smart 9:16 vertical reframing,
kinetic captions, hook overlays, and safe-zone enforcement.
"""

import os
import sys
import json
import logging
import subprocess
from typing import Dict, Any, List, Optional

from ..models.types import UserIntent
from ..subagents.agent_healer import AgentHealer
from ..models.ffmpeg_utils import get_ffmpeg_path
from ..clipper.media_ingestor import MediaIngestor
from ..clipper.viral_moment_detector import ViralMomentDetector, ViralClipCandidate
from ..clipper.smart_reframer import SmartReframer
from ..clipper.caption_burner import ClipperCaptionBurner
from ..clipper.hook_overlay import HookOverlay

logger = logging.getLogger("DirectorClipper")


class DirectorClipper:
    """
    Autonomous Video Clipping Director.
    Extracts viral vertical shorts (1080x1920) from any long video file, YouTube URL, or web link.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.healer = AgentHealer()

        # Initialize specialized clipping subagents
        self.ingestor = MediaIngestor(os.path.join(output_dir, "01_ingestion"))
        self.detector = ViralMomentDetector(os.path.join(output_dir, "02_detection"))
        self.reframer = SmartReframer(os.path.join(output_dir, "03_reframer"))
        self.captioner = ClipperCaptionBurner(os.path.join(output_dir, "04_captions"))
        self.hook_overlay = HookOverlay(os.path.join(output_dir, "05_hooks"))

    def clip_long_video(self, intent: UserIntent) -> Dict[str, Any]:
        """
        Executes end-to-end viral clipping workflow.
        """
        source = intent.source_url or intent.source_file
        if not source:
            raise ValueError("No video source provided (requires source_url or source_file).")

        logger.info(f"✂️ [Director Clipper] Initiating viral clipping for: {source}")

        # Step 1: Media Ingestion & Metadata Extraction
        metadata = {}
        srt_path = None
        is_url = bool(intent.source_url)

        if is_url:
            logger.info("🌐 Fetching remote stream metadata & chapters...")
            metadata = self.ingestor.fetch_youtube_metadata(intent.source_url)
            srt_path = self.ingestor.download_subtitles(intent.source_url)
            media_path = None
        else:
            media_path = intent.source_file
            if not os.path.exists(media_path):
                raise FileNotFoundError(f"Local source video not found: {media_path}")
            metadata = self.ingestor.probe_media(media_path)
            metadata["title"] = os.path.splitext(os.path.basename(media_path))[0]

        # Step 2: Viral Moment Detection & Hook Selection
        user_start = intent.extra_instructions.get("start_time")
        target_duration = intent.target_duration or 45.0

        candidates = self.detector.detect_best_moments(
            metadata=metadata,
            media_path=media_path,
            srt_path=srt_path,
            user_start=user_start,
            target_duration=target_duration
        )
        selected_clip: ViralClipCandidate = candidates[0]
        logger.info(f"🏆 Selected viral clip: '{selected_clip.title}' from {selected_clip.start_time} ({selected_clip.duration}s)")

        # Step 3: Media Segment Sourcing
        raw_clip_path = os.path.join(self.output_dir, "raw_clip_segment.mp4")
        if is_url:
            # Fast-download only the needed section via yt-dlp
            downloaded = self.ingestor.download_section(
                url=intent.source_url,
                start_time=selected_clip.start_time,
                duration=selected_clip.duration,
                out_filename="raw_clip_segment.mp4"
            )
            raw_clip_path = downloaded
        else:
            # Local slice
            raw_clip_path = self._slice_local_video(
                media_path, selected_clip.start_time, selected_clip.duration, raw_clip_path
            )

        # Step 4: Smart Vertical 9:16 Reframing
        reframed_path = os.path.join(self.output_dir, "reframed_vertical_916.mp4")
        reframe_preset = intent.extra_instructions.get("reframe_preset", "blurred_backdrop")
        self.reframer.reframe_to_vertical(
            input_media=raw_clip_path,
            output_mp4=reframed_path,
            start_time="00:00:00" if is_url else selected_clip.start_time,
            duration=selected_clip.duration,
            preset=reframe_preset
        )

        # Step 5: Kinetic Subtitle Burning
        captioned_path = os.path.join(self.output_dir, "captioned_vertical.mp4")
        self.captioner.burn_subtitles_onto_clip(
            video_path=reframed_path,
            srt_path=srt_path,
            start_time_ts=selected_clip.start_time,
            clip_duration=selected_clip.duration,
            output_mp4=captioned_path
        )

        # Step 6: Viral Headline / Hook Overlay
        final_mp4 = os.path.join(self.output_dir, "final_clipped_short.mp4")
        header_text = intent.extra_instructions.get("header_title", selected_clip.title)
        self.hook_overlay.add_hook_header(
            input_video=captioned_path,
            header_text=header_text,
            output_video=final_mp4
        )

        # Step 7: Frame 0 Thumbnail Extraction
        thumb_path = os.path.join(self.output_dir, "final_clipped_short_thumb.jpg")
        self._extract_thumbnail(final_mp4, thumb_path)

        result = {
            "status": "COMPLETED",
            "title": selected_clip.title,
            "source": source,
            "final_video_path": final_mp4,
            "thumbnail_path": thumb_path,
            "start_time": selected_clip.start_time,
            "duration_seconds": selected_clip.duration,
            "virality_score": selected_clip.virality_score,
            "source_method": selected_clip.source_method,
            "reframe_preset": reframe_preset,
            "all_ranked_candidates": [c.__dict__ for c in candidates[:5]]
        }

        report_file = os.path.join(self.output_dir, "clipper_production_report.json")
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        logger.info(f"✨ [Director Clipper] Viral Short Ready -> {final_mp4} (Score {selected_clip.virality_score}/100)")
        return result

    def _slice_local_video(self, input_file: str, start_time: str, duration: float, output_file: str) -> str:
        ffmpeg = get_ffmpeg_path()
        cmd = [
            ffmpeg, "-y",
            "-ss", start_time,
            "-i", input_file,
            "-t", str(duration),
            "-c", "copy",
            output_file
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_file

    def _extract_thumbnail(self, video_path: str, thumb_path: str):
        ffmpeg = get_ffmpeg_path()
        cmd = [
            ffmpeg, "-y",
            "-ss", "00:00:01",
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            thumb_path
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
