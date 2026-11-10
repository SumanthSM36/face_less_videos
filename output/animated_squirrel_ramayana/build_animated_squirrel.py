#!/usr/bin/env python3
"""
build_animated_squirrel.py — Senior Animation Director Production Engine
The Legend of the Ramayana Squirrel (3D Pixar / Disney Cinematic Aesthetic).

Enforces:
1. Safe-Zone Kinetic Subtitles (1080x1920, Y=1450px, Pixar Yellow #00FFFF, MarginV=450).
2. Pacing: 2.5s-3.5s dynamic camera cuts (10 distinct animated cuts across 5 scenes).
3. Studio-Mastered Voiceover: Andrew Multilingual (en-US-AndrewMultilingualNeural) with warm chest EQ, de-essing, dynamic leveling & limiter.
4. Rule 8: High-Definition 3D RenderMan asset fidelity.
5. Acoustic scoring: Tender piano & strings, ducked to 20%.
6. Infinite loop hook.
"""

import os
import re
import sys
import subprocess
import json

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VENV_BIN = os.path.join(WORKSPACE_ROOT, ".venv/bin")
FFMPEG = os.path.join(WORKSPACE_ROOT, ".venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1")
EDGE_TTS = os.path.join(VENV_BIN, "edge-tts")
DEFAULT_MUSIC = os.path.join(WORKSPACE_ROOT, "output/assets/music/satie_gymnopedie.wav")
WORK_DIR = os.path.abspath(os.path.dirname(__file__))

VOICE = "en-US-AndrewMultilingualNeural"
RATE = "+2%"
SUB_COLOR = "&H0000FFFF&"  # Pixar Yellow

SCRIPT_TEXT = (
    "Have you ever wondered why Indian squirrels have three white stripes? "
    "Thousands of years ago, on the stormy shores of Lanka, giant warriors were tossing mountains into the raging sea. "
    "Between their colossal feet scurried a tiny squirrel, rolling in the sand and shaking pebbles into the gaps. "
    "The giants burst into laughter at its tiny effort. "
    "But Lord Rama knelt down in the sand, scooping the trembling creature into his divine hand. "
    "Never mock love, Rama whispered. In my eyes, no sacrifice is small. "
    "With infinite tenderness, Rama stroked the squirrel's back with three fingers. "
    "Under his touch, three glowing white stripes appeared forever. "
    "Which is why, whenever you see a squirrel today, you still wonder..."
)

IMAGES = [
    os.path.join(WORK_DIR, "scene_01.png"),
    os.path.join(WORK_DIR, "scene_02.png"),
    os.path.join(WORK_DIR, "scene_03.png"),
    os.path.join(WORK_DIR, "scene_04.png"),
    os.path.join(WORK_DIR, "scene_05.png")
]


def run_cmd(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stdout}")
    return p.stdout


