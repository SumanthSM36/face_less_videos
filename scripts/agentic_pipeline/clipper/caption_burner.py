"""
caption_burner.py — Kinetic Typography & Subtitle Burning for Video Clipper.
Extracts, offsets, and burns high-contrast ASS kinetic captions in the Y=1450 safe zone.
"""

import os
import re
import logging
import subprocess
from typing import Optional, List
from ..models.ffmpeg_utils import get_ffmpeg_path

logger = logging.getLogger("ClipperCaptionBurner")


class ClipperCaptionBurner:
    """
    Handles subtitle parsing, timestamp offset, and burning onto vertical clips.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def burn_subtitles_onto_clip(
        self,
        video_path: str,
        srt_path: Optional[str],
        start_time_ts: str,
        clip_duration: float,
        output_mp4: str
    ) -> str:
        """
        Parses subtitles, creates offset ASS, and burns them onto the video.
        """
        ffmpeg = get_ffmpeg_path()
        ass_path = os.path.join(self.output_dir, "clip_subtitles.ass")

        has_subtitles = False
        if srt_path and os.path.exists(srt_path):
            has_subtitles = self._generate_offset_ass(srt_path, start_time_ts, clip_duration, ass_path)

        if not has_subtitles:
            logger.info("ℹ️ No subtitles to burn or subtitle offset empty; copying clean video.")
            import shutil
            shutil.copyfile(video_path, output_mp4)
            return output_mp4

        logger.info(f"🔥 Burning kinetic safe-zone subtitles onto {output_mp4}...")
        escaped_ass = ass_path.replace(":", "\\:").replace("'", "\\'")
        vf = f"ass='{escaped_ass}'"

        cmd = [
            ffmpeg, "-y",
            "-i", video_path,
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "19",
            "-c:a", "copy",
            output_mp4
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            logger.warning(f"ASS subtitle burning failed ({res.stderr[-200:]}), copying original clip...")
            import shutil
            shutil.copyfile(video_path, output_mp4)
            return output_mp4

        return output_mp4

    def _generate_offset_ass(
        self,
        srt_file: str,
        clip_start_ts: str,
        duration: float,
        out_ass: str
    ) -> bool:
        """
        Reads SRT, filters dialogue lines within [clip_start, clip_start + duration],
        offsets timestamps relative to 00:00:00, and formats into ASS format.
        """
        clip_start_sec = self._parse_ts_to_sec(clip_start_ts)
        clip_end_sec = clip_start_sec + duration

        ass_header = (
            "[Script Info]\n"
            "Title: Viral Clip Kinetic Subtitles\n"
            "ScriptType: v4.00+\n"
            "WrapStyle: 0\n"
            "PlayResX: 1080\n"
            "PlayResY: 1920\n"
            "ScaledBorderAndShadow: yes\n\n"
            "[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: KineticClipper,Impact,76,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,6,2,2,40,40,450,1\n\n"
            "[Events]\n"
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        )

        dialogue_lines: List[str] = []
        try:
            with open(srt_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            blocks = content.strip().split("\n\n")
            for b in blocks:
                lines = b.strip().split("\n")
                if len(lines) >= 3:
                    time_match = re.search(r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})", lines[1])
                    if time_match:
                        s_str, e_str = time_match.group(1), time_match.group(2)
                        s_sec = self._parse_srt_time(s_str)
                        e_sec = self._parse_srt_time(e_str)

                        # Check overlap with clip window
                        if e_sec > clip_start_sec and s_sec < clip_end_sec:
                            rel_start = max(0.0, s_sec - clip_start_sec)
                            rel_end = min(duration, e_sec - clip_start_sec)
                            text = " ".join(lines[2:]).strip()
                            text = re.sub(r"<[^>]+>", "", text)  # Strip HTML tags
                            if text and (rel_end - rel_start) > 0.2:
                                ass_s = self._format_ass_time(rel_start)
                                ass_e = self._format_ass_time(rel_end)
                                dialogue_lines.append(f"Dialogue: 0,{ass_s},{ass_e},KineticClipper,,0,0,0,,{text.upper()}")

            if not dialogue_lines:
                return False

            with open(out_ass, "w", encoding="utf-8") as f:
                f.write(ass_header + "\n".join(dialogue_lines) + "\n")

            logger.info(f"✨ Offset {len(dialogue_lines)} subtitle lines for clip window.")
            return True
        except Exception as e:
            logger.warning(f"Error parsing subtitles: {e}")
            return False

    def _parse_ts_to_sec(self, ts: str) -> float:
        parts = ts.strip().split(":")
        if len(parts) == 3:
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2:
            return float(parts[0]) * 60 + float(parts[1])
        return float(parts[0])

    def _parse_srt_time(self, srt_time: str) -> float:
        srt_time = srt_time.replace(",", ".")
        return self._parse_ts_to_sec(srt_time)

    def _format_ass_time(self, seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        cs = int(round((seconds - int(seconds)) * 100))
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"
