"""
script_writer.py — Agent Script Writer.
Formats punchy kinetic dialogue (<12 words/sentence) and crafts ASS kinetic subtitle files.
"""

import os
import json
import logging
from typing import List, Dict, Any
from ..models.types import StoryBlueprint

logger = logging.getLogger("ScriptWriter")


class ScriptWriter:
    """
    Formats spoken dialogue and generates word-level kinetic ASS captions.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def write_dialogue_and_captions(self, blueprint: StoryBlueprint) -> Dict[str, Any]:
        logger.info(f"📝 Agent Script Writer: Structuring kinetic captions for '{blueprint.title}'...")

        full_speech = " ".join([s.narration_text for s in blueprint.scenes])

        # Enforce Rule 2: punchy sentences (<12 words)
        clean_lines = []
        for s in blueprint.scenes:
            words = s.narration_text.split()
            if len(words) > 12:
                # Split into two punchy lines
                mid = len(words) // 2
                clean_lines.append(" ".join(words[:mid]))
                clean_lines.append(" ".join(words[mid:]))
            else:
                clean_lines.append(s.narration_text)

        ass_file = os.path.join(self.output_dir, "kinetic.ass")
        self._generate_ass_subtitles(blueprint, ass_file)

        script_data = {
            "title": blueprint.title,
            "full_speech": full_speech,
            "clean_lines": clean_lines,
            "ass_file": ass_file,
            "safe_zone_y": 1450
        }

        with open(os.path.join(self.output_dir, "script_output.json"), "w", encoding="utf-8") as f:
            json.dump(script_data, f, indent=2)

        logger.info(f"✨ Agent Script Writer: Formatted ASS kinetic captions -> {ass_file}")
        return script_data

    def _generate_ass_subtitles(self, blueprint: StoryBlueprint, ass_path: str):
        """Generates standard Rule 3 ASS subtitles with Pixar Yellow & Outline=6."""
        ass_header = """[Script Info]
Title: Epic Lore Kinetic Short
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: PixarKinetic,Arial Black,72,&H0000FFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,6,2,2,40,40,450,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        current_time = 0.0
        events = []

        for scene in blueprint.scenes:
            words = scene.narration_text.split()
            # Split into 3-word bursts
            burst_size = 3
            bursts = [" ".join(words[i:i + burst_size]) for i in range(0, len(words), burst_size)]
            dur_per_burst = scene.duration_seconds / max(len(bursts), 1)

            for b in bursts:
                st = self._format_ass_time(current_time)
                et = self._format_ass_time(current_time + dur_per_burst)
                # Uppercase for viral retention
                clean_text = b.upper().replace(",", "").replace(".", "")
                events.append(f"Dialogue: 0,{st},{et},PixarKinetic,,0,0,0,,{clean_text}")
                current_time += dur_per_burst

        with open(ass_path, "w", encoding="utf-8") as f:
            f.write(ass_header + "\n".join(events) + "\n")

    def _format_ass_time(self, seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        cs = int(round((seconds - int(seconds)) * 100))
        return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"
