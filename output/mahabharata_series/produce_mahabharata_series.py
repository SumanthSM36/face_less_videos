#!/usr/bin/env python3
"""
produce_mahabharata_series.py — Master Production Engine for 5 Mahabharata Fact Shorts.
Renders 1080x1920 MP4s with 10 camera cuts, studio vocal mastering, kinetic ASS subtitles,
and automatically uploads each short to YouTube as PRIVATE.
"""

import os
import re
import sys
import json
import time
import subprocess

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
VENV_BIN = os.path.join(WORKSPACE_ROOT, ".venv/bin")
FFMPEG = os.path.join(WORKSPACE_ROOT, ".venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1")
EDGE_TTS = os.path.join(VENV_BIN, "edge-tts")
DEFAULT_MUSIC = os.path.join(WORKSPACE_ROOT, "output/assets/music/satie_gymnopedie.wav")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Import YouTube connector
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts"))
from connectors.youtube_connector import upload_youtube_short

VOICE = "en-US-AndrewMultilingualNeural"
RATE = "+2%"
SUB_COLOR = "&H0000FFFF&"  # High-contrast Pixar Yellow

MAHABHARATA_SHORTS = [
    {
        "id": "short_01_barbarika_arrows",
        "title": "The Warrior Who Could End Mahabharata in 30 Seconds 🏹",
        "yt_title": "The Warrior Who Could End Mahabharata in 30 Seconds 🏹 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_01_barbarika_arrows"),
        "script": (
            "One warrior could have ended the entire Mahabharata war in thirty seconds. "
            "His name was Barbarika, grandson of Bhima. "
            "Lord Shiva granted him three infallible arrows: the first marked all targets to save, the second marked all targets to destroy, and the third executed the command. "
            "To test him, Krishna secretly hid a peepal leaf under his foot. "
            "Barbarika's arrow marked all leaves and hovered right above Krishna's toe! "
            "Knowing Barbarika vowed to always fight for the losing side, Krishna asked for his head to prevent total annihilation. "
            "Which proves why one warrior could have ended the Mahabharata war in thirty seconds. "
            "Because..."
        ),
        "description": (
            "Did you know one warrior could have ended the entire 18-day Mahabharata war in just 30 seconds? "
            "Discover the legend of Barbarika (Khatu Shyam) and his three infallible cosmic arrows.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #mahabharata #barbarika #khatushyam #krishna #hindumythology #ancienthistory"
        ),
        "tags": ["shorts", "mahabharata", "barbarika", "khatu shyam", "lord krishna", "krishna", "3d animation", "animation", "hindu mythology"]
    },
    {
        "id": "short_02_karna_armor",
        "title": "Why Karna Sliced Off His Own Flesh ⚔️",
        "yt_title": "Why Karna Sliced Off His Own Flesh ⚔️ #Shorts",
        "dir": os.path.join(BASE_DIR, "short_02_karna_armor"),
        "script": (
            "Karna was born wearing golden armor fused directly into his living flesh. "
            "As the son of the Sun god Surya, this divine breastplate made him completely invincible to any weapon in the universe. "
            "Knowing the Pandavas could never defeat him, Indra disguised himself as a poor Brahmin at sunrise. "
            "Karna had a sacred vow never to refuse charity at dawn. "
            "Even after realizing the deception, Karna unsheathed his dagger and sliced the armor off his own bleeding chest with a smile! "
            "True honor outweighed immortality, which is why Karna was born wearing armor fused directly into his flesh. "
            "And yet..."
        ),
        "description": (
            "Karna was born with divine golden armor grown directly into his living flesh. "
            "Witness the supreme sacrifice of Danaveera Karna when Lord Indra came asking for charity.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #mahabharata #karna #surya #indra #kavachkundal #danaveerakarna #mythology"
        ),
        "tags": ["shorts", "mahabharata", "karna", "surya", "indra", "kavach kundal", "3d animation", "animation", "hindu mythology"]
    },
    {
        "id": "short_03_abhimanyu_womb",
        "title": "The 16-Year-Old Who Cracked A Cosmic Labyrinth 🌀",
        "yt_title": "The 16-Year-Old Who Cracked A Cosmic Labyrinth 🌀 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_03_abhimanyu_womb"),
        "script": (
            "Did you know a sixteen-year-old boy cracked a cosmic labyrinth while still in his mother's womb? "
            "When Arjuna explained the secret Chakravyuha formation to pregnant Subhadra, unborn Abhimanyu listened intently to every strategy. "
            "He learned how to penetrate all seven circular layers. "
            "Suddenly, Subhadra fell asleep before Arjuna revealed how to escape! "
            "Years later, on Day Thirteen, young Abhimanyu breached the labyrinth alone and trapped the Kauravas. "
            "Unaware of how to exit, he fought fearlessly until his last breath, proving how a boy cracked a cosmic labyrinth from inside the womb. "
            "So..."
        ),
        "description": (
            "How did 16-year-old Abhimanyu master the deadliest battle formation in human history before he was even born? "
            "The tragic and heroic legend of the Chakravyuha on Day 13 of Kurukshetra.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #mahabharata #abhimanyu #chakravyuha #arjuna #kurukshetra #ancientwisdom"
        ),
        "tags": ["shorts", "mahabharata", "abhimanyu", "chakravyuha", "arjuna", "subhadra", "3d animation", "animation", "hindu mythology"]
    },
    {
        "id": "short_04_sahadeva_curse",
        "title": "The Prince Who Knew The Future But Could Not Speak 🔮",
        "yt_title": "The Prince Who Knew The Future But Could Not Speak 🔮 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_04_sahadeva_curse"),
        "script": (
            "Imagine knowing the exact future of every person you love, but you are cursed to die if you speak it. "
            "Sahadeva, the youngest Pandava, consumed three drops of mystical wisdom from his father Pandu, gaining complete omniscience. "
            "He knew the dice game was rigged. "
            "He knew the exact day each hero would perish in battle. "
            "Yet Krishna warned him: speak a single prediction, and your head will shatter into a thousand pieces! "
            "Even Duryodhana asked Sahadeva to pick the most auspicious time to begin the war, and Sahadeva truthfully revealed it. "
            "That unbearable burden explains why one prince knew the entire future but could never speak. "
            "Because..."
        ),
        "description": (
            "Prince Sahadeva knew every future tragedy of the Mahabharata, but if he spoke a single prophecy, his head would shatter. "
            "Discover the terrifying burden of the omniscient Pandava.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #mahabharata #sahadeva #pandavas #krishna #duryodhana #curse #ancienthistory"
        ),
        "tags": ["shorts", "mahabharata", "sahadeva", "pandavas", "krishna", "duryodhana", "3d animation", "animation", "hindu mythology"]
    },
    {
        "id": "short_05_eklavya_sacrifice",
        "title": "Why The Greatest Archer Cut Off His Own Thumb 🎯",
        "yt_title": "Why The Greatest Archer Cut Off His Own Thumb 🎯 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_05_eklavya_sacrifice"),
        "script": (
            "The greatest archer in the world was not Arjuna. "
            "It was a tribal boy named Eklavya who mastered the bow by practicing before a clay statue of Guru Dronacharya. "
            "One day, a barking dog disturbed his practice. "
            "Without harming the animal, Eklavya shot seven arrows into the dog's mouth in a split second, silencing it without drawing blood. "
            "Stunned by this impossible skill, Dronacharya realized Eklavya surpassed Arjuna. "
            "To protect his royal promise, the master asked for Eklavya's right thumb as Guru Dakshina. "
            "Without hesitating, Eklavya sliced off his thumb, proving why the greatest archer was not Arjuna. "
            "And still..."
        ),
        "description": (
            "The greatest archer who ever lived was not Arjuna—it was Eklavya. "
            "Witness the heart-wrenching Guru Dakshina that preserved Arjuna's supremacy forever.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #mahabharata #eklavya #dronacharya #arjuna #gurudakshina #archery #epic"
        ),
        "tags": ["shorts", "mahabharata", "eklavya", "dronacharya", "arjuna", "archery", "3d animation", "animation", "hindu mythology"]
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
        f"Style: MahabharataKinetic,Impact,78,{SUB_COLOR},&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,6,2,2,60,60,450,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    for start_t, end_t, txt in events:
        lines.append(f"Dialogue: 0,{fmt_ass(start_t)},{fmt_ass(end_t)},MahabharataKinetic,,0,0,0,,{txt}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def produce_mahabharata_short(cfg, index, total):
    short_dir = cfg["dir"]
    short_id = cfg["id"]
    output_mp4 = os.path.join(BASE_DIR, f"{short_id}.mp4")
    thumb_jpg = os.path.join(BASE_DIR, f"{short_id}_thumb.jpg")

    print(f"\n🎬 [{index}/{total}] PRODUCING MAHABHARATA SHORT: {cfg['title']}")

    if os.path.exists(output_mp4) and os.path.getsize(output_mp4) > 1000000:
        print(f"   ⏩ Already rendered: {output_mp4} ({os.path.getsize(output_mp4)/(1024*1024):.2f} MB)")
        return output_mp4, thumb_jpg

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
        "-ss", "00:00:02.0",
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
    print("🎬 PRODUCING 5 MAHABHARATA FACT SHORTS & UPLOADING TO YOUTUBE")
    print("=" * 60)

    results = []
    total = len(MAHABHARATA_SHORTS)
    for idx, cfg in enumerate(MAHABHARATA_SHORTS, 1):
        mp4, thumb = produce_mahabharata_short(cfg, idx, total)
        
        # Upload directly as PRIVATE
        print(f"   🚀 Uploading {cfg['yt_title']} as PRIVATE...")
        up_res = upload_youtube_short(
            video_path=mp4,
            title=cfg["yt_title"],
            description=cfg["description"],
            tags=cfg["tags"],
            privacy_status="private"
        )
        print(f"   Upload Result: {up_res}")
        results.append({
            "id": cfg["id"],
            "title": cfg["yt_title"],
            "mp4": mp4,
            "thumb": thumb,
            "upload": up_res
        })

    out_file = os.path.join(BASE_DIR, "mahabharata_upload_results.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print(f"🎉 ALL 5 MAHABHARATA SHORTS PRODUCED & UPLOADED! Results: {out_file}")
    print("=" * 60)
    for r in results:
        up = r["upload"]
        if up.get("success"):
            print(f"  ✅ {r['title']} -> {up.get('video_url')}")
        else:
            print(f"  ❌ {r['title']} -> {up.get('error')}")


if __name__ == "__main__":
    main()
