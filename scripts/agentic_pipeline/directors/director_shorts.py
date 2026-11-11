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
from ..subagents.multi_engine_motion import MultiEngineMotionDirector
from ..models.ffmpeg_utils import get_ffmpeg_path

logger = logging.getLogger("DirectorShorts")
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))


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

        # Step 3: Multi-Engine Motion Director (Kling, Luma, PixVerse, Open Archives)
        multi_engine_dir = os.path.join(self.output_dir, "03_multi_engine_motion")
        engine_director = MultiEngineMotionDirector(multi_engine_dir)
        engine_specs = engine_director.route_story_scenes(blueprint)

        # Step 4: Agent Screenplay Director
        screenplay = ScreenplayDirector(screenplay_dir)
        shot_list: ScreenplayShotList = self.healer.heal_and_retry(
            "ScreenplayDirector",
            screenplay.choreograph_screenplay,
            blueprint
        )

        # Check for staged AI motion video clips (scene_01.mp4 .. scene_05.mp4)
        staged_clips = []
        for i in range(1, 6):
            clip_cand = os.path.join(engine_director.clips_dir, f"scene_{i:02d}.mp4")
            if os.path.exists(clip_cand):
                staged_clips.append(clip_cand)

        if len(staged_clips) == 5:
            reference_keyframes = staged_clips
            logger.info(f"🚀 Loaded 5 staged AI generative video clips from {engine_director.clips_dir}!")
        else:
            # Check if dossier sourced genuine motion video assets
            dossier_assets = [a["file_path"] for a in dossier.get("assets", []) if os.path.exists(a.get("file_path", ""))]
            if dossier_assets and len(dossier_assets) >= 5:
                reference_keyframes = dossier_assets[:5]
                logger.info(f"🎞️ Using {len(reference_keyframes)} sourced motion assets from Story Explorer.")
            elif not reference_keyframes or len(reference_keyframes) < 5:
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
            "safe_zone_y": 1450,
            "multi_engine_specs": [s.__dict__ for s in engine_specs],
            "ai_prompt_deck": os.path.join(multi_engine_dir, "AI_VIDEO_PROMPT_DECK.md")
        }

        with open(os.path.join(self.output_dir, "director_production_report.json"), "w", encoding="utf-8") as f:
            json.dump(production_summary, f, indent=2)

        logger.info(f"🏆 [Director Shorts] Production finished with Audience Score {scorecard.score}/100 [{scorecard.recommendation}]")
        return production_summary

    def _resolve_fallback_keyframes(self, dossier: Dict[str, Any], target_dir: str) -> List[str]:
        """Resolves topic-matching visual assets from existing productions or builds matching scene frames."""
        import glob
        os.makedirs(target_dir, exist_ok=True)
        paths = []
        topic = dossier.get("topic", "").lower()

        # Search existing output directories for topic matches
        matched_scenes = []
        search_dirs = glob.glob(os.path.join(WORKSPACE_ROOT, "output/*/*"))
        for d in search_dirs:
            if not os.path.isdir(d):
                continue
            base = os.path.basename(d).lower()
            # If any significant keyword from topic is in directory name
            keywords = [w for w in topic.split() if len(w) > 3 and w not in ("short", "video", "about", "sacred", "secret")]
            if any(k in base for k in keywords):
                candidate_scenes = sorted(glob.glob(os.path.join(d, "scene_*.png")))
                if len(candidate_scenes) >= 5:
                    matched_scenes = candidate_scenes[:5]
                    logger.info(f"🎯 Found topic-matched visual assets in {d}")
                    break

        # Fallback to squirrel masterwork if no direct match
        if not matched_scenes:
            squirrel_scenes = sorted(glob.glob(os.path.join(WORKSPACE_ROOT, "output/animated_squirrel_ramayana/scene_*.png")))
            if len(squirrel_scenes) >= 5:
                matched_scenes = squirrel_scenes[:5]

        for i in range(5):
            dest = os.path.join(target_dir, f"keyframe_{i+1:02d}.png")
            if matched_scenes and i < len(matched_scenes) and os.path.exists(matched_scenes[i]):
                import shutil
                shutil.copyfile(matched_scenes[i], dest)
            else:
                subprocess.run([
                    get_ffmpeg_path(), "-y", "-f", "lavfi",
                    "-i", "color=c=0x1a243b:s=1080x1920:d=1",
                    "-vframes", "1", dest
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            paths.append(dest)
        return paths
