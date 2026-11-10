#!/usr/bin/env python3
"""
render_ramayana_series.py — Master Production Engine for 5 Ramayana Fact Shorts.
Uses authentic Public Domain classical masterworks (Raja Ravi Varma & Mewar manuscripts),
Ken Burns 3D camera pan/zoom, algorithmic Indian Tanpura harmonic drone,
word-burst kinetic safe-zone captions, and cinematic 35mm grading.
"""

import os
import re
import sys
import subprocess
import urllib.request

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
FFMPEG = os.path.join(WORKSPACE_ROOT, ".venv/bin/ffmpeg")
EDGE_TTS = os.path.join(WORKSPACE_ROOT, ".venv/bin/edge-tts")
OUTPUT_BASE = os.path.abspath(os.path.dirname(__file__))

SHORTS_DATA = [
    {
        "id": "short_01_ram_setu",
        "title": "The 7,000-Year Mystery of Ram Setu 🌊",
        "yt_title": "The 7,000-Year Mystery of Ram Setu 🌊 #shorts",
        "description": "How did a thirty-mile bridge of floating stones cross the ocean thousands of years ago? Geological core samples and NASA satellite imaging reveal shocking alignments with the Valmiki Ramayana.\n\nSubscribe to @captonsumanth for more intriguing mysteries and facts! 🧐\n\n#shorts #ramayana #ramsetu #historyfacts #indianhistory #invisibleindian #ancientmysteries",
        "tags": ["shorts", "ramayana", "ram setu", "history facts", "indian history", "invisible indian", "ancient mysteries", "adams bridge"],
        "script": (
            "How did a thirty-mile bridge of floating stones cross the ocean thousands of years ago? "
            "In the Ramayana, the Vanara architects Nala and Nila carved sacred symbols into porous limestone boulders, causing them to float upon the deep sea. "
            "Modern satellite imaging by NASA revealed a thirty-kilometer chain of natural limestone shoals connecting India and Sri Lanka. "
            "Geological core samples confirmed the corals are less than four thousand years old, but the underlying boulders date back over seven thousand years. "
            "Meaning ancient engineering and sacred lore may be recounting the exact same historical marvel... "
            "Which is why the world still wonders..."
        ),
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/e/ea/Adams_Bridge_aerial.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/8d/AdamsBridge02-NASA.jpg/1280px-AdamsBridge02-NASA.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/b/b1/Raja_Ravi_Varma%2C_Sree_Rama_Crossing_Sarayu_river.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a7/Battle_at_Lanka%2C_Ramayana%2C_Udaipur%2C_1649-53.jpg/1280px-Battle_at_Lanka%2C_Ramayana%2C_Udaipur%2C_1649-53.jpg"
        ]
    },
    {
        "id": "short_02_ravana_10_heads",
        "title": "The Secret Behind Ravana's 10 Heads 👑",
        "yt_title": "The Secret Behind Ravana's 10 Heads 👑 #shorts",
        "description": "Did the demon king Ravana actually possess ten physical human heads? Ancient Vedic scholars reveal the profound spiritual and psychological meaning behind Dashanatha's ten heads.\n\nSubscribe to @captonsumanth for more intriguing mysteries and facts! 🧐\n\n#shorts #ramayana #ravana #ancientwisdom #mythologyfacts #invisibleindian #vedas",
        "tags": ["shorts", "ramayana", "ravana", "ancient wisdom", "mythology facts", "invisible indian", "vedas", "philosophy"],
        "script": (
            "Did the demon king Ravana actually possess ten physical human heads? "
            "According to ancient Vedic scholars, Dashanatha’s ten heads were not a physical deformity. "
            "They represented his mastery over the four Vedas and the six sacred Shastras. "
            "Each head also symbolized the ten faculties of human intellect: intellect, mind, ego, memory, anger, pride, lust, greed, jealousy, and delusion. "
            "By severing one head in penance to Lord Shiva, Ravana claimed total dominion over his ego. "
            "Yet it was ego itself that ultimately destroyed him. "
            "Proving why scholars still debate..."
        ),
        "images": [
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9a/Fight_between_Rama_and_Ravana_%28cropped%29.jpg/1280px-Fight_between_Rama_and_Ravana_%28cropped%29.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5c/130_Ramakien_Murals_%289150183848%29.jpg/1280px-130_Ramakien_Murals_%289150183848%29.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e6/This_painting_depicts_Kumbhakarna%2C_brother_of_Ravana.jpg/1280px-This_painting_depicts_Kumbhakarna%2C_brother_of_Ravana.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ef/Jatayu_Attacks_Ravana_to_Save_Sita_and_Shatters_his_Chariot_-_early_18th-century.jpg/1280px-Jatayu_Attacks_Ravana_to_Save_Sita_and_Shatters_his_Chariot_-_early_18th-century.jpg"
        ]
    },
    {
        "id": "short_03_hanuman_forgotten_power",
        "title": "Why Hanuman Forgot His Own Superpowers 🐒",
        "yt_title": "Why Hanuman Forgot His Own Superpowers 🐒 #shorts",
        "description": "The strongest entity in the cosmos was once tricked into forgetting his own power. Discover why the ancient Rishis placed a sacred curse upon infant Hanuman.\n\nSubscribe to @captonsumanth for more intriguing mysteries and facts! 🧐\n\n#shorts #ramayana #hanuman #hanumanji #bajrangbali #mythologyfacts #invisibleindian",
        "tags": ["shorts", "ramayana", "hanuman", "hanumanji", "bajrangbali", "mythology facts", "invisible indian", "hinduism"],
        "script": (
            "The strongest warrior in the cosmos was once tricked into forgetting his own power. "
            "As an infant, Hanuman saw the blazing sun and leapt into the sky, mistaking it for a ripe golden fruit. "
            "Fearing cosmic chaos, Lord Indra struck him with a thunderbolt. "
            "To balance his limitless divine strength, the assembly of Rishis placed a sacred curse upon him. "
            "Hanuman would completely forget his omnipotent power—until an elder reminded him of his true destiny. "
            "Which is why on the shores of the ocean, Jambavan had to awaken the sleeping titan... "
            "Reminding us how..."
        ),
        "images": [
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1b/Hanuman_fetches_the_herb-bearing_mountain%2C_in_a_print_from_the_Ravi_Varma_Press%2C_1910%27s.jpg/1280px-Hanuman_fetches_the_herb-bearing_mountain%2C_in_a_print_from_the_Ravi_Varma_Press%2C_1910%27s.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/9/97/Lanka_Dahan.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/0/01/HANUMAN_LIFTS_HILL.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/0/0d/Maruti_Skandharudh_Ramlaxman.jpg"
        ]
    },
    {
        "id": "short_04_kumbhakarna_sleep",
        "title": "Kumbhakarna's Slumber: A Single Mispronounced Word 😴",
        "yt_title": "Kumbhakarna's Slumber: A Single Mispronounced Word 😴 #shorts",
        "description": "The giant Kumbhakarna was meant to conquer the heavens—until one mispronounced letter doomed him forever. The untold boon story from the Ramayana.\n\nSubscribe to @captonsumanth for more intriguing mysteries and facts! 🧐\n\n#shorts #ramayana #kumbhakarna #storytelling #mythologyfacts #invisibleindian #funfacts",
        "tags": ["shorts", "ramayana", "kumbhakarna", "storytelling", "mythology facts", "invisible indian", "fun facts", "ancient legends"],
        "script": (
            "The giant Kumbhakarna was meant to conquer the heavens—until one mispronounced letter doomed him. "
            "After a thousand years of severe tapasya, Lord Brahma appeared to grant the giant any boon. "
            "Kumbhakarna prepared to demand Indra-asana—the sovereign throne of the heavens. "
            "Terrified of his impending reign, the Devas begged Goddess Saraswati to intervene. "
            "She descended onto his giant tongue for a split second, twisting his words into Nidra-asana—the desire for endless sleep. "
            "When Kumbhakarna realized his mistake, Brahma granted him wakefulness for only one day every six months. "
            "Which explains why..."
        ),
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/8/82/Kumbhakarna%2C_tricked_by_the_gods_into_asking_Brahma_for_the_boon_of_interminable_sleep%2C_slumbers_in_the_magnificent_dwelling_prepared_for_him_at_Ravana.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/d/df/The_Demon_Kumbhkaran_finally_wakes_up_and_eats_%286125069010%29.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/a4/Kumbhakarna%2C_the_giant_brother_of_Ravana.jpg/1280px-Kumbhakarna%2C_the_giant_brother_of_Ravana.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e2/The_Demon_Kumbhakarna_Is_Defeated_by_Rama_and_Lakshmana_1.jpg/1280px-The_Demon_Kumbhakarna_Is_Defeated_by_Rama_and_Lakshmana_1.jpg"
        ]
    },
    {
        "id": "short_05_lakshmana_sleepless_vow",
        "title": "The Warrior Who Did Not Sleep for 14 Years ⚔️",
        "yt_title": "The Warrior Who Did Not Sleep for 14 Years ⚔️ #shorts",
        "description": "How did Lakshmana defeat an invincible demon that even the gods could not kill? The incredible 14-year sleepless vow of Lakshmana and Urmila.\n\nSubscribe to @captonsumanth for more intriguing mysteries and facts! 🧐\n\n#shorts #ramayana #lakshmana #indrajit #ancientwarriors #mythologyfacts #invisibleindian",
        "tags": ["shorts", "ramayana", "lakshmana", "indrajit", "ancient warriors", "mythology facts", "invisible indian", "heroic stories"],
        "script": (
            "How did Lakshmana defeat an invincible demon that even the gods could not kill? "
            "Ravana’s son Indrajit possessed a cosmic boon: he could only be slain by someone who had not slept for fourteen consecutive years. "
            "On the first night of exile, Nidra Devi, the goddess of sleep, approached Lakshmana in the dark forest. "
            "Lakshmana begged her to leave him so he could guard Rama and Sita without blinking for fourteen years. "
            "The goddess agreed, transferring his sleep to his devoted wife Urmila back in Ayodhya. "
            "Making Lakshmana the solitary warrior destined to break Indrajit’s invincibility. "
            "Showing how supreme sacrifice..."
        ),
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/1/17/Fall_of_Laxmanai.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/9/99/Rama_vanavas.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/84/Ravi_Varma-Rama-breaking-bow.jpg/1280px-Ravi_Varma-Rama-breaking-bow.jpg",
            "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/95/Ram_Rajyabhishek.jpg/1280px-Ram_Rajyabhishek.jpg"
        ]
    }
]

