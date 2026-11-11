"""
clipper — Automated Video Clipping & Viral Repurposing Engine.
"""

from .media_ingestor import MediaIngestor
from .viral_moment_detector import ViralMomentDetector, ViralClipCandidate
from .smart_reframer import SmartReframer
from .caption_burner import ClipperCaptionBurner
from .hook_overlay import HookOverlay

__all__ = [
    "MediaIngestor",
    "ViralMomentDetector",
    "ViralClipCandidate",
    "SmartReframer",
    "ClipperCaptionBurner",
    "HookOverlay"
]
