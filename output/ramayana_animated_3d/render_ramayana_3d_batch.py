#!/usr/bin/env python3
"""
render_ramayana_3d_batch.py — Senior 3D Animation Production Engine
Recreates Ramayana Shorts 2, 3, 4, 5 in Disney/Pixar 3D RenderMan Cinematic Aesthetic.
"""

import os
import re
import sys
import json
import subprocess

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VENV_BIN = os.path.join(WORKSPACE_ROOT, ".venv/bin")
FFMPEG = os.path.join(WORKSPACE_ROOT, ".venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1")
EDGE_TTS = os.path.join(VENV_BIN, "edge-tts")
DEFAULT_MUSIC = os.path.join(WORKSPACE_ROOT, "output/assets/music/satie_gymnopedie.wav")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

VOICE = "en-US-AndrewMultilingualNeural"
RATE = "+2%"
SUB_COLOR = "&H0000FFFF&"  # Pixar Yellow

SHORTS_CONFIG = [
    {
        "id": "short_02_gayatri_cipher",
        "title": "The Hidden 24-Letter Code in Ramayana 📜",
        "dir": os.path.join(BASE_DIR, "short_02_gayatri_cipher"),
        "script": (
            "The Ramayana hides a sacred cosmic cipher right in plain sight. "
            "Thousands of years ago, sage Valmiki composed exactly twenty-four thousand verses in the epic. "
            "The supreme Gayatri Mantra contains exactly twenty-four mystical syllables. "
            "Here is the secret: every one-thousandth verse begins with the consecutive syllable of the Gayatri Mantra! "
            "By hearing the entire Ramayana, you chant the supreme Gayatri Mantra. "
            "This mathematical miracle proves why the epic hides a sacred cosmic cipher right in plain sight. "
            "Because..."
        )
    },
    {
        "id": "short_03_ravana_violin",
        "title": "Why Ravana Ripped Out His Own Vein 🎻",
        "dir": os.path.join(BASE_DIR, "short_03_ravana_violin"),
        "script": (
            "Did you know Ravana invented the ancestor of the modern violin? "
            "When Ravana tried to lift Mount Kailash, Lord Shiva pressed his toe, crushing him beneath. "
            "In unbearable agony, Ravana knew only music could save his life. "
            "He severed his own arm, plucked out a pulsating tendon, and strung it like a bow. "
            "As he played and chanted the Shiva Tandava, Shiva smiled and granted him the divine sword Chandrahas. "
            "That instrument became the Ravanahatha, proving why Ravana invented the ancestor of the violin. "
            "And yet..."
        )
    },
    {
        "id": "short_04_indrajit_astras",
        "title": "The Only Mortal With 3 Supreme Astras ⚡",
        "dir": os.path.join(BASE_DIR, "short_04_indrajit_astras"),
        "script": (
            "Only one mortal warrior ever possessed all three supreme cosmic weapons. "
            "His name was Meghanada, the prince of Lanka. "
            "When born, Ravana chained all nine celestial planets into the house of immortality. "
            "But Lord Saturn slipped his foot into the house of death at the last second! "
            "Meghanada grew to conquer the heavens, capturing Indra and earning three supreme Astras: Brahmastra, Vaishnavastra, and Pashupatastra. "
            "Even the gods trembled before Meghanada, the only mortal warrior who ever possessed all three supreme cosmic weapons. "
            "Because..."
        )
    },
    {
        "id": "short_05_bharata_penance",
        "title": "The King Who Slept In A 3-Foot Pit 👑",
        "dir": os.path.join(BASE_DIR, "short_05_bharata_penance"),
        "script": (
            "Meet the prince who ruled an empire from a three-foot dirt pit. "
            "When Lord Rama was exiled, Prince Bharata was offered the golden throne of Ayodhya. "
            "He refused to touch it. "
            "Instead, Bharata lived in a straw hut in Nandigram. "
            "He dug a pit to sleep lower than Rama's forest floor, placed Rama's wooden sandals upon the royal throne, and ruled solely as a servant for fourteen years. "
            "True loyalty is not about power, which is why millions still honor the prince who ruled an empire from a dirt pit. "
            "So..."
        )
    }
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
        f"Style: AnimatedRamayana,Impact,78,{SUB_COLOR},&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,6,2,2,60,60,450,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    for start_t, end_t, txt in events:
        lines.append(f"Dialogue: 0,{fmt_ass(start_t)},{fmt_ass(end_t)},AnimatedRamayana,,0,0,0,,{txt}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def produce_short(cfg, index, total):
    short_dir = cfg["dir"]
    short_id = cfg["id"]
    output_mp4 = os.path.join(BASE_DIR, f"{short_id}_3d.mp4")
    thumb_jpg = os.path.join(BASE_DIR, f"{short_id}_3d_thumb.jpg")

    print(f"\n🎬 [{index}/{total}] PRODUCING 3D ANIMATION: {cfg['title']}")

    if os.path.exists(output_mp4) and os.path.getsize(output_mp4) > 1000000:
        print(f"   ⏩ Already rendered: {output_mp4} ({os.path.getsize(output_mp4)/(1024*1024):.2f} MB)")
        return output_mp4, thumb_jpg

    # Check images exist
    images = [os.path.join(short_dir, f"scene_{i:02d}.png") for i in range(1, 6)]
    for img in images:
        if not os.path.exists(img):
            raise FileNotFoundError(f"Missing image: {img} in {short_dir}")
        sz = os.path.getsize(img) / 1024
        print(f"   ✅ Asset: {os.path.basename(img)} ({sz:.1f} KB)")

    # 1. Voice
    voice_audio = os.path.join(short_dir, "voice.mp3")
    vtt_file = os.path.join(short_dir, "speech.vtt")
    ass_file = os.path.join(short_dir, "kinetic.ass")
    mastered_voice = os.path.join(short_dir, "mastered_voice.mp3")

    if not (os.path.exists(voice_audio) and os.path.exists(vtt_file) and os.path.getsize(voice_audio) > 10000):
        cmd_tts = [
            EDGE_TTS,
            "--voice", VOICE,
            "--rate", RATE,
            "--text", cfg["script"],
            "--write-media", voice_audio,
            "--write-subtitles", vtt_file
        ]
        run_cmd(cmd_tts)
    else:
        print("   ✅ Reusing existing voice.mp3 & speech.vtt")

    # 2. Vocal Mastering
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
    print(f"   Mastered Duration: {total_dur:.2f}s")

    # 3. Subtitles
    parse_vtt_to_ass(vtt_file, ass_file)

    # 4. 10 Camera cuts (2 per scene)
    total_cuts = len(images) * 2
    cut_dur = total_dur / total_cuts

    camera_choreography = [
        ("zoompan=z='min(zoom+0.0018,1.22)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'", "Wide Cinematic Establishing"),
        ("zoompan=z='min(zoom+0.0028,1.35)':x='iw*0.4':y='ih*0.65'", "Punch-in Hero Focus"),
        ("zoompan=z='min(zoom+0.002,1.26)':x='iw*0.3':y='ih*0.25'", "Low-Angle Dramatic Tilt"),
        ("zoompan=z='min(zoom+0.0025,1.38)':x='iw*0.45':y='ih*0.6'", "Character Expression Close-up"),
        ("zoompan=z='min(zoom+0.0016,1.24)':x='iw/2-(iw/zoom/2)':y='ih*0.35'", "Volumetric Sweeping Pan"),
        ("zoompan=z='min(zoom+0.0022,1.3)':x='iw*0.48':y='ih*0.55'", "Gentle Downward Push"),
        ("zoompan=z='min(zoom+0.0025,1.35)':x='iw*0.45':y='ih*0.45'", "Intimate Emotional Zoom"),
        ("zoompan=z='min(zoom+0.0018,1.25)':x='iw*0.4':y='ih*0.3'", "Tender Reaction Glide"),
        ("zoompan=z='min(zoom+0.0022,1.32)':x='iw*0.42':y='ih*0.5'", "Macro Hero Slow-Pan"),
        ("zoompan=z='min(zoom+0.003,1.4)':x='iw*0.45':y='ih*0.45'", "Luminous Stardust Pull-Back Loop")
    ]

    clip_paths = []
    cut_idx = 0
    for img_idx, img in enumerate(images):
        for sub_cut in range(2):
            cut_idx += 1
            zp, desc = camera_choreography[(cut_idx - 1) % len(camera_choreography)]
            clip_file = os.path.join(short_dir, f"clip_{cut_idx:02d}.mp4")
            clip_paths.append(clip_file)

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

    # 5. Concat
    concat_txt = os.path.join(short_dir, "concat.txt")
    with open(concat_txt, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p}'\n")

    raw_stitched = os.path.join(short_dir, "raw_stitched.mp4")
    run_cmd([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", raw_stitched])

    # 6. Soundtrack
    mixed_audio = os.path.join(short_dir, "soundtrack.mp3")
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

    # 7. Final assembly
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

    # 8. Thumbnail
    run_cmd([FFMPEG, "-y", "-ss", f"00:00:{int(total_dur*0.65):02d}.0", "-i", output_mp4, "-frames:v", "1", "-q:v", "2", thumb_jpg])

    size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    print(f"   🏆 Finished: {output_mp4} ({size_mb:.2f} MB, {total_dur:.2f}s)")
    return output_mp4, thumb_jpg


def main():
    print("=" * 60)
    print("🎬 PRODUCING RAMAYANA 3D ANIMATION BATCH (SHORTS 2-5)")
    print("=" * 60)

    results = []
    total = len(SHORTS_CONFIG)
    for idx, cfg in enumerate(SHORTS_CONFIG, 1):
        mp4, thumb = produce_short(cfg, idx, total)
        results.append((cfg, mp4, thumb))

    print("\n" + "=" * 60)
    print("🎉 ALL 4 3D ANIMATED SHORTS RENDERED SUCCESSFULLY!")
    print("=" * 60)
    for cfg, mp4, thumb in results:
        sz = os.path.getsize(mp4) / (1024 * 1024)
        print(f"  • {cfg['title']} -> {mp4} ({sz:.2f} MB)")


if __name__ == "__main__":
    main()
