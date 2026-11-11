"""
hook_overlay.py — Viral Hook Header Overlay.
Renders high-CTR attention-grabbing header overlays in the safe upper vertical zone (Y=320px).
"""

import os
import logging
import subprocess
from ..models.ffmpeg_utils import get_ffmpeg_path

logger = logging.getLogger("HookOverlay")


class HookOverlay:
    """
    Renders clean, bold header text cards on vertical clips.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def add_hook_header(
        self,
        input_video: str,
        header_text: str,
        output_video: str
    ) -> str:
        """
        Adds a bold headline banner in the safe upper third of the vertical video.
        """
        if not header_text or len(header_text.strip()) < 3:
            import shutil
            shutil.copyfile(input_video, output_video)
            return output_video

        ffmpeg = get_ffmpeg_path()
        clean_text = header_text.upper().replace("'", "").replace(":", " -")[:45]

        # Drawtext filter positioned at Y=320 (Safe Zone: below 280px status bar)
        draw_filter = (
            f"drawtext=text='{clean_text}':"
            "fontsize=52:"
            "fontcolor=white:"
            "font=Arial Bold:"
            "box=1:boxcolor=black@0.65:boxborderw=18:"
            "x=(w-text_w)/2:"
            "y=320"
        )

        cmd = [
            ffmpeg, "-y",
            "-i", input_video,
            "-vf", draw_filter,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "19",
            "-c:a", "copy",
            output_video
        ]

        logger.info(f"🏷️ Adding viral hook banner: '{clean_text}'...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            logger.warning(f"Hook overlay failed ({res.stderr[-200:]}), skipping overlay.")
            import shutil
            shutil.copyfile(input_video, output_video)
            return output_video

        return output_video
