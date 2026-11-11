"""
types.py — Strongly-typed schemas for Agentic Pipeline communication.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class TaskType(str, Enum):
    SHORTS = "shorts"
    LONG_FORM = "long_form"
    CLIPPING = "clipping"
    OTHER = "other"


class ProductionStyle(str, Enum):
    PIXAR_3D = "pixar_3d"
    DOCUMENTARY = "documentary"
    CINEMATIC_LORE = "cinematic_lore"
    DYNAMIC_MOTION = "dynamic_motion"


@dataclass
class UserIntent:
    raw_prompt: str
    task_type: TaskType
    topic: str
    target_duration: float
    style: ProductionStyle
    source_url: Optional[str] = None
    source_file: Optional[str] = None
    target_channel: Optional[str] = None
    extra_instructions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SourcedAsset:
    asset_id: str
    source_type: str  # wikimedia, nasa, archive_org, pexels, generated
    file_path: str
    description: str
    resolution: str
    license_type: str


@dataclass
class StoryScene:
    scene_number: int
    title: str
    visual_description: str
    narration_text: str
    duration_seconds: float
    emotional_beat: str


@dataclass
class StoryBlueprint:
    title: str
    hook: str
    scenes: List[StoryScene]
    infinite_loop_phrase: str
    facts_cited: List[str]
    target_duration: float


@dataclass
class CameraCut:
    cut_number: int
    scene_number: int
    camera_angle: str  # wide_crane, low_angle_tilt, hero_closeup, intimate_zoom, etc.
    motion_type: str  # ken_burns_zoom_in, upward_tilt, pan_right, macro_reveal
    start_time: float
    end_time: float
    safe_zone_y: int = 1450


@dataclass
class ScreenplayShotList:
    story_title: str
    cuts: List[CameraCut]
    total_cuts: int
    pacing_seconds_per_cut: float


@dataclass
class CharacterDesignSheet:
    character_name: str
    aesthetic_standard: str  # 3D Pixar RenderMan
    lighting_palette: str
    texture_details: str
    scene_prompts: Dict[int, str]


@dataclass
class AudioMasterResult:
    voice_path: str
    soundtrack_path: str
    mastered_voice_path: str
    speech_vtt_path: str
    kinetic_ass_path: str
    lufs_loudness: float


@dataclass
class RenderResult:
    video_path: str
    thumbnail_path: str
    duration_seconds: float
    resolution: str
    file_size_bytes: int
    fingerprint_applied: bool


@dataclass
class AudienceReviewScore:
    score: int  # 0 to 100
    hook_score: int  # /25
    pacing_score: int  # /20
    narrative_score: int  # /20
    subtitle_score: int  # /15
    audio_score: int  # /20
    strengths: List[str]
    friction_points: List[str]
    recommendation: str  # APPROVED or REVISE
    is_approved: bool


@dataclass
class HealingEvent:
    failing_agent: str
    error_type: str
    error_message: str
    diagnosis: str
    healing_action: str
    success: bool
