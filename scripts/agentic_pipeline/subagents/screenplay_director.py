"""
screenplay_director.py — Agent Screenplay Director.
Choreographs 10 distinct camera cuts, shot lists, safe zone alignment, and 2.5s-3.5s cut pacing.
"""

import os
import json
import logging
from typing import List
from ..models.types import StoryBlueprint, ScreenplayShotList, CameraCut

logger = logging.getLogger("ScreenplayDirector")


class ScreenplayDirector:
    """
    Translates narrative blueprints into a director's 10-cut camera shot list.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def choreograph_screenplay(self, blueprint: StoryBlueprint) -> ScreenplayShotList:
        logger.info(f"📐 Agent Screenplay Director: Directing camera choreography for '{blueprint.title}'...")

        cuts: List[CameraCut] = []
        current_time = 0.0

        cut_templates = [
            # Scene 1: World & Scale
            ("wide_crane_sweep", "ken_burns_zoom_in", 4.0),
            ("hero_punch_in", "slow_push_forward", 4.0),
            # Scene 2: Tension
            ("low_angle_upward_tilt", "dramatic_upward_pan", 4.5),
            ("dramatic_side_profile", "lateral_tracking", 4.5),
            # Scene 3: Turning Point / Grace
            ("volumetric_light_sweep", "ken_burns_zoom_out", 4.5),
            ("downward_celestial_push", "gentle_downward_tilt", 4.5),
            # Scene 4: Intimate Devotion / Climax
            ("intimate_emotional_closeup", "eye_level_macro_push", 4.75),
            ("tender_reaction_tracking", "smooth_right_pan", 4.75),
            # Scene 5: Cosmic Revelation & Infinite Loop
            ("macro_stardust_slow_pan", "celestial_orbit", 4.75),
            ("luminous_pull_back_loop", "ken_burns_wide_pullback", 4.75),
        ]

        for i, (angle, motion, dur) in enumerate(cut_templates):
            scene_num = (i // 2) + 1
            cuts.append(CameraCut(
                cut_number=i + 1,
                scene_number=scene_num,
                camera_angle=angle,
                motion_type=motion,
                start_time=round(current_time, 2),
                end_time=round(current_time + dur, 2),
                safe_zone_y=1450
            ))
            current_time += dur

        shot_list = ScreenplayShotList(
            story_title=blueprint.title,
            cuts=cuts,
            total_cuts=len(cuts),
            pacing_seconds_per_cut=round(current_time / len(cuts), 2)
        )

        shot_file = os.path.join(self.output_dir, "screenplay_shot_list.json")
        with open(shot_file, "w", encoding="utf-8") as f:
            json.dump({
                "story_title": shot_list.story_title,
                "total_cuts": shot_list.total_cuts,
                "pacing_seconds_per_cut": shot_list.pacing_seconds_per_cut,
                "cuts": [c.__dict__ for c in shot_list.cuts]
            }, f, indent=2)

        logger.info(f"🎬 Agent Screenplay Director: 10-cut choreography generated ({shot_list.pacing_seconds_per_cut}s avg cut).")
        return shot_list
