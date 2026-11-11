"""
director_shorts.py — Agent Director for Short Videos.
Directs the complete vertical short-video production pipeline across all 9 specialized subagents.
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List
from ..models.types import UserIntent, StoryBlueprint, ScreenplayShotList, RenderResult, AudienceReviewScore
from ..subagents.story_explorer import StoryExplorer
from ..subagents.story_writer import StoryWriter
from ..subagents.screenplay_director import ScreenplayDirector
from ..subagents.animator import Animator
from ..subagents.script_writer import ScriptWriter
from ..subagents.voice_creator import VoiceCreator
from ..subagents.video_renderer import VideoRenderer
from ..subagents.audience_reviewer import AudienceReviewer
from ..subagents.agent_healer import AgentHealer
from ..models.ffmpeg_utils import get_ffmpeg_path

logger = logging.getLogger("DirectorShorts")


class DirectorShorts:
    """
    Executive Showrunner and Director for Vertical Short Videos (9:16).
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.healer = AgentHealer()

    def direct_short_video(self, intent: UserIntent, reference_keyframes: List[str] = None) -> Dict[str, Any]:
        logger.info(f"🎬 [Director Shorts] Initiating production: '{intent.topic}' (Target: {intent.target_duration}s)...")

        # Sub-directories
        explorer_dir = os.path.join(self.output_dir, "01_explorer")
        writer_dir = os.path.join(self.output_dir, "02_writer")
        screenplay_dir = os.path.join(self.output_dir, "03_screenplay")
        animator_dir = os.path.join(self.output_dir, "04_animator")
        script_dir = os.path.join(self.output_dir, "05_script")
        voice_dir = os.path.join(self.output_dir, "06_voice")
        render_dir = os.path.join(self.output_dir, "07_render")
        review_dir = os.path.join(self.output_dir, "08_review")

        # Step 1: Agent Story Explorer
        explorer = StoryExplorer(explorer_dir)
        dossier = self.healer.heal_and_retry(
            "StoryExplorer",
            explorer.explore_topic,
            intent.topic, count=5
        )

        # Step 2: Agent Story Writer
        writer = StoryWriter(writer_dir)
        blueprint: StoryBlueprint = self.healer.heal_and_retry(
            "StoryWriter",
            writer.write_story,
            dossier, target_duration=intent.target_duration
        )

        # Step 3: Agent Screenplay Director
        screenplay = ScreenplayDirector(screenplay_dir)
        shot_list: ScreenplayShotList = self.healer.heal_and_retry(
            "ScreenplayDirector",
            screenplay.choreograph_screenplay,
            blueprint
        )

        # Prepare 5 scene keyframes (use provided or fallback to curated masterwork assets)
        if not reference_keyframes or len(reference_keyframes) < 5:
            reference_keyframes = self._resolve_fallback_keyframes(dossier, animator_dir)

        # Step 4: Agent Animator (with Character Designer & Motion Maker)
        animator = Animator(animator_dir)
        motion_video_path = self.healer.heal_and_retry(
            "Animator",
            animator.produce_visual_animation,
            blueprint, shot_list, reference_keyframes
        )

        # Step 5: Agent Script Writer
        script_agent = ScriptWriter(script_dir)
        script_data = self.healer.heal_and_retry(
            "ScriptWriter",
            script_agent.write_dialogue_and_captions,
            blueprint
        )

        # Step 6: Agent Voice Creator (Neural TTS + Studio Mastering)
        voice_agent = VoiceCreator(voice_dir)
        audio_result = self.healer.heal_and_retry(
            "VoiceCreator",
            voice_agent.produce_mastered_audio,
            script_data["full_speech"], target_duration=intent.target_duration
        )

        # Step 7: Agent Video Renderer
        renderer = VideoRenderer(render_dir)
        final_mp4 = os.path.join(self.output_dir, "final_short.mp4")
        render_result: RenderResult = self.healer.heal_and_retry(
            "VideoRenderer",
            renderer.render_final_short,
            motion_video_path,
            audio_result.mastered_voice_path,
            script_data["ass_file"],
            final_mp4
        )

        # Step 8: Agent Audience Reviewer (Viewer Critique & Retention Scoring)
        reviewer = AudienceReviewer(review_dir)
        scorecard: AudienceReviewScore = reviewer.review_video(blueprint, shot_list, render_result)

        production_summary = {
            "status": "COMPLETED",
            "title": blueprint.title,
            "topic": intent.topic,
            "video_path": render_result.video_path,
            "thumbnail_path": render_result.thumbnail_path,
            "duration_seconds": render_result.duration_seconds,
            "audience_score": scorecard.score,
            "audience_verdict": scorecard.recommendation,
            "healing_events_count": len(self.healer.healing_history),
            "shot_list_cuts": shot_list.total_cuts,
            "safe_zone_y": 1450
        }

        with open(os.path.join(self.output_dir, "director_production_report.json"), "w", encoding="utf-8") as f:
            json.dump(production_summary, f, indent=2)

        logger.info(f"🏆 [Director Shorts] Production finished with Audience Score {scorecard.score}/100 [{scorecard.recommendation}]")
        return production_summary

    def _resolve_fallback_keyframes(self, dossier: Dict[str, Any], target_dir: str) -> List[str]:
        """Ensures 5 valid keyframes exist for the animation pipeline."""
        os.makedirs(target_dir, exist_ok=True)
        paths = []
        # Check if assets exist in earlier output directories
        sample_assets = [
            "/Users/sumanth/Downloads/New/output/epic_facts_10/short_01_urmila_slumber/scene_01.png",
            "/Users/sumanth/Downloads/New/output/epic_facts_10/short_01_urmila_slumber/scene_02.png",
            "/Users/sumanth/Downloads/New/output/epic_facts_10/short_01_urmila_slumber/scene_03.png",
            "/Users/sumanth/Downloads/New/output/epic_facts_10/short_01_urmila_slumber/scene_04.png",
            "/Users/sumanth/Downloads/New/output/epic_facts_10/short_01_urmila_slumber/scene_05.png"
        ]
        
        for i in range(5):
            dest = os.path.join(target_dir, f"keyframe_{i+1:02d}.png")
            if os.path.exists(sample_assets[i]):
                import shutil
                shutil.copyfile(sample_assets[i], dest)
            else:
                # Create a procedural solid 1080x1920 image via ffmpeg if none exists
                subprocess.run([
                    get_ffmpeg_path(), "-y", "-f", "lavfi",
                    "-i", f"color=c=0x1a243b:s=1080x1920:d=1",
                    "-vframes", "1", dest
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            paths.append(dest)
        return paths
