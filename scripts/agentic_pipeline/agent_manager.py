"""
agent_manager.py — Master Orchestrator & Intake Manager.
Identifies user interest and input, plans task distribution, and coordinates specialized Directors.
"""

import os
import sys
import json
import logging
from typing import Dict, Any, Optional
from .models.types import TaskType, ProductionStyle, UserIntent
from .directors.director_shorts import DirectorShorts
from .directors.director_long import DirectorLong
from .directors.director_clipper import DirectorClipper
from .subagents.agent_healer import AgentHealer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("AgentManager")


class AgentManager:
    """
    Top-Level Orchestrator of the Autonomous Video Studio.
    """

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.output_base = os.path.join(self.workspace_root, "output/agentic_studio")
        os.makedirs(self.output_base, exist_ok=True)
        self.healer = AgentHealer()

    def process_user_request(self, user_prompt: str, extra_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main intake entry point. Classifies intent, plans distribution, and dispatches to Directors.
        """
        logger.info(f"🧠 [Agent Manager] Received request: '{user_prompt}'")

        # Step 1: Intent Identification
        intent = self._identify_user_intent(user_prompt, extra_params or {})
        logger.info(f"📋 [Agent Manager] Intent Classified -> Task: {intent.task_type.value}, Topic: '{intent.topic}', Style: {intent.style.value}")

        # Create task-specific output workspace
        task_slug = intent.topic.lower().replace(" ", "_")[:30]
        task_dir = os.path.join(self.output_base, f"{intent.task_type.value}_{task_slug}")
        os.makedirs(task_dir, exist_ok=True)

        # Step 2: Plan Task Distribution & Route to Appropriate Director
        result = None
        if intent.task_type == TaskType.SHORTS:
            logger.info("➡️ Routing payload to: Agent Director for Short Videos")
            director = DirectorShorts(task_dir)
            result = director.direct_short_video(intent)

        elif intent.task_type == TaskType.LONG_FORM:
            logger.info("➡️ Routing payload to: Agent Director for Longer Videos")
            director = DirectorLong(task_dir)
            result = director.direct_long_video(intent)

        elif intent.task_type == TaskType.CLIPPING:
            logger.info("➡️ Routing payload to: Agent Director for Video Clipping")
            director = DirectorClipper(task_dir)
            result = director.clip_long_video(intent)

        else:
            logger.info("ℹ️ Task classified as general metadata/channel task.")
            result = {
                "status": "COMPLETED",
                "message": f"Processed general instruction for '{intent.topic}'",
                "intent": intent.__dict__
            }

        # Step 3: Compile Executive Production Summary
        summary = {
            "orchestrator": "Agent Manager v2.0",
            "user_prompt": user_prompt,
            "classified_intent": {
                "task_type": intent.task_type.value,
                "topic": intent.topic,
                "target_duration": intent.target_duration,
                "style": intent.style.value
            },
            "director_execution_result": result,
            "healer_status": {
                "active_guards": ["IPv4_DNS_Routing", "Neural_Voice_Fallback", "FFmpeg_Sanitization"],
                "total_healing_events": len(self.healer.healing_history)
            }
        }

        summary_file = os.path.join(task_dir, "master_orchestrator_summary.json")
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"🎉 [Agent Manager] Execution successfully finished. Summary logged -> {summary_file}")
        return summary

    def _identify_user_intent(self, prompt: str, params: Dict[str, Any]) -> UserIntent:
        p_low = prompt.lower()

        # Check for clipping / long video extraction first
        if "clip" in p_low or "youtube.com" in p_low or "youtu.be" in p_low or "extract" in p_low or "from long" in p_low:
            task_type = TaskType.CLIPPING
            # Detect URL if present
            url = params.get("source_url")
            if not url:
                for word in prompt.split():
                    if "http://" in word or "https://" in word:
                        url = word
                        break
            return UserIntent(
                raw_prompt=prompt,
                task_type=task_type,
                topic=params.get("topic", "Viral Video Highlights"),
                target_duration=params.get("duration", 45.0),
                style=ProductionStyle.DYNAMIC_MOTION,
                source_url=url,
                source_file=params.get("source_file"),
                extra_instructions=params
            )

        # Check for long-form / documentary
        if "long video" in p_low or "longer" in p_low or "documentary" in p_low or "chapter" in p_low or "10 minute" in p_low:
            return UserIntent(
                raw_prompt=prompt,
                task_type=TaskType.LONG_FORM,
                topic=self._extract_topic(prompt),
                target_duration=params.get("duration", 600.0),
                style=ProductionStyle.DOCUMENTARY,
                extra_instructions=params
            )

        # Default is Short Video (vertical 9:16)
        style = ProductionStyle.PIXAR_3D if "cartoon" in p_low or "animated" in p_low or "3d" in p_low else ProductionStyle.CINEMATIC_LORE
        return UserIntent(
            raw_prompt=prompt,
            task_type=TaskType.SHORTS,
            topic=self._extract_topic(prompt),
            target_duration=params.get("duration", 45.0),
            style=style,
            extra_instructions=params
        )

    def _extract_topic(self, prompt: str) -> str:
        clean = prompt.lower()
        for prefix in ["create short video on", "create a short video on", "create video on", "create short on", "create a short about", "create a video about", "make a video on", "make a video about", "create"]:
            if prefix in clean:
                clean = clean.split(prefix, 1)[1]
                break
        clean = clean.replace("shorts", "").replace("video", "").replace("facts", "").strip()
        if clean.startswith("on "):
            clean = clean[3:].strip()
        elif clean.startswith("about "):
            clean = clean[6:].strip()
        return clean.capitalize() if clean else "Ancient Indian Lore"
