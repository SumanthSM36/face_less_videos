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
        elif preset == "dynamic_angles":
            # Industry-leading Dynamic Angle Switching (Alternates Wide <-> Hero Punch-in Zoom every 3.5s)
            vf = (
                "split=4[v_bg1][v_fg1][v_bg2][v_fg2];"
                "[v_bg1]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:14,eq=brightness=-0.08:contrast=1.1[bg1];"
                "[v_fg1]scale=1080:-1[wide_fg];"
                "[bg1][wide_fg]overlay=(W-w)/2:(H-h)/2[wide];"
                "[v_bg2]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:14,eq=brightness=-0.08:contrast=1.1[bg2];"
                "[v_fg2]scale=1458:-1[zoom_fg];"
                "[bg2][zoom_fg]overlay=(W-w)/2:(H-h)/2[punchin];"
                "[wide][punchin]overlay=0:0:enable='gte(mod(t,7),3.5)'[stacked];"
                "[stacked]eq=contrast=1.06:saturation=1.12,vignette=PI/4.5,fps=30"
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
