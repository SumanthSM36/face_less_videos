"""
motion_maker.py — Agent Motion Maker.
Generates dynamic 2.5D parallax, Ken Burns zooms/pans, and procedural living motion.
"""

import os
import sys
import json
import logging
import subprocess
from typing import List, Dict, Any
from ..models.types import ScreenplayShotList, CameraCut
from ..models.ffmpeg_utils import get_ffmpeg_path

logger = logging.getLogger("MotionMaker")


class MotionMaker:
    """
    Produces dynamic living motion video clips from static keyframes using 2.5D camera choreographies.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_motion_clip(self, input_image: str, cut: CameraCut, output_clip_path: str) -> str:
        """
        Renders a single camera cut with smooth Ken Burns 2.5D motion.
        """
        duration = cut.end_time - cut.start_time
        fps = 30
        total_frames = int(duration * fps)

        # Build dynamic zoompan filter based on motion type
        m = cut.motion_type
        if "zoom_in" in m or "push" in m:
            zp = f"zoompan=z='min(zoom+0.0015,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1080x1920:fps={fps}"
        elif "zoom_out" in m or "pullback" in m:
            zp = f"zoompan=z='max(1.25-0.0015*on,1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1080x1920:fps={fps}"
        elif "upward" in m:
            zp = f"zoompan=z='1.15':x='iw/2-(iw/zoom/2)':y='ih-(ih/zoom)-(on*0.8)':d={total_frames}:s=1080x1920:fps={fps}"
        else:
            zp = f"zoompan=z='min(zoom+0.001,1.18)':x='iw/2-(iw/zoom/2)+(on*0.5)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1080x1920:fps={fps}"

        cmd = [
            get_ffmpeg_path(), "-y",
            "-loop", "1",
            "-i", input_image,
            "-vf", f"{zp},format=yuv420p",
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            output_clip_path
        ]

        logger.debug(f"Rendering cut {cut.cut_number} ({cut.camera_angle}): {zp[:60]}...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            logger.error(f"Motion cut render failed: {res.stderr[-300:]}")
            raise RuntimeError(f"FFmpeg motion clip render error: {res.stderr[-200:]}")

        return output_clip_path

    def assemble_motion_sequence(self, scene_images: List[str], shot_list: ScreenplayShotList) -> str:
        """
        Creates all 10 cuts and stitches them into an assembled dynamic motion MP4.
        """
        logger.info(f"🎞️ Agent Motion Maker: Synthesizing 10-cut 2.5D living motion sequence...")
        cuts_dir = os.path.join(self.output_dir, "motion_cuts")
        os.makedirs(cuts_dir, exist_ok=True)

        clip_paths = []
        for cut in shot_list.cuts:
            # Pick scene image (scene_number is 1-indexed)
            img_idx = min(cut.scene_number - 1, len(scene_images) - 1)
            img_path = scene_images[img_idx]
            out_clip = os.path.join(cuts_dir, f"cut_{cut.cut_number:02d}.mp4")
            self.generate_motion_clip(img_path, cut, out_clip)
            clip_paths.append(out_clip)

        # Concatenate all cuts
        concat_list = os.path.join(self.output_dir, "cuts_concat.txt")
        with open(concat_list, "w") as f:
            for cp in clip_paths:
                f.write(f"file '{cp}'\n")

        motion_video_path = os.path.join(self.output_dir, "assembled_motion_sequence.mp4")
        concat_cmd = [
            get_ffmpeg_path(), "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_list,
            "-c", "copy",
            motion_video_path
        ]
        subprocess.run(concat_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"✨ Agent Motion Maker: 10 cuts assembled into {motion_video_path}")
        return motion_video_path
