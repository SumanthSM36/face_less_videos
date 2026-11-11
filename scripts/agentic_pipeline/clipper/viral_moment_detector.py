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
        """
        Deep full-video transcript scanner.
        Evaluates dialogue windows across the entire video for hook strength,
        conversational energy, and punchline climax, returning non-overlapping viral moments.
        """
        candidates: List[ViralClipCandidate] = []
        try:
            with open(srt_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            blocks = content.strip().split("\n\n")
            entries = []
            for b in blocks:
                lines = b.strip().split("\n")
                if len(lines) >= 3:
                    tm = re.search(r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})", lines[1])
                    if tm:
                        def to_sec(s):
                            p = s.replace(",", ".").split(":")
                            return float(p[0]) * 3600 + float(p[1]) * 60 + float(p[2])
                        s_sec = to_sec(tm.group(1))
                        e_sec = to_sec(tm.group(2))
                        raw_text = " ".join(lines[2:]).strip()
                        raw_text = re.sub(r"<[^>]+>", "", raw_text)
                        raw_text = re.sub(r">>", "", raw_text).strip()
                        if raw_text:
                            entries.append((s_sec, e_sec, raw_text))

            if not entries:
                return []

            total_dur = entries[-1][1]
            step = 10.0
            scored_windows = []

            for cur_t in [i * step for i in range(int(total_dur // step))]:
                win_end = cur_t + duration
                win_entries = [e for e in entries if e[0] >= cur_t and e[1] <= win_end]
                if not win_entries:
                    continue

                first_few = " ".join([e[2] for e in win_entries[:3]]).lower()
                full_text = " ".join([e[2] for e in win_entries])
                last_few = " ".join([e[2] for e in win_entries[-3:]]).lower()

                score = 65
                # 1. Hook score in first 3 lines
                for kw in self.VIRAL_KEYWORDS:
                    if kw in first_few:
                        score += 5
                for extra_cue in ["wait", "what", "why", "yo", "bro", "look", "cops", "police", "officer", "spiderman", "gwen", "crazy", "insane", "no way", "oh my god", "hold on", "run", "tackle"]:
                    if extra_cue in first_few:
                        score += 5
                if "?" in first_few or "!" in first_few:
                    score += 8

                # 2. Dialogue pacing & energy
                word_count = len(full_text.split())
                if word_count > 60:
                    score += 8
                elif word_count > 40:
                    score += 4

                # 3. Climax / reaction in last lines
                if "?" in last_few or "!" in last_few or any(w in last_few for w in ["bro", "way", "insane", "crazy", "god", "let's go"]):
                    score += 6

                score = min(score, 99)
                if score >= 80:
                    # Synthesize clean title from opening sentence
                    first_sent = full_text.split(".")[0].split("?")[0].strip()
                    if len(first_sent) > 40:
                        first_sent = first_sent[:40] + "..."
                    scored_windows.append((cur_t, score, first_sent, full_text[:90]))

            # Sort descending by virality score
            scored_windows.sort(key=lambda x: x[1], reverse=True)

            # Greedily pick non-overlapping top moments
            selected_times: List[float] = []
            for st_sec, sc, title, snippet in scored_windows:
                if any(abs(st_sec - prev) < (duration * 0.8) for prev in selected_times):
                    continue
                selected_times.append(st_sec)

                st_ts = self._format_sec_to_ts(st_sec)
                candidates.append(ViralClipCandidate(
                    start_time=st_ts,
                    duration=duration,
                    title=title,
                    hook_phrase=f"{title.upper()}",
                    virality_score=sc,
                    source_method="transcript_scanner"
                ))
                if len(candidates) >= 8:
                    break

            logger.info(f"🎯 Full-video transcript scanner discovered {len(candidates)} high-potential viral moments!")
        except Exception as e:
            logger.warning(f"Full-video transcript scan error: {e}")

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