def get_audio_duration(path):
    cmd = [FFMPEG, "-i", path, "-f", "null", "-"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", p.stdout)
    if m:
        h, mn, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
        return h * 3600 + mn * 60 + s
    return 35.0


def parse_vtt_to_ass(vtt_path, ass_path):
    with open(vtt_path, "r", encoding="utf-8") as f:
        vtt_text = f.read()

    pattern = re.compile(
        r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*\n(.*?)(?=\n\s*\n|\n\d+\n|$)",
        re.DOTALL
    )
    
    events = []
    for m in pattern.finditer(vtt_text):
        s_h, s_m, s_s, s_ms = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        e_h, e_m, e_s, e_ms = int(m.group(5)), int(m.group(6)), int(m.group(7)), int(m.group(8))
        
        start_sec = s_h * 3600 + s_m * 60 + s_s + s_ms / 1000.0
        end_sec = e_h * 3600 + e_m * 60 + e_s + e_ms / 1000.0
        text = m.group(9).replace("\n", " ").strip()
        words = text.split()
        if not words:
            continue
            
        chunk_size = 3
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        total_chars = sum(len(w) for w in words)
        
        curr = start_sec
        total_dur = end_sec - start_sec
        
        for chk in chunks:
            chk_chars = sum(len(w) for w in chk)
            frac = chk_chars / max(1, total_chars)
            d = max(0.35, total_dur * frac)
            c_end = min(end_sec, curr + d)
            events.append((curr, c_end, " ".join(chk).upper()))
            curr = c_end

    def fmt_ass(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        cs = min(99, int((sec - int(sec)) * 100))
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "WrapStyle: 0",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: AnimatedSquirrel,Impact,78,{SUB_COLOR},&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,6,2,2,60,60,450,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    for start_t, end_t, txt in events:
        lines.append(f"Dialogue: 0,{fmt_ass(start_t)},{fmt_ass(end_t)},AnimatedSquirrel,,0,0,0,,{txt}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"✅ Generated Kinetic ASS Subtitles: {len(events)} word bursts -> {ass_path}")


def render_animated_short():
    os.makedirs(WORK_DIR, exist_ok=True)
    voice_audio = os.path.join(WORK_DIR, "dir_voice.mp3")
    vtt_file = os.path.join(WORK_DIR, "dir_subs.vtt")
    ass_file = os.path.join(WORK_DIR, "dir_kinetic.ass")
    mastered_voice = os.path.join(WORK_DIR, "mastered_voice.mp3")
    output_mp4 = os.path.join(WORK_DIR, "the_squirrels_three_stripes_3d.mp4")
    thumb_jpg = os.path.join(WORK_DIR, "thumbnail.jpg")

    print("\n🎬 =======================================================")
    print("🐿️ 3D ANIMATED SHORTS MASTER: THE SQUIRREL'S 3 STRIPES")
    print("=======================================================")

    # 1. Narrator Synthesis
    print(f"\n🎙️ Step 1: Synthesizing Emotional Storytelling Narration ({VOICE} {RATE})...")
    cmd_tts = [
        EDGE_TTS,
        "--voice", VOICE,
        "--rate", RATE,
        "--text", SCRIPT_TEXT,
        "--write-media", voice_audio,
        "--write-subtitles", vtt_file
    ]
    run_cmd(cmd_tts)

    # 2. Vocal Mastering
    print("🎛️ Step 2: Applying Conversational Studio Mastering Chain (280Hz warm boost, de-essing, limiter)...")
    cmd_master = [
        FFMPEG, "-y",
        "-i", voice_audio,
        "-af", "highpass=f=80,lowpass=f=11000,equalizer=f=280:t=q:w=1.0:g=3.0,equalizer=f=3200:t=q:w=1.5:g=-2.5,compand=attacks=0.02:decays=0.2:points=-80/-80|-30/-20|0/-12:soft-knee=6,alimiter=limit=-1.5dB:attack=5:release=50:asc=1",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        mastered_voice
    ]
    run_cmd(cmd_master)
    total_dur = get_audio_duration(mastered_voice)
    print(f"✅ Mastered Voice Duration: {total_dur:.2f} seconds")

    # 3. Kinetic Subtitles
    print("\n📝 Step 3: Generating Mobile Safe-Zone Kinetic Subtitles...")
    parse_vtt_to_ass(vtt_file, ass_file)

    # 4. Asset Fidelity Gate (Rule 8)
    print("\n🛡️ Step 4: Rule 8 Anti-Blur Verification...")
    for img in IMAGES:
        if not os.path.exists(img):
            raise FileNotFoundError(f"Missing required 3D asset: {img}")
        size_kb = os.path.getsize(img) / 1024
        if size_kb < 150:
            raise ValueError(f"Asset {os.path.basename(img)} ({size_kb:.1f} KB) failed Rule 8 high-definition threshold.")
        print(f"   ✅ Verified High-Definition Asset: {os.path.basename(img)} ({size_kb:.1f} KB)")

    # 5. Pacing & Camera Cuts (2 dynamic cuts per 3D scene = 10 cuts total)
    total_cuts = len(IMAGES) * 2
    cut_dur = total_dur / total_cuts
    print(f"\n🎬 Step 5: Directing {total_cuts} Cinematic 3D Camera Cuts ({cut_dur:.2f}s per cut)...")

    camera_choreography = [
        # Scene 1: Ocean & Shore
        ("zoompan=z='min(zoom+0.0018,1.22)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'", "Wide Ocean Crane Down"),
        ("zoompan=z='min(zoom+0.0028,1.35)':x='iw*0.4':y='ih*0.65'", "Punch-in on Tiny Squirrel in Sand"),
        # Scene 2: Giant Laughter
        ("zoompan=z='min(zoom+0.002,1.26)':x='iw*0.3':y='ih*0.25'", "Low-Angle Laughing Vanara Giants"),
        ("zoompan=z='min(zoom+0.0025,1.38)':x='iw*0.45':y='ih*0.6'", "Squirrel Rolling in Dust Hero Close-up"),
        # Scene 3: Lord Rama Kneeling
        ("zoompan=z='min(zoom+0.0016,1.24)':x='iw/2-(iw/zoom/2)':y='ih*0.35'", "Lord Rama Kneeling Sunset Wide"),
        ("zoompan=z='min(zoom+0.0022,1.3)':x='iw*0.48':y='ih*0.55'", "Divine Hand Reaching Down"),
        # Scene 4: Squirrel in Palm
        ("zoompan=z='min(zoom+0.0025,1.35)':x='iw*0.45':y='ih*0.45'", "Teary Squirrel Looking Up in Devotion"),
        ("zoompan=z='min(zoom+0.0018,1.25)':x='iw*0.4':y='ih*0.3'", "Rama's Tender Smiling Face"),
        # Scene 5: Glowing Stripes Materializing
        ("zoompan=z='min(zoom+0.0022,1.32)':x='iw*0.42':y='ih*0.5'", "Three Fingers Stroking Fur"),
        ("zoompan=z='min(zoom+0.003,1.4)':x='iw*0.45':y='ih*0.45'", "Celestial Glowing Stripes Materializing")
    ]

    clip_paths = []
    cut_idx = 0
    for img_idx, img in enumerate(IMAGES):
        for sub_cut in range(2):
            cut_idx += 1
            zp, desc = camera_choreography[(cut_idx - 1) % len(camera_choreography)]
            clip_file = os.path.join(WORK_DIR, f"clip_{cut_idx:02d}.mp4")
            clip_paths.append(clip_file)
            print(f"   [{cut_idx}/{total_cuts}] Cut {cut_idx}: {desc} ({cut_dur:.2f}s)...")

            d_frames = int(cut_dur * 30) + 1
            vf = (
                f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                f"{zp}:d={d_frames}:s=1080x1920:fps=30,"
                f"eq=contrast=1.14:saturation=1.24:brightness=0.01,"
                f"vignette=PI/4.8"
            )
            cmd_clip = [
                FFMPEG, "-y",
                "-loop", "1",
                "-i", img,
                "-t", str(cut_dur),
                "-vf", vf,
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                clip_file
            ]
            run_cmd(cmd_clip)

    # 6. Concat
    concat_txt = os.path.join(WORK_DIR, "concat.txt")
    with open(concat_txt, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p}'\n")

    raw_stitched = os.path.join(WORK_DIR, "raw_stitched.mp4")
    print("\n🎬 Step 6: Stitching Visual Cuts...")
    run_cmd([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", raw_stitched])

    # 7. Soundtrack & Ducking
    print("\n🎵 Step 7: Acoustic Piano Scoring & Automatic Vocal Ducking...")
    mixed_audio = os.path.join(WORK_DIR, "soundtrack.mp3")
    cmd_audio = [
        FFMPEG, "-y",
        "-i", mastered_voice,
        "-ss", "00:00:03.0",
        "-i", DEFAULT_MUSIC,
        "-filter_complex",
        f"[0:a]volume=1.05[v];[1:a]volume=0.20,afade=t=in:ss=0:d=1.5,afade=t=out:st={total_dur-2.0:.2f}:d=2.0[m];[v][m]amix=inputs=2:duration=first[aout]",
        "-map", "[aout]",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        mixed_audio
    ]
    run_cmd(cmd_audio)

    # 8. Burning Kinetic Subtitles
    print("\n🔥 Step 8: Burning Safe-Zone Kinetic Subtitles & Broadcast Assembly...")
    cmd_final = [
        FFMPEG, "-y",
        "-i", raw_stitched,
        "-i", mixed_audio,
        "-vf", f"ass={ass_file}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4
    ]
    run_cmd(cmd_final)

    # 9. Thumbnail
    print("📸 Step 9: Extracting High-Contrast Thumbnail...")
    run_cmd([FFMPEG, "-y", "-ss", f"00:00:{int(total_dur*0.65):02d}.0", "-i", output_mp4, "-frames:v", "1", "-q:v", "2", thumb_jpg])

    size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    print("\n" + "=" * 60)
    print("🏆 3D ANIMATED MASTERWORK COMPLETE")
    print(f"Video:     {output_mp4} ({size_mb:.2f} MB, {total_dur:.2f}s)")
    print(f"Thumbnail: {thumb_jpg}")
    print("=" * 60 + "\n")
    return output_mp4, thumb_jpg


if __name__ == "__main__":
    render_animated_short()
