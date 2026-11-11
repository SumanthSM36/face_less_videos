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
        if user_start in ["auto", "None", "", "00:00:00"]:
            user_start = None

        target_duration = intent.target_duration or 40.0

        candidates = self.detector.detect_best_moments(
            metadata=metadata,
            media_path=media_path,
            srt_path=srt_path,
            user_start=user_start,
            target_duration=target_duration
        )

        num_clips = int(intent.extra_instructions.get("num_clips", 3))
        if user_start:
            num_clips = 1

        selected_candidates = candidates[:num_clips]
        reframe_preset = intent.extra_instructions.get("reframe_preset", "dynamic_angles")
        caption_preset = intent.extra_instructions.get("caption_preset", "hormozi_pop")

        logger.info(f"🏆 Selected {len(selected_candidates)} viral moments for multi-short batch generation (Preset: {reframe_preset}).")

        import re
        import shutil
        generated_shorts: List[Dict[str, Any]] = []

        for idx, clip in enumerate(selected_candidates, start=1):
            slug_title = re.sub(r"[^a-zA-Z0-9]+", "_", clip.title[:30]).strip("_").lower()
            short_slug = f"short_{idx:02d}_{slug_title}"
            short_dir = os.path.join(self.output_dir, short_slug)
            os.makedirs(short_dir, exist_ok=True)

            logger.info(f"🎬 [Director Clipper] Producing Short #{idx}/{len(selected_candidates)}: '{clip.title}' ({clip.start_time}, {clip.duration}s)...")

            # Step 3: Media Segment Sourcing
            raw_clip_path = os.path.join(short_dir, "raw_clip_segment.mp4")
            if is_url:
                raw_clip_path = self.ingestor.download_section(
                    url=intent.source_url,
                    start_time=clip.start_time,
                    duration=clip.duration,
                    out_filename=f"{short_slug}_raw.mp4"
                )
            else:
                raw_clip_path = self._slice_local_video(
                    media_path, clip.start_time, clip.duration, raw_clip_path
                )

            # Step 4: Smart Vertical 9:16 Reframing (Dynamic Angles)
            reframed_path = os.path.join(short_dir, "reframed_vertical_916.mp4")
            self.reframer.reframe_to_vertical(
                input_media=raw_clip_path,
                output_mp4=reframed_path,
                start_time="00:00:00" if is_url else clip.start_time,
                duration=clip.duration,
                preset=reframe_preset
            )

            # Step 5: Kinetic Subtitle Burning & Hook Headline Banner
            final_mp4 = os.path.join(short_dir, "final_clipped_short.mp4")
            header_text = clip.hook_phrase
            self.captioner.burn_subtitles_onto_clip(
                video_path=reframed_path,
                srt_path=srt_path,
                start_time_ts=clip.start_time,
                clip_duration=clip.duration,
                output_mp4=final_mp4,
                preset=caption_preset,
                header_title=header_text
            )

            # Step 6: Frame 0 Thumbnail Extraction
            thumb_path = os.path.join(short_dir, "final_clipped_short_thumb.jpg")
            self._extract_thumbnail(final_mp4, thumb_path)

            # Step 7: YouTube SEO Metadata Pack
            short_info = {
                "short_index": idx,
                "title": f"{clip.title.upper()} 😱 #shorts",
                "start_time": clip.start_time,
                "duration_seconds": clip.duration,
                "virality_score": clip.virality_score,
                "hook_header": header_text,
                "final_video_path": final_mp4,
                "thumbnail_path": thumb_path,
                "description": (
                    f"Watch this viral moment: {clip.title}!\n\n"
                    f"Follow for more viral clips & highlights.\n\n"
                    f"#shorts #viral #funny #trending"
                ),
                "tags": ["shorts", "viral", "highlights", "funny", "trending"]
            }

            with open(os.path.join(short_dir, "metadata.json"), "w", encoding="utf-8") as f:
                json.dump(short_info, f, indent=2)

            generated_shorts.append(short_info)

        # For backward compatibility, link the top short as the primary output
        primary_short = generated_shorts[0]
        top_final_mp4 = os.path.join(self.output_dir, "final_clipped_short.mp4")
        top_thumb = os.path.join(self.output_dir, "final_clipped_short_thumb.jpg")
        shutil.copyfile(primary_short["final_video_path"], top_final_mp4)
        shutil.copyfile(primary_short["thumbnail_path"], top_thumb)

        result = {
            "status": "COMPLETED",
            "total_shorts_generated": len(generated_shorts),
            "reframe_preset": reframe_preset,
            "caption_preset": caption_preset,
            "source": source,
            "primary_short": primary_short,
            "generated_shorts": generated_shorts,
            "final_video_path": top_final_mp4,
            "thumbnail_path": top_thumb,
            "all_ranked_candidates": [c.__dict__ for c in candidates[:8]]
        }

        report_file = os.path.join(self.output_dir, "batch_clipping_report.json")
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        logger.info(f"✨ [Director Clipper] Successfully produced {len(generated_shorts)} viral shorts! Master report -> {report_file}")
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
