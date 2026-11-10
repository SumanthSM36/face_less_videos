#!/usr/bin/env python3
"""
generate_short.py — Complete, free, local faceless short video generator.
No paid APIs, no MCP servers. Uses edge-tts, FFmpeg, and optional Pollinations AI images.
"""

import argparse
import asyncio
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from connectors.stock_connector import fetch_open_stock_video
WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../.."))
VENV_DIR = os.path.join(WORKSPACE_ROOT, ".venv")
FFMPEG_EXE = os.path.join(VENV_DIR, "bin/ffmpeg")

if not os.path.exists(FFMPEG_EXE):
    FFMPEG_EXE = "ffmpeg"


GENRE_PROFILES = {
    "mystery": {
        "voice": "en-US-AndrewMultilingualNeural",
        "bgm": "0.025*sin(2*PI*98*t)+0.02*sin(2*PI*123.47*t)+0.015*sin(2*PI*146.83*t)",
        "color_eq": "eq=contrast=1.18:saturation=0.95:brightness=-0.04",
        "sub_color": "&H00FFFF00&",
        "prompt_suffix": "dark moody suspense cinematic atmosphere dramatic shadows photorealistic"
    },
    "scifi": {
        "voice": "en-US-AndrewMultilingualNeural",
        "bgm": "0.022*sin(2*PI*110*t)+0.018*sin(2*PI*164.81*t)+0.015*sin(2*PI*220*t)",
        "color_eq": "eq=contrast=1.15:saturation=1.25:brightness=-0.02",
        "sub_color": "&H00FFFF00&",
        "prompt_suffix": "epic science fiction futuristic cosmic nebula stars 8k cinematic"
    },
    "mythology": {
        "voice": "en-IN-PrabhatNeural",
        "bgm": "0.02*sin(2*PI*130.81*t)+0.018*sin(2*PI*164.81*t)+0.015*sin(2*PI*196*t)",
        "color_eq": "eq=contrast=1.12:saturation=1.20:brightness=-0.01",
        "sub_color": "&H0000FFFF&",
        "prompt_suffix": "ancient mythology magnificent epic legendary stone temple golden lighting"
    },
    "philosophy": {
        "voice": "en-US-AndrewMultilingualNeural",
        "bgm": "0.022*sin(2*PI*146.83*t)+0.018*sin(2*PI*174.61*t)+0.015*sin(2*PI*220*t)",
        "color_eq": "eq=contrast=1.14:saturation=1.10:brightness=-0.02",
        "sub_color": "&H00FFFFFF&",
        "prompt_suffix": "stoic contemplative cinematic marble statue dramatic rain stormy sea"
    },
    "cartoon": {
        "voice": "en-US-AndrewMultilingualNeural",
        "bgm": "0.02*sin(2*PI*196*t)+0.018*sin(2*PI*246.94*t)+0.015*sin(2*PI*293.66*t)",
        "color_eq": "eq=contrast=1.08:saturation=1.35:brightness=0.01",
        "sub_color": "&H0000FFFF&",
        "prompt_suffix": "3D Pixar Disney animation style colorful expressive cute character adorable"
    },
    "psychology": {
        "voice": "en-US-AndrewMultilingualNeural",
        "bgm": "0.022*sin(2*PI*110*t)+0.02*sin(2*PI*138.59*t)+0.016*sin(2*PI*164.81*t)",
        "color_eq": "eq=contrast=1.16:saturation=1.05:brightness=-0.03",
        "sub_color": "&H0000FFFF&",
        "prompt_suffix": "deep thought psychological metaphor human mind neurons darkness light"
    },
    "history": {
        "voice": "en-US-AndrewMultilingualNeural",
        "bgm": "0.022*sin(2*PI*130.81*t)+0.018*sin(2*PI*155.56*t)+0.016*sin(2*PI*196*t)",
        "color_eq": "eq=contrast=1.15:saturation=0.98:brightness=-0.02",
        "sub_color": "&H00D0FFFF&",
        "prompt_suffix": "historical archival authentic cinematic period piece museum oil painting"
    },
    "general": {
        "voice": "en-US-AndrewMultilingualNeural",
        "bgm": "0.025*sin(2*PI*130.81*t)+0.02*sin(2*PI*164.81*t)+0.015*sin(2*PI*196*t)",
        "color_eq": "eq=contrast=1.12:saturation=1.16:brightness=-0.02",
        "sub_color": "&H0000FFFF&",
        "prompt_suffix": "cinematic dramatic lighting photorealistic 8k"
    }
}


