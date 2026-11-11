"""
character_designer.py — Agent Character Designer.
Enforces character continuity, 3D Pixar RenderMan lighting palettes, tactile materials, and style sheets.
"""

import os
import json
import logging
from typing import Dict, Any
from ..models.types import CharacterDesignSheet, StoryBlueprint

logger = logging.getLogger("CharacterDesigner")


class CharacterDesigner:
    """
    Guarantees character visual consistency and RenderMan 3D Pixar aesthetics.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def design_character(self, blueprint: StoryBlueprint) -> CharacterDesignSheet:
        logger.info(f"🎨 Agent Character Designer: Crafting style guide for '{blueprint.title}'...")

        title = blueprint.title
        char_name = "Epic Protagonist"
        if "shabari" in title.lower():
            char_name = "Devoted Shabari"
        elif "urmila" in title.lower():
            char_name = "Princess Urmila"
        elif "jatayu" in title.lower():
            char_name = "Noble Jatayu"
        elif "karna" in title.lower():
            char_name = "Danaveera Karna"
        elif "bhishma" in title.lower():
            char_name = "Pitamaha Bhishma"
        elif "arjuna" in title.lower():
            char_name = "Warrior Arjuna"

        sheet = CharacterDesignSheet(
            character_name=char_name,
            aesthetic_standard="3D Pixar / Disney RenderMan Cinematic Standard",
            lighting_palette="Warm golden hour volumetric rays, gentle amber rim light, soft global illumination",
            texture_details="Subsurface scattering on skin, tactile velvet fabrics, intricate Vedic jewelry with photorealistic brass reflection",
            scene_prompts={
                1: f"3D Pixar render of {char_name}, wide panoramic establishing scene, atmospheric mist, volumetric sunlight, 8k crisp details.",
                2: f"3D Pixar close-up of {char_name}, dramatic shadow contrasts, determined eyes, tactile textures, cinematic depth of field.",
                3: f"3D Pixar spiritual encounter, golden radiance enveloping {char_name}, divine aura, sparkling stardust particles.",
                4: f"3D Pixar emotional macro close-up of {char_name}, glistening tears of pure devotion, warm open palms, intimate RenderMan lighting.",
                5: f"3D Pixar cosmic ascension, stardust galaxy swirling around {char_name}, luminous transcendental glow, infinite loop horizon."
            }
        )

        sheet_file = os.path.join(self.output_dir, "character_design_sheet.json")
        with open(sheet_file, "w", encoding="utf-8") as f:
            json.dump(sheet.__dict__, f, indent=2)

        logger.info(f"✨ Agent Character Designer: Design sheet locked for '{char_name}' with 5 scene visual prompts.")
        return sheet
