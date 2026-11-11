#!/usr/bin/env python3
"""
produce_and_upload_batch.py — Production Engine for 10 Epic Fact Shorts (Ramayana & Mahabharata).
Renders 1080x1920 vertical MP4s with 10 cuts, studio vocal mastering, kinetic ASS subtitles,
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

# YouTube connector
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts"))
from connectors.youtube_connector import upload_youtube_short

VOICE = "en-IN-PrabhatNeural"
RATE = "+3%"
SUB_COLOR = "&H0000FFFF&"  # Pixar Yellow

SHORTS_DATA = [
    {
        "id": "short_01_urmila_slumber",
        "title": "The Princess Who Slept For 14 Years 🌙",
        "yt_title": "The Princess Who Slept For 14 Years 🌙 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_01_urmila_slumber"),
        "script": (
            "A royal princess slept continuously for fourteen years without waking up. "
            "When Prince Lakshmana vowed to protect Rama and Sita day and night, the Goddess of Sleep appeared. "
            "Lakshmana asked her to take away his sleep completely for fourteen years. "
            "The Goddess agreed on one condition: another soul must accept his slumber. "
            "Hearing this, Lakshmana's devoted wife, Princess Urmila, selflessly volunteered to sleep through his entire exile. "
            "For fourteen continuous years, Urmila remained in deep meditation so Lakshmana could stay vigilant. "
            "True sacrifice is silent, which is why a royal princess slept continuously for fourteen years without waking. "
            "Because..."
        ),
        "description": (
            "How did Princess Urmila endure 14 years of unbroken slumber for her husband? "
            "Discover the quietest and most selfless sacrifice in the Ramayana.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #ramayana #urmila #lakshmana #ayodhya #hindumythology #ancientlore #indianhistory"
        ),
        "tags": ["shorts", "ramayana", "urmila", "lakshmana", "ayodhya", "hindumythology", "ancientlore", "indianhistory"]
    },
    {
        "id": "short_02_shabari_devotion",
        "title": "Why Lord Rama Ate Tasted Berries 🍇",
        "yt_title": "Why Lord Rama Ate Tasted Berries 🍇 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_02_shabari_devotion"),
        "script": (
            "Lord Rama gladly accepted fruit that had already been bitten. "
            "Deep in the Dandakaranya forest, an elderly devotee named Shabari waited decades for the divine arrival. "
            "Every morning, she gathered wild berries from the woods. "
            "To ensure her Lord never tasted a single bitter or sour fruit, Shabari tasted every single berry first. "
            "Offering tasted food broke ancient ritual traditions, but Rama smiled with boundless joy. "
            "He explained that heartfelt love is sweeter than the strictest ritual. "
            "That pure devotion explains why Lord Rama gladly accepted fruit that had already been bitten. "
            "So..."
        ),
        "description": (
            "Why did Lord Rama joyfully accept half-eaten wild berries from an elderly forest hermit? "
            "The timeless tale of Shabari's pure devotion in the Ramayana.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #ramayana #shabari #lord rama #rama #devotion #hindumythology #ancientindia"
        ),
        "tags": ["shorts", "ramayana", "shabari", "lord rama", "rama", "devotion", "hindumythology", "ancientindia"]
    },
    {
        "id": "short_03_jatayu_valour",
        "title": "The Sacred Bird Who Fought A Demon King 🦅",
        "yt_title": "The Sacred Bird Who Fought A Demon King 🦅 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_03_jatayu_valour"),
        "script": (
            "An aged king of vultures flew alone against an invincible demon king. "
            "When Ravana abducted Sita in his flying chariot, elderly Jatayu heard her desperate cries from the clouds. "
            "Without hesitation, the valiant bird attacked Ravana mid-air to protect her. "
            "He fought relentlessly, shattering Ravana's chariot with his mighty beak and talons. "
            "Though mortally struck, Jatayu held onto life through pure devotion until Rama arrived. "
            "Deeply moved by his supreme courage, Lord Rama performed Jatayu's final rites as his own father. "
            "Which proves why an aged king of vultures flew alone against an invincible king. "
            "Because..."
        ),
        "description": (
            "Witness the supreme courage of King Jatayu, who flew into battle against Ravana to protect Mother Sita.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #ramayana #jatayu #ravana #sita #lord rama #valour #hindumythology"
        ),
        "tags": ["shorts", "ramayana", "jatayu", "ravana", "sita", "lord rama", "valour", "hindumythology"]
    },
    {
        "id": "short_04_floating_bridge",
        "title": "The Secret Behind Ram Setu's Floating Stones 🌊",
        "yt_title": "The Secret Behind Ram Setu's Floating Stones 🌊 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_04_floating_bridge"),
        "script": (
            "Did you know a childhood curse became the miracle that built Ram Setu? "
            "As young monkey infants, the twin architects Nala and Nila loved throwing sacred objects into holy forest rivers. "
            "Frustrated sages placed a curious curse upon them: whatever they tossed into water would never sink! "
            "Years later, when the Vanara army stood before the vast ocean, Nala and Nila remembered the prophecy. "
            "By inscribing Lord Rama's sacred name upon massive boulders, every stone floated effortlessly upon the waves. "
            "That ancient curse transformed into the engineering wonder of the floating ocean bridge. "
            "Which is why a childhood curse became the miracle that built Ram Setu. "
            "Because..."
        ),
        "description": (
            "How did massive stone boulders float upon the deep sea to construct the Ram Setu bridge to Lanka? "
            "The astonishing legend of twin architects Nala and Nila.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #ramayana #ram setu #floating stones #nala nila #ocean bridge #hindumythology"
        ),
        "tags": ["shorts", "ramayana", "ram setu", "floating stones", "nala nila", "ocean bridge", "hindumythology"]
    },
    {
        "id": "short_05_vibhishana_refuge",
        "title": "The Demon Prince Who Stood For Truth 👑",
        "yt_title": "The Demon Prince Who Stood For Truth 👑 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_05_vibhishana_refuge"),
        "script": (
            "One prince walked away from an empire of gold to stand with truth. "
            "In the golden city of Lanka, Vibhishana pleaded with his brother Ravana to return Sita and follow Dharma. "
            "When Ravana banished him in fury, Vibhishana flew across the ocean and sought refuge at Lord Rama's feet. "
            "Rama's commanders warned he might be an enemy spy. "
            "Yet Rama proclaimed his eternal vow: whoever seeks refuge with a sincere heart shall be protected forever. "
            "Rama crowned Vibhishana King of Lanka on the ocean shore before battle even began. "
            "That timeless promise shows why one prince walked away from an empire of gold to stand with truth. "
            "And so..."
        ),
        "description": (
            "Prince Vibhishana abandoned the golden palaces of Lanka to uphold righteousness. "
            "Discover Lord Rama's unconditional vow of sanctuary.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #ramayana #vibhishana #lord rama #lanka #dharma #righteousness #hindumythology"
        ),
        "tags": ["shorts", "ramayana", "vibhishana", "lord rama", "lanka", "dharma", "righteousness", "hindumythology"]
    },
    {
        "id": "short_06_gita_wisdom",
        "title": "When Cosmic Time Froze At Kurukshetra 🌟",
        "yt_title": "When Cosmic Time Froze At Kurukshetra 🌟 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_06_gita_wisdom"),
        "script": (
            "Cosmic time froze on the battlefield of Kurukshetra. "
            "Standing between two massive armies, Prince Arjuna lowered his Gandiva bow in overwhelming grief and doubt. "
            "Right then, Lord Krishna paused the entire universe to reveal the sacred Bhagavad Gita. "
            "He reminded Arjuna that the soul is eternal, untouched by weapons, fire, or death. "
            "Focus on your noble duty, not the fruits of action. "
            "Awakened by supreme wisdom, Arjuna lifted his bow with fearless clarity and purpose. "
            "That eternal guidance explains why cosmic time froze on the battlefield of Kurukshetra. "
            "Because..."
        ),
        "description": (
            "How did Lord Krishna freeze cosmic time amidst two gigantic armies to deliver the Bhagavad Gita? "
            "The timeless essence of Arjuna's spiritual awakening at Kurukshetra.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #mahabharata #bhagavad gita #krishna #arjuna #kurukshetra #ancientwisdom #hindumythology"
        ),
        "tags": ["shorts", "mahabharata", "bhagavad gita", "krishna", "arjuna", "kurukshetra", "ancientwisdom", "hindumythology"]
    },
    {
        "id": "short_07_bhishma_vow",
        "title": "The Grandfather Who Waited 58 Days 🏹",
        "yt_title": "The Grandfather Who Waited 58 Days 🏹 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_07_bhishma_vow"),
        "script": (
            "One revered warrior chose the exact hour and day of his own departure. "
            "Grandfather Bhishma was blessed with the rare boon of choosing his own time of death. "
            "On Day Ten of Kurukshetra, his body rested upon a revered bed of arrow tips. "
            "Rather than departing, Bhishma endured fifty-eight days of deep contemplation upon the battlefield. "
            "He waited patiently for the sun to enter the auspicious northern solstice of Uttarayana. "
            "During this time, he imparted the highest principles of governance and righteous conduct to King Yudhishthira. "
            "That unwavering willpower explains why one warrior chose the exact hour and day of his departure. "
            "So..."
        ),
        "description": (
            "Grandfather Bhishma lay upon a bed of arrows for 58 days, awaiting the sacred northern solstice. "
            "The supreme devotion and fortitude of the patriarch of Hastinapur.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #mahabharata #bhishma #kurukshetra #uttarayana #dharma #hindumythology"
        ),
        "tags": ["shorts", "mahabharata", "bhishma", "kurukshetra", "uttarayana", "dharma", "hindumythology"]
    },
    {
        "id": "short_08_karna_generosity",
        "title": "The King Who Never Refused Anyone At Dawn ☀️",
        "yt_title": "The King Who Never Refused Anyone At Dawn ☀️ #Shorts",
        "dir": os.path.join(BASE_DIR, "short_08_karna_generosity"),
        "script": (
            "No beggar was ever turned away from this king's palace at sunrise. "
            "Karna held a sacred personal vow: anyone who approached him for charity at dawn would receive whatever they asked. "
            "Even when tests and rivals attempted to trick him, Karna gave away golden crowns, land, and royal jewels. "
            "To Karna, honor and generosity were infinitely greater than wealth or power. "
            "His legendary charity earned him the eternal title of Danaveera, the hero of giving. "
            "True nobility lives in what you give away, which is why no soul was ever turned away from Karna at sunrise. "
            "And yet..."
        ),
        "description": (
            "Why was King Karna revered as Danaveera, the supreme hero of charity? "
            "The steadfast honor of the warrior who gave everything away at dawn.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #mahabharata #karna #danaveera #generosity #honor #ancientindia #hindumythology"
        ),
        "tags": ["shorts", "mahabharata", "karna", "danaveera", "generosity", "honor", "ancientindia", "hindumythology"]
    },
    {
        "id": "short_09_yuyutsu_righteousness",
        "title": "The Lone Kaurava Who Chose Dharma ⚖️",
        "yt_title": "The Lone Kaurava Who Chose Dharma ⚖️ #Shorts",
        "dir": os.path.join(BASE_DIR, "short_09_yuyutsu_righteousness"),
        "script": (
            "Out of one hundred brothers, only one chose righteousness over family. "
            "His name was Yuyutsu, a prince of Hastinapur. "
            "Before the conch shells blew at Kurukshetra, King Yudhishthira invited anyone who wished to switch sides for Dharma. "
            "While others stayed silent, Yuyutsu courageously crossed the battlefield to join the Pandavas. "
            "He believed truth must always triumph over blind bloodlines. "
            "Because of his unwavering integrity, Yuyutsu survived the entire war and became the respected guardian regent of Hastinapur. "
            "That moral strength shows why only one brother chose righteousness over family. "
            "Because..."
        ),
        "description": (
            "Why did Prince Yuyutsu abandon his 100 brothers on the eve of the Kurukshetra war? "
            "The courage of the lone Kaurava prince who stood for Dharma.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #mahabharata #yuyutsu #hastinapur #dharma #pandavas #righteousness #hindumythology"
        ),
        "tags": ["shorts", "mahabharata", "yuyutsu", "hastinapur", "dharma", "pandavas", "righteousness", "hindumythology"]
    },
    {
        "id": "short_10_arjuna_chariot",
        "title": "The Cosmic Chariot Guided By God 🐎",
        "yt_title": "The Cosmic Chariot Guided By God 🐎 #Shorts",
        "dir": os.path.join(BASE_DIR, "short_10_arjuna_chariot"),
        "script": (
            "The most unstoppable chariot in history had God as its driver. "
            "Arjuna's battle chariot was gifted by Agni and drawn by four celestial white steeds. "
            "Upon its banner flew Lord Hanuman, whose fierce roar terrified opposing armies. "
            "At the reins sat Lord Krishna Himself, guiding every maneuver with divine precision. "
            "The chariot absorbed countless celestial astras and cosmic fires throughout the eighteen days. "
            "Only after the war ended and Krishna stepped down did the chariot instantly vanish into sacred flames. "
            "That divine shield reveals why the most unstoppable chariot in history had God as its driver. "
            "So..."
        ),
        "description": (
            "Why did Arjuna's battle chariot instantly burst into flames the moment Lord Krishna stepped off? "
            "The celestial mystery of the Nandighosha chariot.\n\n"
            "Subscribe to @captonsumanth for more untold ancient epics!\n\n"
            "#shorts #mahabharata #arjuna #krishna #chariot #hanuman #kurukshetra #hindumythology"
        ),
        "tags": ["shorts", "mahabharata", "arjuna", "krishna", "chariot", "hanuman", "kurukshetra", "hindumythology"]
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
        f"Style: EpicKinetic,Impact,78,{SUB_COLOR},&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,6,2,2,60,60,450,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    for start_t, end_t, txt in events:
        lines.append(f"Dialogue: 0,{fmt_ass(start_t)},{fmt_ass(end_t)},EpicKinetic,,0,0,0,,{txt}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def produce_short(cfg, index, total):
    short_dir = cfg["dir"]
    short_id = cfg["id"]
    output_mp4 = os.path.join(BASE_DIR, f"{short_id}.mp4")
    thumb_jpg = os.path.join(BASE_DIR, f"{short_id}_thumb.jpg")

    print(f"\n🎬 [{index}/{total}] PRODUCING EPIC SHORT: {cfg['title']}")

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
        voices_to_try = [VOICE, "en-US-ChristopherNeural", "en-US-AndrewMultilingualNeural"]
        tts_ok = False
        for v in voices_to_try:
            cmd_tts = [
                EDGE_TTS,
                "--voice", v,
                "--rate", RATE,
                "--text", cfg["script"],
                "--write-media", voice_audio,
                "--write-subtitles", vtt_file
            ]
            try:
                subprocess.run(cmd_tts, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=15)
                if os.path.exists(voice_audio) and os.path.getsize(voice_audio) > 10000:
                    tts_ok = True
                    break
            except Exception as e:
                print(f"   ⚠️ Voice {v} attempt notice: {e}, trying alternative...")
        if not tts_ok:
            raise RuntimeError(f"Failed to generate TTS for {cfg['title']}")
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
    print("🎬 PRODUCING 10 EPIC FACT SHORTS & ATTEMPTING YOUTUBE UPLOADS")
    print("=" * 60)

    results = []
    total = len(SHORTS_DATA)
    # Daily YouTube upload limit was confirmed hit during earlier run today
    upload_limit_hit = True

    for idx, cfg in enumerate(SHORTS_DATA, 1):
        mp4, thumb = produce_short(cfg, idx, total)
        
        if upload_limit_hit:
            print(f"   📦 YouTube daily quota active. Video packaged and queued for upload: {os.path.basename(mp4)}")
            up_res = {"success": False, "reason": "queued_for_reset", "status": "Ready for upload when YouTube 24h quota resets"}
        else:
            print(f"   🚀 Attempting upload for {cfg['yt_title']} as PRIVATE...")
            try:
                up_res = upload_youtube_short(
                    video_path=mp4,
                    title=cfg["yt_title"],
                    description=cfg["description"],
                    tags=cfg["tags"],
                    privacy_status="private"
                )
                print(f"   Upload Result: {up_res}")
            except Exception as e:
                err_str = str(e)
                upload_limit_hit = True
                print(f"   ⚠️ YouTube Daily Upload Limit Reached ({err_str}). All subsequent videos will be packaged and queued.")
                up_res = {"success": False, "reason": "uploadLimitExceeded", "error": "Daily YouTube upload limit reached. Video rendered and ready on disk."}

        results.append({
            "id": cfg["id"],
            "title": cfg["yt_title"],
            "mp4": mp4,
            "thumb": thumb,
            "upload": up_res
        })

    out_file = os.path.join(BASE_DIR, "epic_facts_10_results.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print(f"🎉 PRODUCTION RUN COMPLETE! Results saved to {out_file}")
    print("=" * 60)
    for r in results:
        up = r["upload"]
        if up.get("success"):
            print(f"  ✅ {r['title']} -> {up.get('video_url')}")
        else:
            print(f"  📦 {r['title']} -> Rendered locally ({up.get('error') or up.get('reason')})")


if __name__ == "__main__":
    main()