def run_cmd(cmd):
    """Run a shell command and check for errors."""
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{r.stdout}")
    return r.stdout


def get_duration(audio_path):
    """Get audio duration in seconds using ffprobe/ffmpeg."""
    cmd = [
        FFMPEG_EXE, "-i", audio_path,
        "-f", "null", "-"
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", p.stdout)
    if m:
        h, mn, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
        return h * 3600 + mn * 60 + s
    return 30.0


async def generate_speech_and_subtitles(text, voice, out_audio_path, out_ass_path):
    """
    Generate audio via edge-tts and create styled ASS kinetic subtitles.
    """
    import edge_tts

    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+5%")
    submaker = edge_tts.SubMaker()

    with open(out_audio_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                submaker.feed(chunk)

    # Convert sentences into punchy, rhythm-timed word bursts for Shorts
    entries = []
    # submaker.cues format: Subtitle object with cue.start, cue.end, cue.content
    if hasattr(submaker, "cues") and submaker.cues:
        for cue in submaker.cues:
            start_s = cue.start.total_seconds()
            end_s = cue.end.total_seconds()
            sentence = cue.content.strip()
            words = sentence.split()
            if not words:
                continue

            # Split sentence into chunks of 2-4 words
            chunk_size = 3
            word_chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
            tot_len = sum(len(w) for w in words)
            curr_s = start_s

            for w_chunk in word_chunks:
                chunk_len = sum(len(w) for w in w_chunk)
                ratio = chunk_len / max(1, tot_len)
                duration = max(0.4, (end_s - start_s) * ratio)
                chunk_end = min(end_s, curr_s + duration)
                chunk_text = " ".join(w_chunk).upper()
                entries.append((curr_s, chunk_end, chunk_text))
                curr_s = chunk_end
    else:
        # Fallback if no cues: single chunk
        dur = get_duration(out_audio_path)
        words = text.split()
        chunk_size = 3
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        dt = dur / max(1, len(chunks))
        for i, c in enumerate(chunks):
            entries.append((i * dt, (i + 1) * dt, " ".join(c).upper()))

    def fmt_ass_time(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        cs = int((sec - int(sec)) * 100)
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    # ASS Header with high-retention viral styling:
    # Yellow primary, black thick border, bold uppercase font, safe-zone positioning
    ass_content = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "WrapStyle: 0",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: ShortsDefault,Arial,68,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,60,60,420,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    for start_s, end_s, chunk_text in entries:
        t_start = fmt_ass_time(start_s)
        t_end = fmt_ass_time(end_s)
        ass_content.append(f"Dialogue: 0,{t_start},{t_end},ShortsDefault,,0,0,0,,{chunk_text}")

    with open(out_ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_content))


def download_ai_image(prompt, out_path):
    """Download vertical AI-generated image from Pollinations.ai with graceful local fallback."""
    try:
        clean_prompt = re.sub(r"[^a-zA-Z0-9\s,]", "", prompt)[:90]
        encoded = urllib.parse.quote(clean_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}%20cinematic%20dramatic%20lighting?width=720&height=1280&nologo=true"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(out_path, "wb") as f:
                f.write(resp.read())
            return True
    except Exception as e:
        print(f"    (AI image service notice: {e}; falling back to procedural cinematic scene)")
        # Fallback: Generate an elegant dark gradient still using FFmpeg
        cmd = [
            FFMPEG_EXE, "-y", "-f", "lavfi",
            "-i", "color=c=0x111625:s=1080x1920:d=1,drawbox=y=ih*0.3:color=0x212a45@0.8:width=iw:height=ih*0.4:t=fill,boxblur=lr=100:cr=100",
            "-vframes", "1", out_path
        ]
        run_cmd(cmd)
        return False


def create_ai_scenes_video(prompts, total_duration, out_video_path, temp_dir):
    """
    Download AI images for each scene and apply Ken Burns pan/zoom with FFmpeg.
    """
    scene_dur = max(3.0, total_duration / len(prompts))
    scene_clips = []

    for i, p in enumerate(prompts):
        img_path = os.path.join(temp_dir, f"scene_{i}.jpg")
        clip_path = os.path.join(temp_dir, f"clip_{i}.mp4")
        print(f"  [AI Visual {i+1}/{len(prompts)}] Generating image for: '{p[:40]}...'")
        download_ai_image(p, img_path)

        # Alternating zoom-in and zoom-out Ken Burns effect
        zoom_filter = (
            f"zoompan=z='min(zoom+0.0015,1.25)':d={int(scene_dur * 30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
            if i % 2 == 0
            else f"zoompan=z='if(lte(zoom,1.0),1.25,max(1.001,zoom-0.0015))':d={int(scene_dur * 30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        )

        cmd = [
            FFMPEG_EXE, "-y", "-loop", "1", "-i", img_path,
            "-vf", zoom_filter,
            "-t", f"{scene_dur:.2f}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            clip_path
        ]
        run_cmd(cmd)
        scene_clips.append(clip_path)

    # Concat clips
    concat_txt = os.path.join(temp_dir, "concat.txt")
    with open(concat_txt, "w") as f:
        for c in scene_clips:
            f.write(f"file '{c}'\n")

    cmd = [
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-t", f"{total_duration:.2f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        out_video_path
    ]
    run_cmd(cmd)


def create_procedural_motion_video(total_duration, out_video_path):
    """
    Generate dynamic animated gradient backdrop in 1080x1920.
    """
    vf = (
        "color=c=black:s=1080x1920:d=" + str(total_duration) + "[base];"
        "testsrc2=s=1080x1920:d=" + str(total_duration) + ",boxblur=lr=60:cr=60[bg];"
        "[base][bg]blend=all_mode='overlay':all_opacity=0.45,"
        "eq=brightness=-0.05:contrast=1.2:saturation=1.4,"
        "vignette=PI/4[out]"
    )
    cmd = [
        FFMPEG_EXE, "-y", "-f", "lavfi", "-i", f"nullsrc=s=1080x1920:d={total_duration}",
        "-filter_complex", vf,
        "-map", "[out]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        out_video_path
    ]
    run_cmd(cmd)


def create_broll_video(broll_path, total_duration, out_video_path):
    """
    Loop and crop user-provided B-roll video to 1080x1920 vertical.
    """
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    cmd = [
        FFMPEG_EXE, "-y", "-stream_loop", "-1", "-i", broll_path,
        "-vf", vf,
        "-t", f"{total_duration:.2f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-an",
        out_video_path
    ]
    run_cmd(cmd)


def main():
    parser = argparse.ArgumentParser(description="Free Faceless Short Video Generator")
    parser.add_argument("--title", default="Viral Short", help="Title of the video")
    parser.add_argument("--genre", default="general", choices=list(GENRE_PROFILES.keys()), help="Content genre: mystery, scifi, mythology, philosophy, cartoon, psychology, history, general")
    parser.add_argument("--script", help="Script text directly")
    parser.add_argument("--script-file", help="Path to text file containing script")
    parser.add_argument("--voice", help="Edge-TTS voice (overrides genre default)")
    parser.add_argument("--visuals", default="stock", choices=["stock", "ai", "motion", "broll"], help="Visual style: 'stock' (Wikimedia/NASA/open clips), 'ai', 'motion', or 'broll'")
    parser.add_argument("--keyword", help="Search keyword for open stock video (e.g. 'earth', 'space', 'ocean', 'city')")
    parser.add_argument("--broll", help="Path to custom B-roll video file (e.g. gameplay, nature, satisfying footage)")
    parser.add_argument("--cinematic", action="store_true", default=True, help="Apply cinematic 35mm film grain, color grading, and lens vignette")
    parser.add_argument("--output", default="output/final_short.mp4", help="Output MP4 path")
    args = parser.parse_args()

    profile = GENRE_PROFILES.get(args.genre, GENRE_PROFILES["general"])
    active_voice = args.voice if args.voice else profile["voice"]

    if args.script_file and os.path.exists(args.script_file):
        with open(args.script_file, "r", encoding="utf-8") as f:
            script_text = f.read().strip()
    elif args.script:
        script_text = args.script.strip()
    else:
        sys.exit("Error: Must provide --script or --script-file.")

    output_path = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    temp_dir = os.path.join(os.path.dirname(output_path), "temp_build")
    os.makedirs(temp_dir, exist_ok=True)

    print("==================================================")
    print("🎬 STARTING FACELESS SHORT VIDEO PIPELINE")
    print(f"Title:   {args.title}")
    print(f"Genre:   {args.genre.upper()}")
    print(f"Voice:   {active_voice}")
    print(f"Visuals: {args.visuals}")
    print("==================================================")

    # 1. Voice & Subtitles
    voice_audio = os.path.join(temp_dir, "voice.mp3")
    captions_ass = os.path.join(temp_dir, "captions.ass")
    print("📢 Step 1: Synthesizing voiceover and generating subtitles...")
    asyncio.run(generate_speech_and_subtitles(script_text, active_voice, voice_audio, captions_ass))
    duration = get_duration(voice_audio)
    print(f"   Voice track duration: {duration:.2f}s")

    # 2. Visuals
    raw_video = os.path.join(temp_dir, "raw_video.mp4")
    print("🎨 Step 2: Generating visuals...")
    if args.broll and os.path.exists(args.broll):
        print(f"   Using custom B-roll footage: {args.broll}")
        create_broll_video(args.broll, duration, raw_video)
    elif args.visuals == "stock":
        query = args.keyword if args.keyword else args.title
        stock_clip_path = os.path.join(temp_dir, "downloaded_stock.mp4")
        print(f"   Querying open connectors (Wikimedia / NASA / Open Archives) for: '{query}'...")
        success = fetch_open_stock_video(query, stock_clip_path)
        if success:
            print("   Downloaded real open-source footage! Scaling & cropping to 1080x1920...")
            create_broll_video(stock_clip_path, duration, raw_video)
        else:
            print("   No direct video match in open connectors; falling back to procedural motion.")
            create_procedural_motion_video(duration, raw_video)
    elif args.visuals == "ai":
        # Extract sentence prompts from script
        sentences = [s.strip() for s in re.split(r"[.!?]", script_text) if len(s.strip()) > 8]
        if not sentences:
            sentences = [script_text[:80]]
        # Limit to 3-6 scenes max for clean pacing
        if len(sentences) > 6:
            step = len(sentences) // 5
            prompts = [sentences[i] for i in range(0, len(sentences), step)][:5]
        else:
            prompts = sentences
        create_ai_scenes_video(prompts, duration, raw_video, temp_dir)
    else:
        create_procedural_motion_video(duration, raw_video)

    # 3. Audio & Music Bed (Genre-specific ambient harmonic soundscape)
    print(f"🎵 Step 3: Mixing {args.genre} ambient soundtrack and audio ducking...")
    mixed_audio = os.path.join(temp_dir, "mixed_audio.mp3")
    bgm_tone = profile["bgm"]
    bgm_filter = (
        f"aevalsrc='{bgm_tone}':d={duration}[bgm];"
        "[0:a][bgm]amix=inputs=2:duration=first:weights=1.0 0.23[out]"
    )
    cmd = [
        FFMPEG_EXE, "-y", "-i", voice_audio,
        "-filter_complex", bgm_filter,
        "-map", "[out]",
        mixed_audio
    ]
    run_cmd(cmd)

    # 4. Final Render with Burned-In Captions
    print("⚡ Step 4: Final rendering with cinematic grading & kinetic captions...")
    escaped_ass = captions_ass.replace(":", "\\:").replace("'", "\\'")
    
    if args.cinematic:
        color_eq = profile["color_eq"]
        vf_chain = f"{color_eq},noise=alls=5:allf=t+u,vignette=PI/4,ass='{escaped_ass}'"
    else:
        vf_chain = f"ass='{escaped_ass}'"

    cmd = [
        FFMPEG_EXE, "-y",
        "-i", raw_video,
        "-i", mixed_audio,
        "-vf", vf_chain,
        "-c:v", "libx264", "-preset", "fast", "-crf", "19",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", f"{duration:.2f}",
        output_path
    ]
    run_cmd(cmd)

    print("==================================================")
    print(f"✅ VIDEO READY: {output_path}")
    print("==================================================")


if __name__ == "__main__":
    main()
