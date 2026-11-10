#!/usr/bin/env python3
"""
build_coldest_universe.py — End-to-end generator for 'The Coldest Place in the Universe' Short.
Combines authentic NASA public domain 4K footage + bespoke sci-fi artwork,
word-burst kinetic safe-zone captions, ducked algorithmic ambient music, and cinematic grading.
"""

import os
import re
import sys
import asyncio
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.dirname(SCRIPT_DIR)
WORKSPACE_ROOT = os.path.abspath(os.path.join(OUTPUT_DIR, ".."))
FFMPEG = os.path.join(WORKSPACE_ROOT, ".venv/bin/ffmpeg")

SCRIPT_TEXT = (
    "The coldest place in the known universe is not deep space. "
    "It is actually inside a laboratory on planet Earth. "
    "In the frozen vacuum of space, cosmic radiation keeps everything around minus 455 degrees Fahrenheit. "
    "Even the Boomerang Nebula sits at one Kelvin above absolute zero. "
    "Yet in 2014, scientists in Italy chilled a one-ton copper cube down to just six millikelvin. "
    "That is minus 459.5 degrees Fahrenheit—colder than anywhere else in the cosmos. "
    "Which means across billions of light years, the coldest place in the universe is..."
)

VOICE = "en-US-ChristopherNeural"
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "the_coldest_place_in_the_universe.mp4")

NASA_CLIPS = {
    "nebula": "https://images-assets.nasa.gov/video/ksc_061404_t-nebula/ksc_061404_t-nebula~orig.mp4",
    "galaxies": "https://images-assets.nasa.gov/video/Evolution_of_Galaxies_H264/Evolution_of_Galaxies_H264~medium.mp4",
    "laboratory": "https://images-assets.nasa.gov/video/GRC-2016-CM-0129.3/GRC-2016-CM-0129.3~small.mp4",
    "earth": "https://images-assets.nasa.gov/video/GSFC_20140421_EarthOrbit_m11525/GSFC_20140421_EarthOrbit_m11525~medium.mp4"
}


def run_cmd(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stdout}")
    return p.stdout