VOICE = "en-US-ChristopherNeural"


def run_cmd(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stdout}")
    return p.stdout


def download_file(url, target_path):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        with open(target_path, "wb") as f:
            f.write(resp.read())


def generate_voice_and_captions(text, voice, out_audio, out_ass, temp_dir):
    out_vtt = os.path.join(temp_dir, "speech.vtt")
    cmd_tts = [
        EDGE_TTS,
        "--voice", voice,
        "--rate", "+4%",
        "--text", text,
        "--write-media", out_audio,
        "--write-subtitles", out_vtt
    ]
    run_cmd(cmd_tts)

    with open(out_vtt, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.findall(
        r"(\d+:\d+:\d+[\.,]\d+)\s*-->\s*(\d+:\d+:\d+[\.,]\d+)\s*\n(.*?)(?=\n\n|\n\d+|\Z)",
        content,
        re.DOTALL
    )

    def parse_t(ts):
        ts = ts.replace(",", ".")
        parts = ts.split(":")
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])

    def fmt_time(t):
        hrs = int(t // 3600)
        mins = int((t % 3600) // 60)
        secs = int(t % 60)
        cs = int(round((t - int(t)) * 100))
        if cs >= 100:
            cs = 99
        return f"{hrs:d}:{mins:02d}:{secs:02d}.{cs:02d}"

    entries = []
    for s_str, e_str, raw_text in blocks:
        s_sec = parse_t(s_str)
        e_sec = parse_t(e_str)
        words = raw_text.strip().split()
        if not words:
            continue
        chunk_size = 3
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        c_dur = (e_sec - s_sec) / max(len(chunks), 1)
        for idx, ch in enumerate(chunks):
            cs = s_sec + idx * c_dur
            ce = cs + c_dur
            entries.append((cs, ce, " ".join(ch).upper()))

    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,82,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,6,2,2,60,60,400,1

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
    return 30.0


def produce_short(item, index, total):
    short_id = item["id"]
    title = item["title"]
    short_dir = os.path.join(OUTPUT_BASE, short_id)
    os.makedirs(short_dir, exist_ok=True)
    final_output = os.path.join(OUTPUT_BASE, f"{short_id}.mp4")

    # If already rendered and valid, skip
    if os.path.exists(final_output) and os.path.getsize(final_output) > 1024 * 1024:
        print(f"\n[{index}/{total}] ⚡ Already rendered: {final_output} ({os.path.getsize(final_output)/(1024*1024):.2f} MB). Skipping.")
        return final_output

    print("\n" + "=" * 60)
    print(f"[{index}/{total}] PRODUCING: {title}")
    print("=" * 60)

    # 1. Synthesize audio & subtitles via edge-tts CLI
    voice_mp3 = os.path.join(short_dir, "voice.mp3")
    captions_ass = os.path.join(short_dir, "captions.ass")
    print("📢 Synthesizing narration and generating safe-zone kinetic subtitles...")
    generate_voice_and_captions(item["script"], VOICE, voice_mp3, captions_ass, short_dir)
    total_dur = get_audio_duration(voice_mp3)
    print(f"   Duration: {total_dur:.2f}s")

    # 2. Download 4 high-res artworks
    print("🖼️  Fetching classical public-domain masterworks...")
    local_images = []
    for img_idx, url in enumerate(item["images"], 1):
        target_img = os.path.join(short_dir, f"scene_{img_idx:02d}.jpg")
        if not os.path.exists(target_img):
            download_file(url, target_img)
        local_images.append(target_img)

    # 3. Render 4 Ken Burns animated scenes (1080x1920)
    num_scenes = len(local_images)
    scene_dur = total_dur / num_scenes
    print(f"🎬 Rendering {num_scenes} animated 3D Ken Burns cuts ({scene_dur:.2f}s each)...")

    clips = []
    for idx, img_path in enumerate(local_images, 1):
        clip_path = os.path.join(short_dir, f"clip_{idx:02d}.mp4")
        fps = 30
        frames = int(scene_dur * fps)

        if idx % 2 == 1:
            z_expr = "min(zoom+0.0016,1.26)"
        else:
            z_expr = "if(lte(zoom,1.0),1.26,max(1.001,zoom-0.0016))"

        vf = (
            f"scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,"
            f"zoompan=z='{z_expr}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={fps}"
        )

        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", img_path,
            "-vf", vf,
            "-t", f"{scene_dur:.2f}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
            "-an", clip_path
        ]
        run_cmd(cmd)
        clips.append(clip_path)

    # 4. Concatenate scenes
    concat_txt = os.path.join(short_dir, "concat.txt")
    with open(concat_txt, "w") as f:
        for c in clips:
            f.write(f"file '{c}'\n")

    raw_video = os.path.join(short_dir, "raw_video.mp4")
    cmd_cat = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-t", f"{total_dur:.2f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        raw_video
    ]
    run_cmd(cmd_cat)

    # 5. Mix Algorithmic Indian Classical Tanpura Soundbed
    mixed_audio = os.path.join(short_dir, "mixed_audio.mp3")
    print("🎵 Mixing algorithmic Indian Tanpura harmonic drone & ducking...")
    tanpura_tone = (
        "0.022*sin(2*PI*146.83*t)+"
        "0.018*sin(2*PI*220.0*t)+"
        "0.015*sin(2*PI*293.66*t)+"
        "0.010*sin(2*PI*369.99*t)"
    )
    bgm_filter = (
        f"aevalsrc='{tanpura_tone}':d={total_dur}[bgm];"
        "[0:a][bgm]amix=inputs=2:duration=first:weights=1.0 0.20[out]"
    )
    cmd_audio = [
        FFMPEG, "-y",
        "-i", voice_mp3,
        "-filter_complex", bgm_filter,
        "-map", "[out]",
        mixed_audio
    ]
    run_cmd(cmd_audio)

    # 6. Final Pass: 35mm grain, color curves, lens vignette, burned subtitles
    print("⚡ Applying golden mythological grading, 35mm grain, vignette & kinetic captions...")
    escaped_ass = captions_ass.replace(":", "\\:").replace("'", "\\'")
    vf_chain = (
        "eq=contrast=1.14:saturation=1.22:brightness=-0.02,"
        "noise=alls=4:allf=t+u,"
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
        final_output
    ]
    run_cmd(cmd_final)

    size_mb = os.path.getsize(final_output) / (1024 * 1024)
    print(f"✅ RENDERED: {final_output} ({size_mb:.2f} MB, {total_dur:.2f}s)")
    return final_output


def main():
    print("=" * 60)
    print("🕉️  RAMAYANA 5-PART FACT SHORTS PRODUCTION ENGINE")
    print("=" * 60)

    rendered_files = []
    total = len(SHORTS_DATA)

    for idx, item in enumerate(SHORTS_DATA, 1):
        out_f = produce_short(item, idx, total)
        rendered_files.append((item, out_f))

    print("\n" + "=" * 60)
    print("🎉 ALL 5 RAMAYANA SHORTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    for it, p in rendered_files:
        size = os.path.getsize(p) / (1024 * 1024)
        print(f"  • {it['title']} -> {p} ({size:.2f} MB)")


if __name__ == "__main__":
    main()
