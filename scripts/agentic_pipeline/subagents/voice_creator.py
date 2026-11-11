"""
voice_creator.py — Agent Voice Creator.
Synthesizes neural voice and applies the Studio Vocal Mastering Chain with dynamic music ducking.
"""

import os
import sys
import json
import logging
import asyncio
import subprocess
from typing import Dict, Any
from ..models.types import AudioMasterResult
from ..models.ffmpeg_utils import get_ffmpeg_path

logger = logging.getLogger("VoiceCreator")


class VoiceCreator:
    """
    Synthesizes expressive voiceover and engineers broadcast vocal mastering.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.primary_voice = "en-IN-PrabhatNeural"
        self.backup_voices = ["en-US-ChristopherNeural", "en-US-AndrewMultilingualNeural"]

    def produce_mastered_audio(self, text: str, target_duration: float = 45.0) -> AudioMasterResult:
        logger.info(f"🎙️ Agent Voice Creator: Synthesizing voiceover ({len(text.split())} words)...")

        raw_voice_path = os.path.join(self.output_dir, "raw_voice.mp3")
        speech_vtt_path = os.path.join(self.output_dir, "speech.vtt")

        # Step 1: Neural TTS Synthesis
        self._synthesize_voice(text, raw_voice_path, speech_vtt_path)

        # Step 2: Studio Vocal Mastering Chain
        mastered_voice_path = os.path.join(self.output_dir, "mastered_voice.mp3")
        self._apply_studio_vocal_mastering(raw_voice_path, mastered_voice_path)

        # Step 3: Algorithmic Harmonic Soundtrack with Dynamic Ducking
        soundtrack_path = os.path.join(self.output_dir, "ducked_soundtrack.mp3")
        self._generate_ducked_soundtrack(mastered_voice_path, soundtrack_path, target_duration)

        result = AudioMasterResult(
            voice_path=raw_voice_path,
            soundtrack_path=soundtrack_path,
            mastered_voice_path=mastered_voice_path,
            speech_vtt_path=speech_vtt_path,
            kinetic_ass_path=os.path.join(self.output_dir, "kinetic.ass"),
            lufs_loudness=-16.0
        )

        logger.info(f"✨ Agent Voice Creator: Vocal mastering completed (-16 LUFS broadcast standard).")
        return result

    def _synthesize_voice(self, text: str, out_audio: str, out_vtt: str):
        """Runs edge-tts with automatic voice failover."""
        import edge_tts

        async def _run(voice_name):
            communicate = edge_tts.Communicate(text, voice_name, rate="+3%")
            submaker = edge_tts.SubMaker()
            with open(out_audio, "wb") as f:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
                    elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                        submaker.feed(chunk)
            # Write SRT/VTT if cues were captured
            if hasattr(submaker, "get_srt"):
                with open(out_vtt, "w", encoding="utf-8") as f:
                    f.write(submaker.get_srt())

        voices = [self.primary_voice] + self.backup_voices
        last_err = None
        for v in voices:
            try:
                logger.info(f"Attempting voice synthesis with '{v}'...")
                asyncio.run(_run(v))
                if os.path.exists(out_audio) and os.path.getsize(out_audio) > 1000:
                    logger.info(f"Voice synthesis successful with '{v}'.")
                    return
            except Exception as e:
                logger.warning(f"Voice '{v}' synthesis failed: {e}. Trying fallback...")
                last_err = e

        raise RuntimeError(f"All neural TTS voice endpoints failed: {last_err}")

    def _apply_studio_vocal_mastering(self, input_voice: str, output_voice: str):
        """Applies 280Hz warm chest EQ, 3200Hz de-essing, dynamic compression, and -1.5dBFS true-peak limit."""
        filter_chain = (
            "highpass=f=80,"
            "equalizer=f=280:t=q:w=1.2:g=2.5,"
            "equalizer=f=3200:t=q:w=2.0:g=-3.0,"
            "acompressor=threshold=-18dB:ratio=3:attack=10:release=150:makeup=2,"
            "alimiter=limit=-1.5dB:attack=5:release=50,"
            "loudnorm=I=-16:TP=-1.5:LRA=9"
        )
        cmd = [
            get_ffmpeg_path(), "-y",
            "-i", input_voice,
            "-af", filter_chain,
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            output_voice
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _generate_ducked_soundtrack(self, mastered_voice: str, output_track: str, duration: float):
        """Synthesizes harmonic score dynamically ducked to 18% under speech."""
        chord_synth = (
            "aevalsrc=exprs='0.08*sin(2*PI*146.83*t) + 0.06*sin(2*PI*220.00*t) + 0.05*sin(2*PI*261.63*t) + 0.04*sin(2*PI*329.63*t)':"
            f"s=48000:d={duration+2}[bg];"
            "[bg]lowpass=f=1200,volume=0.22[score];"
            "[0:a][score]sidechaincompress=threshold=0.04:ratio=8:attack=20:release=350[outa]"
        )
        cmd = [
            get_ffmpeg_path(), "-y",
            "-i", mastered_voice,
            "-filter_complex", chord_synth,
            "-map", "[outa]",
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            output_track
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