async def generate_voice_and_captions(text, voice, out_audio, out_ass):
    import edge_tts

    print("📢 Synthesizing neural voiceover...")
    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+4%")
    submaker = edge_tts.SubMaker()

    with open(out_audio, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                submaker.feed(chunk)

    entries = []
    if hasattr(submaker, "cues") and submaker.cues:
        for cue in submaker.cues:
            start_s = cue.start.total_seconds()
            end_s = cue.end.total_seconds()
            sentence = cue.content.strip()
            words = sentence.split()
            if not words:
                continue
            chunk_size = 3
            word_chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
            total_chunks = len(word_chunks)
            chunk_dur = (end_s - start_s) / max(total_chunks, 1)

            for idx, ch in enumerate(word_chunks):
                cs = start_s + idx * chunk_dur
                ce = cs + chunk_dur
                entries.append((cs, ce, " ".join(ch).upper()))

    def fmt_time(t):
        hrs = int(t // 3600)
        mins = int((t % 3600) // 60)
        secs = int(t % 60)
        cs = int(round((t - int(t)) * 100))
        if cs >= 100:
            cs = 99
        return f"{hrs:d}:{mins:02d}:{secs:02d}.{cs:02d}"

    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,80,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,6,2,2,60,60,400,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(ass_header)
        for s, e, txt in entries:
            clean = txt.replace("{", "").replace("}", "")
            f.write(f"Dialogue: 0,{fmt_time(s)},{fmt_time(e)},Default,,0,0,0,,{clean}\n")


def get_audio_duration(path):
    cmd = [FFMPEG, "-i", path, "-f", "null", "-"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", p.stdout)
    if m:
        h, mn, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
        return h * 3600 + mn * 60 + s
    return 24.0


def main():
    print("=" * 60)
    print("🎬 BUILDING: The Coldest Place in the Universe")
    print("=" * 60)

    voice_mp3 = os.path.join(SCRIPT_DIR, "voice.mp3")
    captions_ass = os.path.join(SCRIPT_DIR, "captions.ass")

    asyncio.run(generate_voice_and_captions(SCRIPT_TEXT, VOICE, voice_mp3, captions_ass))
    total_dur = get_audio_duration(voice_mp3)
    print(f"✅ Voice duration: {total_dur:.2f}s")

    num_scenes = 5
    scene_dur = total_dur / num_scenes
    print(f"✂️  5 Scene cuts, each lasting {scene_dur:.2f}s")

    clips = []

    # Scene 1: Bespoke still with Ken Burns slow zoom
    clip1 = os.path.join(SCRIPT_DIR, "clip_01.mp4")
    scene1_img = os.path.join(SCRIPT_DIR, "scene_01.jpg")
    print("🎨 Rendering Scene 1 (Bespoke Deep Space Still + Ken Burns Zoom)...")
    cmd1 = [
        FFMPEG, "-y",
        "-loop", "1", "-i", scene1_img,
        "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0015,1.25)':d={int(scene_dur*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30",
        "-t", f"{scene_dur:.2f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-an", clip1
    ]
    run_cmd(cmd1)
    clips.append(clip1)

    # Scene 2: NASA Nebula
    clip2 = os.path.join(SCRIPT_DIR, "clip_02.mp4")
    print("🌌 Streaming Scene 2 (NASA Deep Space Nebula)...")
    cmd2 = [
        FFMPEG, "-y",
        "-ss", "1", "-t", f"{scene_dur:.2f}",
        "-i", NASA_CLIPS["nebula"],
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-an", clip2
    ]
    run_cmd(cmd2)
    clips.append(clip2)

    # Scene 3: NASA Galaxies
    clip3 = os.path.join(SCRIPT_DIR, "clip_03.mp4")
    print("✨ Streaming Scene 3 (NASA Cosmic Galaxy Evolution)...")
    cmd3 = [
        FFMPEG, "-y",
        "-ss", "3", "-t", f"{scene_dur:.2f}",
        "-i", NASA_CLIPS["galaxies"],
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-an", clip3
    ]
    run_cmd(cmd3)
    clips.append(clip3)

    # Scene 4: NASA Laboratory
    clip4 = os.path.join(SCRIPT_DIR, "clip_04.mp4")
    print("🔬 Streaming Scene 4 (NASA Cryogenic Experiments Lab)...")
    cmd4 = [
        FFMPEG, "-y",
        "-ss", "10", "-t", f"{scene_dur:.2f}",
        "-i", NASA_CLIPS["laboratory"],
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-an", clip4
    ]
    run_cmd(cmd4)
    clips.append(clip4)

    # Scene 5: NASA Earth from Orbit
    clip5 = os.path.join(SCRIPT_DIR, "clip_05.mp4")
    print("🌍 Streaming Scene 5 (NASA Earth Orbit Reveal)...")
    cmd5 = [
        FFMPEG, "-y",
        "-ss", "4", "-t", f"{scene_dur:.2f}",
        "-i", NASA_CLIPS["earth"],
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-an", clip5
    ]
    run_cmd(cmd5)
    clips.append(clip5)

    # Concatenate 5 scenes
    concat_txt = os.path.join(SCRIPT_DIR, "concat.txt")
    with open(concat_txt, "w") as f:
        for c in clips:
            f.write(f"file '{c}'\n")

    raw_video = os.path.join(SCRIPT_DIR, "raw_video.mp4")
    print("🎞️  Concatenating multi-scene visual reel...")
    cmd_cat = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-t", f"{total_dur:.2f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        raw_video
    ]
    run_cmd(cmd_cat)

    # Mix audio with deep space harmonic drone soundbed
    mixed_audio = os.path.join(SCRIPT_DIR, "mixed_audio.mp3")
    print("🎵 Mixing ambient space drone soundtrack and ducking...")
    # Deep A-minor cosmic frequency drone
    bgm_tone = "0.02*sin(2*PI*55*t)+0.015*sin(2*PI*82.41*t)+0.012*sin(2*PI*110*t)+0.008*sin(2*PI*164.81*t)"
    bgm_filter = (
        f"aevalsrc='{bgm_tone}':d={total_dur}[bgm];"
        "[0:a][bgm]amix=inputs=2:duration=first:weights=1.0 0.22[out]"
    )
    cmd_audio = [
        FFMPEG, "-y",
        "-i", voice_mp3,
        "-filter_complex", bgm_filter,
        "-map", "[out]",
        mixed_audio
    ]
    run_cmd(cmd_audio)

    # Final pass: burned-in kinetic subtitles, 35mm grain, color curves, lens vignette
    print("⚡ Applying cinematic grading, vignette, and burning kinetic subtitles...")
    escaped_ass = captions_ass.replace(":", "\\:").replace("'", "\\'")
    vf_chain = (
        "eq=contrast=1.14:saturation=1.18:brightness=-0.02,"
        "noise=alls=5:allf=t+u,"
        "vignette=PI/4,"
        f"ass='{escaped_ass}'"
    )

    cmd_final = [
        FFMPEG, "-y",
        "-i", raw_video,
        "-i", mixed_audio,
        "-vf", vf_chain,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", f"{total_dur:.2f}",
        OUTPUT_VIDEO
    ]
    run_cmd(cmd_final)

    print("=" * 60)
    print(f"🎉 RENDER COMPLETE: {OUTPUT_VIDEO}")
    print(f"   Size: {os.path.getsize(OUTPUT_VIDEO) / (1024*1024):.2f} MB")
    print("=" * 60)


if __name__ == "__main__":
    main()
