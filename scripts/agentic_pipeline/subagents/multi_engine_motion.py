"""
multi_engine_motion.py — Multi-Engine AI Video & Motion Director.
Routes scenes to their specialized visual generation engine:
1. Kling AI: Epic character action, warrior combat, chariots, and physical battle dynamics.
2. Luma Dream Machine: Grand cosmic vistas, divine revelations, floating elements, and 3D camera sweeps.
3. PixVerse: 3D Pixar/Disney cartoon character animation, emotional expressions, and stylized lore.
4. Open Video Archives: Real 30fps continuous video clips (NASA, Wikimedia, Archive.org).
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List
from enum import Enum
from dataclasses import dataclass, field
from ..models.types import StoryBlueprint, StoryScene

logger = logging.getLogger("MultiEngineMotion")


class EngineType(str, Enum):
    KLING = "kling_ai"
    LUMA = "luma_dream_machine"
    PIXVERSE = "pixverse_3d"
    OPEN_FOOTAGE = "open_video_archives"


@dataclass
class EnginePromptSpec:
    scene_number: int
    title: str
    engine: EngineType
    platform_name: str
    generation_prompt: str
    camera_movement: str
    duration_seconds: float
    aspect_ratio: str = "9:16 (1080x1920)"
    assigned_clip_path: str = ""


class MultiEngineMotionDirector:
    """
    Directs scene distribution across Kling AI, Luma Dream Machine, PixVerse, and Open Video Archives.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.prompts_dir = os.path.join(output_dir, "engine_prompts")
        self.clips_dir = os.path.join(output_dir, "staged_motion_clips")
        os.makedirs(self.prompts_dir, exist_ok=True)
        os.makedirs(self.clips_dir, exist_ok=True)

    def route_story_scenes(self, blueprint: StoryBlueprint) -> List[EnginePromptSpec]:
        """
        Analyzes narrative beats and assigns each scene to its optimal AI video engine.
        """
        logger.info(f"🎯 [Multi-Engine Director] Routing 5 scenes for '{blueprint.title}'...")
        specs: List[EnginePromptSpec] = []

        for scene in blueprint.scenes:
            engine, platform, cam = self._classify_scene_engine(scene, blueprint.title)
            prompt = self._craft_platform_prompt(scene, engine, blueprint.title)

            expected_clip = os.path.join(self.clips_dir, f"scene_{scene.scene_number:02d}_{engine.value}.mp4")

            spec = EnginePromptSpec(
                scene_number=scene.scene_number,
                title=scene.title,
                engine=engine,
                platform_name=platform,
                generation_prompt=prompt,
                camera_movement=cam,
                duration_seconds=scene.duration_seconds,
                assigned_clip_path=expected_clip if os.path.exists(expected_clip) else ""
            )
            specs.append(spec)

        manifest_path = os.path.join(self.output_dir, "multi_engine_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump([s.__dict__ for s in specs], f, indent=2)

        self._export_user_copy_guides(specs)
        logger.info(f"✨ [Multi-Engine Director] Route manifest locked and prompt guides generated -> {manifest_path}")
        return specs

    def _classify_scene_engine(self, scene: StoryScene, story_title: str) -> (EngineType, str, str):
        text = (scene.title + " " + scene.narration_text + " " + scene.visual_description + " " + story_title).lower()

        # 1. Physical Action, Chariots, Combat, Running, Horses -> KLING AI
        if any(w in text for w in ["chariot", "horse", "warrior", "battle", "fight", "arrow", "weapon", "karna", "arjuna", "running"]):
            return (
                EngineType.KLING,
                "Kling AI (klingai.com)",
                "Fast Tracking Shot with dynamic motion blur and physical character movement"
            )

        # 2. 3D Cartoon, Squirrel, Pip, Cute, Tender Emotional Devotion -> PIXVERSE
        if any(w in text for w in ["squirrel", "pip", "robot", "cartoon", "cute", "shabari", "tears", "tenderness"]):
            return (
                EngineType.PIXVERSE,
                "PixVerse (pixverse.ai)",
                "3D Pixar Cinematic Character Close-up with subtle facial emotional performance"
            )

        # 3. Cosmic Vistas, Divine Revelations, Time Freeze, Vishwaroopa, Ram Setu Floating Stones -> LUMA
        if any(w in text for w in ["cosmic", "time", "galaxy", "divine", "revelation", "krishna", "floating", "stardust", "temple", "light"]):
            return (
                EngineType.LUMA,
                "Luma Dream Machine (lumalabs.ai)",
                "Sweeping 3D Camera Orbit with volumetric god rays and floating celestial depth"
            )

        # Default: Luma for majestic establishing shots
        return (
            EngineType.LUMA,
            "Luma Dream Machine (lumalabs.ai)",
            "Cinematic Forward Crane Push with golden hour atmospheric lighting"
        )

    def _craft_platform_prompt(self, scene: StoryScene, engine: EngineType, story_title: str) -> str:
        base_desc = scene.visual_description

        if engine == EngineType.KLING:
            return (
                f"{base_desc}, 8k cinematic hyper-realistic physical motion, 30fps smooth running movement, "
                f"dynamic camera tracking, highly detailed armor and atmospheric dust, dramatic high-contrast lighting, vertical 9:16"
            )
        elif engine == EngineType.LUMA:
            return (
                f"Cinematic photorealistic 3D footage of {base_desc}, volumetric golden god rays, "
                f"floating mystical particles, slow majestic camera push, highly realistic scale and depth, vertical 9:16"
            )
        elif engine == EngineType.PIXVERSE:
            return (
                f"3D Pixar and Disney RenderMan animation style, {base_desc}, tactile velvety textures, "
                f"large expressive eyes, warm golden rim lighting, subtle fluid character breathing motion, vertical 9:16"
            )
        else:
            return f"Real 4k documentary motion footage of {base_desc}, continuous movement, vertical 9:16"

    def _export_user_copy_guides(self, specs: List[EnginePromptSpec]):
        """Generates easy one-click copy-paste prompt cards for the user."""
        guide_file = os.path.join(self.output_dir, "AI_VIDEO_PROMPT_DECK.md")
        lines = [
            "# 🎬 Multi-Engine AI Video Prompt Deck",
            "",
            "Use each specialized engine for its designated purpose to achieve maximum visual quality:\n"
        ]

        for s in specs:
            lines.extend([
                f"### Scene {s.scene_number}: {s.title}",
                f"- **Assigned Engine:** `{s.platform_name}`",
                f"- **Camera Movement:** {s.camera_movement}",
                f"- **Target Duration:** {s.duration_seconds:.1f}s (Vertical 9:16)",
                f"- **Copy-Paste Prompt:**",
                f"```text\n{s.generation_prompt}\n```",
                f"- **Clip Destination:** Drop the downloaded MP4 into:",
                f"  `{self.clips_dir}/scene_{s.scene_number:02d}.mp4`",
                ""
            ])

        with open(guide_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
