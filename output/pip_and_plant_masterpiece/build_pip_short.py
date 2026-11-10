#!/usr/bin/env python3
"""
build_pip_short.py — Master rendering engine for Pip & The Iron Blossom Short.
Features:
- Andrew Multilingual Neural human-touch voiceover
- 12 dynamic Ken Burns camera cuts (2.5 - 3.5s pacing)
- 3D Pixar Disney aesthetic
- Word-burst kinetic ASS subtitles in mobile safe-zone (Y=1450px)
- Algorithmic uplifting harmonic soundbed (G-major emotional warmth, 0% copyright)
- Cinematic 35mm grain & vignette
"""

import os
import re
import sys
import subprocess

DIR = os.path.abspath(os.path.dirname(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(DIR, "../.."))
FFMPEG = os.path.join(WORKSPACE_ROOT, ".venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1")

SCENE_1 = os.path.join(DIR, "scene_01.jpg")
SCENE_2 = os.path.join(DIR, "scene_02.jpg")
SCENE_4 = os.path.join(DIR, "scene_04.jpg")
SCENE_5 = os.path.join(DIR, "scene_05.jpg")

VOICE_AUDIO = os.path.join(DIR, "pip_voice.mp3")
VTT_FILE = os.path.join(DIR, "pip_subs.vtt")
ASS_FILE = os.path.join(DIR, "pip_kinetic.ass")
FINAL_MP4 = os.path.join(DIR, "pip_and_the_iron_blossom.mp4")
THUMB_JPG = os.path.join(DIR, "pip_thumbnail.jpg")


def parse_vtt_to_ass(vtt_path, ass_path):
    with open(vtt_path, "r", encoding="utf-8") as f:
        vtt_text = f.read()

    # Match VTT cues: 00:00:00,050 --> 00:00:06,747
    pattern = re.compile(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*\n(.*?)(?=\n\s*\n|\n\d+\n|$)", re.DOTALL)
    
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
            d = max(0.4, total_dur * frac)
            c_end = min(end_sec, curr + d)
            events.append((curr, c_end, " ".join(chk).upper()))
            curr = c_end

    def fmt_ass(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        cs = int((sec - int(sec)) * 100)
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
        "Style: PixarShorts,Arial,66,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,60,60,450,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    for start_t, end_t, txt in events:
        lines.append(f"Dialogue: 0,{fmt_ass(start_t)},{fmt_ass(end_t)},PixarShorts,,0,0,0,,{txt}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Created ASS subtitles: {len(events)} kinetic word bursts -> {ass_path}")


def main():
    print("--- 1. Parsing VTT to ASS Kinetic Subtitles ---")
    parse_vtt_to_ass(VTT_FILE, ASS_FILE)

    # 12 dynamic camera cuts across 41.66s
    cuts = [
        # (image, duration, zoompan_filter, description)
        (SCENE_1, 3.40, "zoompan=z='min(zoom+0.0015,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=102:s=1080x1920:fps=30", "Cut 1: Wide twilight scrap hill slow zoom"),
        (SCENE_1, 3.35, "zoompan=z='min(zoom+0.002,1.3)':x='iw*0.3':y='ih*0.2':d=101:s=1080x1920:fps=30", "Cut 2: Close punch on Pip glowing eyes"),
        (SCENE_2, 3.65, "zoompan=z='min(zoom+0.0015,1.25)':x='iw*0.4':y='ih*0.5':d=110:s=1080x1920:fps=30", "Cut 3: Pip cupping glowing sprout pan"),
        (SCENE_2, 3.68, "zoompan=z='min(zoom+0.002,1.35)':x='iw*0.35':y='ih*0.35':d=111:s=1080x1920:fps=30", "Cut 4: Emerald glow reflecting on Pip face"),
        (SCENE_4, 3.42, "zoompan=z='min(zoom+0.0012,1.2)':x='iw*0.5':y='ih*0.3':d=103:s=1080x1920:fps=30", "Cut 5: Mountaintop sunrise mist wide"),
        (SCENE_4, 3.34, "zoompan=z='min(zoom+0.0018,1.28)':x='iw*0.35':y='ih*0.55':d=101:s=1080x1920:fps=30", "Cut 6: Pip planting sprout in dark soil"),
        (SCENE_2, 2.95, "zoompan=z='min(zoom+0.0025,1.3)':x='iw*0.45':y='ih*0.45':d=89:s=1080x1920:fps=30", "Cut 7: Warm drop touches glowing leaf"),
        (SCENE_2, 2.96, "zoompan=z='min(zoom+0.003,1.4)':x='iw*0.4':y='ih*0.4':d=89:s=1080x1920:fps=30", "Cut 8: Bioluminescent pulse bloom"),
        (SCENE_5, 3.75, "zoompan=z='min(zoom+0.0015,1.22)':x='iw*0.45':y='ih*0.4':d=113:s=1080x1920:fps=30", "Cut 9: Massive golden blossom rises"),
        (SCENE_5, 3.76, "zoompan=z='min(zoom+0.0012,1.18)':x='iw*0.5':y='ih*0.6':d=113:s=1080x1920:fps=30", "Cut 10: Wildflowers spreading to horizon"),
        (SCENE_5, 3.74, "zoompan=z='min(zoom+0.002,1.28)':x='iw*0.35':y='ih*0.65':d=113:s=1080x1920:fps=30", "Cut 11: Pip leaping with pure joy"),
        (SCENE_1, 3.66, "zoompan=z='min(zoom+0.0015,1.2)':x='iw*0.4':y='ih*0.35':d=110:s=1080x1920:fps=30", "Cut 12: Loop resolution and wonder")
    ]

    clip_paths = []
    print(f"--- 2. Rendering {len(cuts)} Dynamic Camera Motion Cuts ---")
    
    for i, (img, dur, zp, desc) in enumerate(cuts):
        clip_out = os.path.join(DIR, f"clip_{i+1:02d}.mp4")
        clip_paths.append(clip_out)
        print(f"[{i+1}/{len(cuts)}] {desc} ({dur}s)...")
        
        # Color grade: vibrant 3D Pixar warmth + subtle lens vignette
        vf = (
            f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"{zp},"
            f"eq=contrast=1.12:saturation=1.30:brightness=0.01,"
            f"vignette=PI/4.5"
        )
        
        cmd = [
            FFMPEG, "-y",
            "-loop", "1",
            "-i", img,
            "-t", str(dur),
            "-vf", vf,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            clip_out
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    # Concat file
    concat_txt = os.path.join(DIR, "concat_clips.txt")
    with open(concat_txt, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p}'\n")

    raw_stitched = os.path.join(DIR, "raw_stitched.mp4")
    print("--- 3. Concatenating Visual Cuts ---")
    cmd_concat = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        raw_stitched
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    print("--- 4. Synthesizing Uplifting G-Major Soundbed & Mixing Voice ---")
    # Voice duration is 41.66s. Generate ducked ambient music bed (0% copyright)
    mixed_audio = os.path.join(DIR, "pip_soundtrack.mp3")
    
    # G major emotional chord progression (G3=196Hz, B3=246.94Hz, D4=293.66Hz, G4=392Hz)
    bgm_expr = (
        "0.018*sin(2*PI*196*t*(1+0.002*sin(2*PI*0.4*t)))"
        "+0.015*sin(2*PI*246.94*t)"
        "+0.013*sin(2*PI*293.66*t)"
        "+0.010*sin(2*PI*392*t*(1+0.002*cos(2*PI*0.3*t)))"
    )
    
    cmd_audio = [
        FFMPEG, "-y",
        "-i", VOICE_AUDIO,
        "-f", "lavfi",
        "-t", "41.66",
        "-i", f"aevalsrc={bgm_expr}:s=44100",
        "-filter_complex",
        "[0:a]volume=1.05[v];[1:a]volume=0.20,afade=t=in:ss=0:d=1.5,afade=t=out:st=40.0:d=1.6[m];[v][m]amix=inputs=2:duration=first[aout]",
        "-map", "[aout]",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        mixed_audio
    ]
    subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    print("--- 5. Final Render: Muxing Audio & Burning Kinetic Subtitles ---")
    cmd_final = [
        FFMPEG, "-y",
        "-i", raw_stitched,
        "-i", mixed_audio,
        "-vf", f"ass={ASS_FILE}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        FINAL_MP4
    ]
    subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    print("--- 6. Generating Thumbnail Poster ---")
    cmd_thumb = [
        FFMPEG, "-y",
        "-ss", "00:00:29.0",
        "-i", FINAL_MP4,
        "-frames:v", "1",
        "-q:v", "2",
        THUMB_JPG
    ]
    subprocess.run(cmd_thumb, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    print("\n==========================================")
    print("✨ PRODUCTION COMPLETE ✨")
    print(f"Final Video: {FINAL_MP4}")
    print(f"Thumbnail:   {THUMB_JPG}")
    print("==========================================")


if __name__ == "__main__":
    main()
