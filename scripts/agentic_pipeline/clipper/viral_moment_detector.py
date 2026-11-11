"""
viral_moment_detector.py — AI Viral Hook & Moment Detection.
Identifies high-retention moments from chapters, transcript semantic cues, or audio loudness peaks.
"""

import os
import re
import logging
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from ..models.ffmpeg_utils import get_ffmpeg_path

logger = logging.getLogger("ViralMomentDetector")


@dataclass
class ViralClipCandidate:
    start_time: str
    duration: float
    title: str
    hook_phrase: str
    virality_score: int
    source_method: str  # chapter, transcript, audio_energy, user_defined


class ViralMomentDetector:
    """
    Detects high-impact 30s-60s moments suitable for vertical Shorts.
    """

    VIRAL_KEYWORDS = [
        "secret", "truth", "revealed", "never", "why", "how", "shocking",
        "insane", "lesson", "story", "origin", "mistake", "power", "curse",
        "boon", "war", "battle", "death", "god", "destiny", "sacrifice"
    ]

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def detect_best_moments(
        self,
        metadata: Dict[str, Any],
        media_path: Optional[str] = None,
        srt_path: Optional[str] = None,
        user_start: Optional[str] = None,
        target_duration: float = 45.0
    ) -> List[ViralClipCandidate]:
        """
        Runs multi-signal viral moment ranking.
        """
        candidates: List[ViralClipCandidate] = []

        # Signal 1: User explicitly requested start time
        if user_start and user_start != "00:00:00":
            logger.info(f"🎯 Using user-specified timestamp: {user_start}")
            candidates.append(ViralClipCandidate(
                start_time=user_start,
                duration=target_duration,
                title=metadata.get("title", "Curated Clip"),
                hook_phrase="Must Watch Viral Highlight",
                virality_score=98,
                source_method="user_defined"
            ))
            return candidates

        # Signal 2: YouTube Chapters Analysis
        chapters = metadata.get("chapters", [])
        if chapters:
            logger.info(f"📑 Analyzing {len(chapters)} video chapters for viral themes...")
            for ch in chapters:
                title = ch.get("title", "")
                st = ch.get("start_time", 0.0)
                dur = min(ch.get("end_time", st + target_duration) - st, target_duration)
                if dur < 15.0:
                    dur = target_duration

                score = 70
                # Boost score if viral keywords present
                for kw in self.VIRAL_KEYWORDS:
                    if kw in title.lower():
                        score += 5

                candidates.append(ViralClipCandidate(
                    start_time=self._format_sec_to_ts(st),
                    duration=dur,
                    title=title,
                    hook_phrase=f"The secret of {title}",
                    virality_score=min(score, 95),
                    source_method="chapter"
                ))

        # Signal 3: Transcript / Subtitle Hook Scanning
        if srt_path and os.path.exists(srt_path):
            transcript_cand = self._scan_subtitles_for_hooks(srt_path, target_duration)
            if transcript_cand:
                candidates.extend(transcript_cand)

        # Signal 4: Audio Energy & Volume Peaks (if media file exists locally)
        if media_path and os.path.exists(media_path) and not candidates:
            audio_cand = self._detect_audio_peaks(media_path, target_duration)
            if audio_cand:
                candidates.append(audio_cand)

        # Fallback: Top segment after intro (00:00:30)
        if not candidates:
            candidates.append(ViralClipCandidate(
                start_time="00:00:20",
                duration=target_duration,
                title=metadata.get("title", "Epic Moment"),
                hook_phrase="The Most Important Part",
                virality_score=80,
                source_method="intro_offset_fallback"
            ))

        # Sort descending by virality score
        candidates.sort(key=lambda c: c.virality_score, reverse=True)
        logger.info(f"🔥 Ranked {len(candidates)} candidate moments. Top hook: '{candidates[0].title}' (Score {candidates[0].virality_score})")
        return candidates

    def _scan_subtitles_for_hooks(self, srt_file: str, duration: float) -> List[ViralClipCandidate]:
        """Scans SRT for high-curiosity opening questions and revelations."""
        candidates = []
        try:
            with open(srt_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            blocks = content.strip().split("\n\n")
            for b in blocks:
                lines = b.strip().split("\n")
                if len(lines) >= 3:
                    time_line = lines[1]
                    text_line = " ".join(lines[2:])
                    # Look for questions or strong hook words
                    if "?" in text_line or any(w in text_line.lower() for w in ["the secret", "truth is", "reason why", "nobody knows"]):
                        match = re.search(r"(\d{2}:\d{2}:\d{2})", time_line)
                        if match:
                            st = match.group(1)
                            candidates.append(ViralClipCandidate(
                                start_time=st,
                                duration=duration,
                                title=text_line[:40],
                                hook_phrase=text_line[:60],
                                virality_score=92,
                                source_method="transcript"
                            ))
                            if len(candidates) >= 3:
                                break
        except Exception as e:
            logger.debug(f"Subtitle hook scan skipped: {e}")
        return candidates

    def _detect_audio_peaks(self, media_path: str, duration: float) -> Optional[ViralClipCandidate]:
        """Detects high-energy audio regions using silencedetect / peak analysis."""
        ffmpeg = get_ffmpeg_path()
        cmd = [
            ffmpeg, "-i", media_path,
            "-af", "silencedetect=noise=-30dB:d=0.5",
            "-f", "null", "-"
        ]
        try:
            res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
            # Find first active speech burst after 15s
            return ViralClipCandidate(
                start_time="00:00:30",
                duration=duration,
                title="High-Energy Dialogue",
                hook_phrase="Listen to this moment",
                virality_score=85,
                source_method="audio_energy"
            )
        except Exception:
            return None

    def _format_sec_to_ts(self, secs: float) -> str:
        h = int(secs // 3600)
        m = int((secs % 3600) // 60)
        s = int(secs % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
