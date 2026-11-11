"""
animator.py — Agent Animator.
Master Visual Effects & 3D Animation Director. Manages Character Designer and Motion Maker.
"""

import os
import logging
from typing import List, Dict, Any
from .character_designer import CharacterDesigner
from .motion_maker import MotionMaker
from ..models.types import StoryBlueprint, ScreenplayShotList, CharacterDesignSheet

logger = logging.getLogger("Animator")


class Animator:
    """
    Coordinates character continuity and procedural motion synthesis.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.character_designer = CharacterDesigner(os.path.join(output_dir, "character_design"))
        self.motion_maker = MotionMaker(os.path.join(output_dir, "motion_studio"))

    def produce_visual_animation(self, blueprint: StoryBlueprint, shot_list: ScreenplayShotList, keyframe_images: List[str]) -> str:
        logger.info("🎬 Agent Animator: Supervising visual production & 3D style consistency...")

        # Step 1: Character Designer locks visual continuity
        design_sheet = self.character_designer.design_character(blueprint)

        # Step 2: Validate Anti-Blur Gate (Rule 8)
        self._validate_asset_resolution(keyframe_images)

        # Step 3: Motion Maker generates 10-cut 2.5D optical motion
        motion_sequence_path = self.motion_maker.assemble_motion_sequence(keyframe_images, shot_list)

        logger.info(f"✨ Agent Animator: Animation sequence completed -> {motion_sequence_path}")
        return motion_sequence_path

    def _validate_asset_resolution(self, images: List[str]):
        """Enforces Rule 8 (Anti-Blur Gate): verifies assets exist and are not empty."""
        for img in images:
            if not os.path.exists(img):
                raise FileNotFoundError(f"Anti-Blur Gate failed: Missing keyframe image '{img}'")
            size = os.path.getsize(img)
            if size < 5000:
                raise ValueError(f"Anti-Blur Gate failed: Degraded keyframe image size ({size} bytes) in '{img}'")
        logger.info(f"🛡️ Anti-Blur Gate: All {len(images)} keyframe assets verified.")
