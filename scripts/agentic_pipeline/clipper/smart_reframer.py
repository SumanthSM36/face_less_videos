"""
smart_reframer.py — Smart 9:16 Vertical Reframing Engine.
Converts horizontal 16:9 videos to broadcast-grade vertical Shorts (1080x1920):
- Preset A: Cinematic Dynamic Blurred Ambient Backdrop (Podcast / Video Standard)
- Preset B: Dual-Speaker Stack (Split Screen)
- Preset C: Dynamic Centered Crop
"""

import os
import logging
import subprocess
from ..models.ffmpeg_utils import get_ffmpeg_path

logger = logging.getLogger("SmartReframer")


class SmartReframer:
    """
    Renders 9:16 vertical video from 16:9 horizontal sources.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def reframe_to_vertical(
        self,
        input_media: str,
        output_mp4: str,
        start_time: str,
        duration: float,
        preset: str = "blurred_backdrop"
    ) -> str:
        """
        Executes FFmpeg vertical reframing.
        """
        ffmpeg = get_ffmpeg_path()
        logger.info(f"📐 [SmartReframer] Reframing '{input_media}' ({start_time}, {duration}s) using preset '{preset}'...")

        if preset == "split_screen":
            # Dual-speaker / Interview stack
            vf = (
                "split=2[top][bottom];"
                "[top]crop=iw/2:ih:0:0,scale=1080:960[t_scaled];"
                "[bottom]crop=iw/2:ih:iw/2:0,scale=1080:960[b_scaled];"
                "[t_scaled][b_scaled]vstack=inputs=2[stacked];"
                "[stacked]eq=contrast=1.05:saturation=1.1,vignette=PI/4.5"
            )
        elif preset == "crop_center":
            # Center action crop
            vf = (
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "fps=30,"
                "eq=contrast=1.08:saturation=1.12,"
                "vignette=PI/4.5"
            )
        else:
            # Default: Cinematic Blurred Ambient Backdrop (Industry Standard)
            vf = (
                "split[original][copy];"
                "[copy]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:14,eq=brightness=-0.08:contrast=1.1[bg];"
                "[original]scale=1080:-1[fg];"
                "[bg][fg]overlay=(W-w)/2:(H-h)/2,"
                "fps=30"
            )

        cmd = [
            ffmpeg, "-y",
            "-ss", start_time,
            "-i", input_media,
            "-t", str(duration),
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "19",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "48000",
            output_mp4
        ]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            logger.error(f"Reframing failed: {res.stderr[-300:]}")
            raise RuntimeError(f"FFmpeg vertical reframing error: {res.stderr[-200:]}")

        logger.info(f"✨ [SmartReframer] Reframed to 1080x1920 vertical -> {output_mp4}")
        return output_mp4
