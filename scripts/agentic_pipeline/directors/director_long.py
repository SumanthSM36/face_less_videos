"""
director_long.py — Agent Director for Longer Videos (16:9).
Directs multi-chapter documentaries, long-form educational deep dives, and serialized content.
"""

import os
import json
import logging
from typing import Dict, Any, List
from ..models.types import UserIntent
from ..subagents.agent_healer import AgentHealer

logger = logging.getLogger("DirectorLong")


class DirectorLong:
    """
    Executive Showrunner and Director for Horizontal Long-Form Videos (16:9).
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.healer = AgentHealer()

    def direct_long_video(self, intent: UserIntent) -> Dict[str, Any]:
        logger.info(f"🎥 [Director Long] Planning chaptered long-form production: '{intent.topic}'...")

        chapters = [
            {"chapter": 1, "title": "The Forgotten Genesis", "timestamp": "00:00", "duration": 120},
            {"chapter": 2, "title": "The Clash of Principles", "timestamp": "02:00", "duration": 180},
            {"chapter": 3, "title": "The Hidden Strategic Decisive Turn", "timestamp": "05:00", "duration": 180},
            {"chapter": 4, "title": "The Cosmic Climax & Legacy", "timestamp": "08:00", "duration": 120}
        ]

        report = {
            "status": "BLUEPRINT_READY",
            "topic": intent.topic,
            "aspect_ratio": "16:9 (1920x1080)",
            "estimated_duration_minutes": 10.0,
            "chapters": chapters,
            "b_roll_strategy": "Historical archival footage, 3D RenderMan reenactments, and semantic diagrams",
            "audio_strategy": "Normalized stereo dialogue (-14 LUFS) with dynamic orchestral accompaniment",
            "output_directory": self.output_dir
        }

        with open(os.path.join(self.output_dir, "long_form_production_blueprint.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        logger.info(f"✨ [Director Long] 4-chapter long-form blueprint generated for '{intent.topic}'.")
        return report
