"""
story_writer.py — Agent Story Writer.
Refines explorer dossiers into a 5-scene emotional story structure with infinite loop hooks.
"""

import os
import json
import logging
from typing import Dict, Any, List
from ..models.types import StoryBlueprint, StoryScene

logger = logging.getLogger("StoryWriter")


class StoryWriter:
    """
    Constructs high-retention 5-scene narrative structures.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def write_story(self, explorer_dossier: Dict[str, Any], target_duration: float = 45.0) -> StoryBlueprint:
        topic = explorer_dossier.get("topic", "Epic Lore")
        facts = explorer_dossier.get("facts", [])
        focus_fact = explorer_dossier.get("recommended_focus", facts[0] if facts else topic)

        logger.info(f"✍️ Agent Story Writer: Drafting narrative for '{topic}'...")

        # Craft 5 scenes matching Senior Animation Director standards
        hook_text = f"Did you know the deepest secret of {topic}?"
        scenes = [
            StoryScene(
                scene_number=1,
                title="The Ancient Hook",
                visual_description=f"Wide cinematic shot revealing {focus_fact[:40]} with glowing atmospheric lighting.",
                narration_text=f"Have you ever wondered about the untold truth behind {topic}?",
                duration_seconds=8.0,
                emotional_beat="Curiosity & Awe"
            ),
            StoryScene(
                scene_number=2,
                title="The Unseen Challenge",
                visual_description="Low-angle upward tilt capturing the monumental obstacle and emotional tension.",
                narration_text="When duty demanded the ultimate sacrifice, an unspoken oath was forged in silence.",
                duration_seconds=9.0,
                emotional_beat="Tension & Devotion"
            ),
            StoryScene(
                scene_number=3,
                title="The Turning Point",
                visual_description="Golden hour volumetric lighting illuminating the decisive choice of righteousness.",
                narration_text="Beyond the reach of mortal understanding, divine grace touched every beating heart.",
                duration_seconds=9.0,
                emotional_beat="Revelation & Hope"
            ),
            StoryScene(
                scene_number=4,
                title="The Emotional Climax",
                visual_description="Intimate character close-up with teary glistening eyes expressing boundless courage.",
                narration_text="In that profound instant of unconditional love, destiny itself bowed to pure devotion.",
                duration_seconds=9.5,
                emotional_beat="Emotional Peak"
            ),
            StoryScene(
                scene_number=5,
                title="Cosmic Loop",
                visual_description="Luminous camera pull-back into stardust galaxy, seamlessly blending into opening frame.",
                narration_text="And this eternal sacrifice is why history still remembers the untold truth behind it.",
                duration_seconds=9.5,
                emotional_beat="Cosmic Transcendence"
            )
        ]

        infinite_loop = scenes[4].narration_text

        blueprint = StoryBlueprint(
            title=f"The Sacred Secret of {topic}",
            hook=scenes[0].narration_text,
            scenes=scenes,
            infinite_loop_phrase=infinite_loop,
            facts_cited=[focus_fact],
            target_duration=target_duration
        )

        blueprint_file = os.path.join(self.output_dir, "story_blueprint.json")
        with open(blueprint_file, "w", encoding="utf-8") as f:
            json.dump({
                "title": blueprint.title,
                "hook": blueprint.hook,
                "infinite_loop_phrase": blueprint.infinite_loop_phrase,
                "target_duration": blueprint.target_duration,
                "scenes": [s.__dict__ for s in blueprint.scenes]
            }, f, indent=2)

        logger.info(f"✨ Agent Story Writer: Blueprint '{blueprint.title}' created with 5-scene emotional arc.")
        return blueprint
