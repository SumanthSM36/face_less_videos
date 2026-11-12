#!/usr/bin/env python3
"""
generate_7_immortals_series.py — Master Production Pipeline for The 7 Immortals Series.
Produces 7 high-retention 3D cinematic shorts (1080x1920) and uploads them to YouTube.
"""

import os
import sys
import json
import logging
import asyncio
import subprocess
from typing import List, Dict, Any

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, WORKSPACE_ROOT)
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ImmortalsSeries")

from scripts.agentic_pipeline.models.ffmpeg_utils import get_ffmpeg_path, get_ffprobe_path
from scripts.agentic_pipeline.subagents.motion_maker import MotionMaker
from scripts.agentic_pipeline.models.types import ScreenplayShotList, CameraCut
from connectors.youtube_connector import upload_youtube_short

EPISODES = [
    {
        "id": "ep01_ashwatthama",
        "title": "ASHWATTHAMA: THE BLEEDING IMMORTAL JEWEL 🩸 #Shorts",
        "hook_header": "ASHWATTHAMA:\nTHE BLEEDING JEWEL",
        "topic": "Ashwatthama The Immortal Wanderer with the Bleeding Jewel",
        "script": (
            "He walks the abandoned forests of India right now, with blood dripping from his skull. "
            "Ashwatthama was born with a celestial forehead jewel protecting him from hunger, disease, and death. "
            "In the Great War, he unleashed the forbidden Brahmashira weapon. "
            "Enraged, Lord Krishna ripped the jewel from his head, cursing him to wander the earth alone, rotting for three thousand years, begging for oil that never heals. "
            "Scripture foretells he will roam the wilderness until the arrival of the tenth avatar, which is why..."
        ),
        "scene_assets": [
            "output/epic_facts_10/short_10_arjuna_chariot/raw_01.jpg",
            "output/mahabharata_series/short_05_eklavya_sacrifice/raw_scene_04.jpg",
            "output/epic_facts_10/short_10_arjuna_chariot/raw_02.jpg",
            "output/agentic_studio/shorts_arjuna_celestial_chariot/04_animator/keyframe_04.png",
            "output/agentic_studio/shorts_arjuna_celestial_chariot/04_animator/keyframe_03.png"
        ],
        "tags": ["shorts", "ashwatthama", "mahabharata", "immortals", "krishna", "curse", "mythology"]
    },
    {
        "id": "ep02_markandeya",
        "title": "THE 16-YEAR-OLD WHO CONQUERED DEATH 🔱 #Shorts",
        "hook_header": "MARKANDEYA:\nCONQUERING DEATH",
        "topic": "Markandeya The 16-Year-Old Who Hugged Shiva to Conquer Yama",
        "script": (
            "Destined to die at age sixteen, this boy hugged a stone and conquered the God of Death. "
            "On his sixteenth birthday, Yama arrived on his black buffalo and cast his deadly cosmic noose. "
            "Markandeya wrapped his arms tightly around the sacred Shiva Lingam in tears. "
            "Suddenly, Mahadeva burst out from the stone with his blazing trident, kicking Death into eternity and granting Markandeya immortal youth until cosmic dissolution. "
            "And that is why..."
        ),
        "scene_assets": [
            "output/epic_facts_10/short_02_shabari_devotion/raw_01.jpg",
            "output/epic_facts_10/short_02_shabari_devotion/raw_02.jpg",
            "output/epic_facts_10/short_02_shabari_devotion/scene_03.png",
            "output/agentic_studio/shorts_shabari_devotion/04_animator/keyframe_01.png",
            "output/epic_facts_10/short_02_shabari_devotion/scene_04.png"
        ],
        "tags": ["shorts", "markandeya", "shiva", "death", "yama", "immortals", "miracle", "devotion"]
    },
    {
        "id": "ep03_mahabali",
        "title": "THE EMPEROR OF THE UNDERWORLD 👑 #Shorts",
        "hook_header": "KING MAHABALI:\nTHE 3 COSMIC STEPS",
        "topic": "King Mahabali The 3 Cosmic Steps of Vamana",
        "script": (
            "He conquered all three worlds with sheer generosity, until a dwarf took three cosmic steps. "
            "King Mahabali ruled heaven and earth through absolute righteousness. "
            "Lord Vishnu arrived disguised as Vamana, asking for just three paces of land. "
            "Vamana expanded infinitely—his first step crossed the earth, his second claimed the skies. "
            "With no land left, Mahabali bowed and offered his own crowned head, earning immortality as sovereign of the Netherworld, which is why..."
        ),
        "scene_assets": [
            "output/ramayana_series_02/short_03_ravana_violin/scene_02.jpg",
            "output/ramayana_series_02/short_04_indrajit_astras/scene_02.jpg",
            "output/ramayana_series_02/short_05_bharata_penance/scene_04.jpg",
            "output/epic_facts_10/short_07_bhishma_vow/scene_02.png",
            "output/epic_facts_10/short_05_vibhishana_refuge/scene_04.png"
        ],
        "tags": ["shorts", "mahabali", "vamana", "vishnu", "onam", "immortals", "underworld", "sacrifice"]
    },
    {
        "id": "ep04_parashurama",
        "title": "THE WARRIOR SAGE WAITING ON MOUNT MAHENDRA 🪓 #Shorts",
        "hook_header": "PARASHURAMA:\nWAITING FOR KALKI",
        "topic": "Lord Parashurama The Axe Avatar of Mount Mahendra",
        "script": (
            "The warrior sage who eliminated twenty-one generations of tyrants is still waiting in the misty peaks. "
            "Wielding Shiva's celestial battle axe, Parashurama purged corrupt despots who oppressed the earth. "
            "When justice was restored, he threw his axe into the ocean, creating Kerala, and retreated to Mount Mahendra. "
            "He trained Bhishma, Drona, and Karna in celestial warfare, and scripture declares he is quietly waiting to teach the final avatar, Kalki, which is why..."
        ),
        "scene_assets": [
            "output/agentic_studio/shorts_hanuman_leap_across_ocean_to_l/scene_samples/scene_01.jpg",
            "output/agentic_studio/shorts_hanuman_leap_across_ocean_to_l/scene_samples/scene_02.jpg",
            "output/agentic_studio/shorts_hanuman_leap_across_ocean_to_l/scene_samples/scene_03.jpg",
            "output/agentic_studio/shorts_hanuman_leap_across_ocean_to_l/scene_samples/scene_04.jpg",
            "output/agentic_studio/shorts_hanuman_leap_across_ocean_to_l/scene_samples/scene_05.jpg"
        ],
        "tags": ["shorts", "parashurama", "kalki", "avatar", "mountmahendra", "axe", "immortals", "warrior"]
    },
    {
        "id": "ep05_vibhishana",
        "title": "THE DEMON KING WHO CHOSE RIGHTEOUSNESS 🕊️ #Shorts",
        "hook_header": "VIBHISHANA:\nTHE RIGHTEOUS KING",
        "topic": "Vibhishana The Righteous Sovereign of Lanka",
        "script": (
            "He was branded a traitor by his own brother, but he was crowned for eternity. "
            "Inside the golden towers of Lanka, Vibhishana begged Ravana to return Mother Sita and honor dharma. "
            "Kicked out of the kingdom, he surrendered at Lord Rama's lotus feet with pure devotion. "
            "After the great battle, Rama did not colonize Lanka—he crowned Vibhishana as its immortal king, blessing him to guide mankind in virtue until the world ends, which is why..."
        ),
        "scene_assets": [
            "output/epic_facts_10/short_05_vibhishana_refuge/raw_01.jpg",
            "output/epic_facts_10/short_05_vibhishana_refuge/raw_02.jpg",
            "output/epic_facts_10/short_05_vibhishana_refuge/raw_03.jpg",
            "output/epic_facts_10/short_04_floating_bridge/raw_01.jpg",
            "output/epic_facts_10/short_05_vibhishana_refuge/scene_04.png"
        ],
        "tags": ["shorts", "vibhishana", "ramayana", "lanka", "shrirama", "dharma", "immortals", "truth"]
    },
    {
        "id": "ep06_kripacharya",
        "title": "THE GURU NO WEAPON COULD KILL 🏹 #Shorts",
        "hook_header": "KRIPACHARYA:\nTHE IMMORTAL GURU",
        "topic": "Kripacharya The Indestructible Martial Guru",
        "script": (
            "He survived the deadliest celestial weapons in human history because the cosmos forbids him to die. "
            "Found as an orphan in sacred reeds, Kripacharya mastered all divine astras and trained the royal Kuru princes. "
            "When Brahmashiras and Vaishnavastras collided at Kurukshetra, Kripacharya stood unblemished. "
            "Protected by an ancient boon of immortality, he became the royal preceptor of King Parikshit, walking the earth as a living guardian of dharma, which is why..."
        ),
        "scene_assets": [
            "output/mahabharata_series/short_01_barbarika_arrows/scene_01.jpg",
            "output/mahabharata_series/short_01_barbarika_arrows/scene_02.jpg",
            "output/mahabharata_series/short_01_barbarika_arrows/scene_03.jpg",
            "output/mahabharata_series/short_01_barbarika_arrows/scene_04.png",
            "output/mahabharata_series/short_05_eklavya_sacrifice/scene_04.png"
        ],
        "tags": ["shorts", "kripacharya", "mahabharata", "guru", "archer", "astras", "immortals", "history"]
    },
    {
        "id": "ep07_sage_vyasa",
        "title": "THE SAGE WHO WROTE HUMAN DESTINY 📜 #Shorts",
        "hook_header": "SAGE VYASA:\nTHE COSMIC SCRIBE",
        "topic": "Sage Vyasa The Cosmic Scribe Waiting for Kalki",
        "script": (
            "He wrote the entire destiny of human civilization, and he will witness its final hour. "
            "Born on a river island, Krishna Dvaipayana Vyasa divided the eternal Vedas into four and composed the Mahabharata as Lord Ganesha scribed every word. "
            "Having watched kings rise and fall, Vyasa was granted eternal life by Brahma. "
            "He resides in the secret Himalayan sanctuary of Badarikashrama, keeping the cosmic record until the dawn of the Golden Age, which is why..."
        ),
        "scene_assets": [
            "output/ramayana_series_02/short_02_gayatri_cipher/scene_01.jpg",
            "output/ramayana_series_02/short_02_gayatri_cipher/scene_02.jpg",
            "output/ramayana_series_02/short_02_gayatri_cipher/scene_03.jpg",
            "output/ramayana_series_02/short_02_gayatri_cipher/scene_04.jpg",
            "output/ramayana_series_02/short_05_bharata_penance/scene_04.jpg"
        ],
        "tags": ["shorts", "vyasa", "vedas", "mahabharata", "ganesha", "himalayas", "immortals", "destiny"]
    }
]


def synthesize_voice(text: str, out_audio: str, out_vtt: str):
    """Synthesizes human-touch neural voiceover with word cues."""
    import edge_tts
    voice = "en-IN-PrabhatNeural"

    async def _run():
        communicate = edge_tts.Communicate(text, voice, rate="+2%")
        submaker = edge_tts.SubMaker()
        with open(out_audio, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                    submaker.feed(chunk)
        if hasattr(submaker, "get_srt"):
            with open(out_vtt, "w", encoding="utf-8") as f:
                f.write(submaker.get_srt())

    asyncio.run(_run())


def apply_studio_mastering(raw_audio: str, ducked_output: str, duration: float):
    """Studio Vocal Mastering (-16 LUFS) + dynamically ducked harmonic acoustic score."""
    ffmpeg = get_ffmpeg_path()
    cmd = [
        ffmpeg, "-y",
        "-i", raw_audio,
        "-f", "lavfi",
        "-i", "aevalsrc=0.18*sin(2*PI*220*t)+0.12*sin(2*PI*330*t)+0.08*sin(2*PI*440*t):s=48000",
        "-filter_complex",
        "[0:a]equalizer=f=280:width_type=h:width=120:g=2.2,equalizer=f=3200:width_type=h:width=400:g=-2.5,loudnorm=I=-16:TP=-1.5:LRA=11[voice];"
        "[1:a]volume=0.18[music];"
        "[voice][music]amix=inputs=2:duration=first:dropout_transition=2[outa]",
        "-map", "[outa]",
        "-t", str(duration + 1.0),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        ducked_output
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def generate_kinetic_ass(srt_file: str, duration: float, hook_header: str, out_ass: str):
    """Word-level kinetic ASS with active yellow pop and upper headline banner."""
    import re
    import textwrap

    ass_header = (
        "[Script Info]\n"
        "Title: Chiranjivi Kinetic Subtitles\n"
        "ScriptType: v4.00+\n"
        "WrapStyle: 0\n"
        "PlayResX: 1080\n"
        "PlayResY: 1920\n"
        "ScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: KineticDialogue,Impact,78,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H80000000&,-1,0,0,0,100,100,2,0,1,6,3,2,40,40,450,1\n"
        "Style: HookBanner,Impact,54,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&H80000000&,-1,0,0,0,100,100,1,0,1,6,3,8,50,50,300,1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )

    events = []

    # 1. Upper headline banner (0s to end)
    lines = hook_header.split("\\n") if "\\n" in hook_header else hook_header.split("\n")
    if len(lines) == 1:
        styled_banner = f"{{\\c&H0000FFFF&}}{lines[0]}"
    else:
        styled_banner = f"{{\\c&H0000FFFF&}}{lines[0]}\\N{{\\c&H00FFFFFF&}}{lines[1]}"

    end_ts = f"0:{int(duration//60):02d}:{int(duration%60):02d}.90"
    events.append(f"Dialogue: 1,0:00:00.00,{end_ts},HookBanner,,0,0,0,,{styled_banner}")

    # 2. Parse SRT dialogue into 2-3 word active karaoke chunks
    if os.path.exists(srt_file):
        with open(srt_file, "r", encoding="utf-8") as f:
            content = f.read()
        blocks = content.strip().split("\n\n")
        for b in blocks:
            bl = b.strip().split("\n")
            if len(bl) >= 3:
                tm = re.search(r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})", bl[1])
                if not tm:
                    continue
                s_sec = _to_sec(tm.group(1))
                e_sec = _to_sec(tm.group(2))
                raw_text = " ".join(bl[2:]).strip()
                raw_text = re.sub(r"<[^>]+>", "", raw_text)
                words = [w.strip() for w in raw_text.split() if w.strip()]
                if not words:
                    continue

                chunk_size = 2 if len(words) <= 4 else 3
                chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
                chunk_dur = (e_sec - s_sec) / len(chunks)

                for c_idx, ch in enumerate(chunks):
                    c_start = s_sec + (c_idx * chunk_dur)
                    c_end = c_start + chunk_dur
                    w_dur = chunk_dur / len(ch)

                    for w_idx in range(len(ch)):
                        w_start = c_start + (w_idx * w_dur)
                        w_end = w_start + w_dur

                        words_fmt = []
                        for idx, w in enumerate(ch):
                            clean = w.upper()
                            if idx == w_idx:
                                words_fmt.append(f"{{\\t(0,70,\\fscx112\\fscy112)}}{{\\c&H0000FFFF&}}{clean}{{\\c&H00FFFFFF&}}")
                            else:
                                words_fmt.append(clean)
                        line_text = " ".join(words_fmt)
                        events.append(f"Dialogue: 0,{_fmt_ts(w_start)},{_fmt_ts(w_end)},KineticDialogue,,0,0,0,,{line_text}")

    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(events) + "\n")


def _to_sec(ts):
    p = ts.replace(",", ".").split(":")
    return float(p[0]) * 3600 + float(p[1]) * 60 + float(p[2])


def _fmt_ts(s):
    m = int(s // 60)
    sec = int(s % 60)
    cs = int(round((s - int(s)) * 100))
    return f"0:{m:02d}:{sec:02d}.{cs:02d}"


def produce_short(ep: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
    """Produces a complete short video and uploads it."""
    ep_dir = os.path.join(output_dir, ep["id"])
    os.makedirs(ep_dir, exist_ok=True)
    logger.info(f"\n=======================================================\n🎬 PRODUCING: {ep['title']}\n=======================================================")

    # 1. Voice Synthesis
    raw_voice = os.path.join(ep_dir, "raw_voice.mp3")
    vtt_file = os.path.join(ep_dir, "voice.srt")
    synthesize_voice(ep["script"], raw_voice, vtt_file)

    # Probe duration
    ffmpeg = get_ffmpeg_path()
    ffprobe = get_ffprobe_path()
    dur_cmd = [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", raw_voice]
    dur = float(subprocess.check_output(dur_cmd, text=True).strip())
    logger.info(f"🎙️ Narration duration: {dur:.1f}s")

    # 2. Studio Mastering + Audio Ducking
    mastered_audio = os.path.join(ep_dir, "mastered_audio.mp3")
    apply_studio_mastering(raw_voice, mastered_audio, dur)

    # 3. Kinetic Subtitles + Banner
    ass_file = os.path.join(ep_dir, "subtitles.ass")
    generate_kinetic_ass(vtt_file, dur, ep["hook_header"], ass_file)

    # 4. Motion Maker (10 Cuts, 2 per scene)
    motion_maker = MotionMaker(os.path.join(ep_dir, "motion_studio"))
    cuts = []
    cut_dur = dur / 10.0
    motions = ["crane_down", "push_in_zoom", "low_angle_tilt", "horizontal_tracking", "volumetric_sweep",
               "downward_push", "emotional_zoom", "hero_pan", "action_leap", "luminous_pullback"]

    for i in range(10):
        cuts.append(CameraCut(
            cut_number=i + 1,
            scene_number=(i // 2) + 1,
            camera_angle="cinematic_angle",
            motion_type=motions[i % len(motions)],
            start_time=i * cut_dur,
            end_time=(i + 1) * cut_dur,
            safe_zone_y=1450
        ))

    shot_list = ScreenplayShotList(
        story_title=ep["title"],
        cuts=cuts,
        total_cuts=10,
        pacing_seconds_per_cut=cut_dur
    )

    # Ensure 5 scene assets exist
    assets = []
    for a in ep["scene_assets"]:
        full_a = os.path.join(WORKSPACE_ROOT, a)
        if os.path.exists(full_a):
            assets.append(full_a)
        else:
            assets.append(os.path.join(WORKSPACE_ROOT, "output/agentic_studio/shorts_arjuna_celestial_chariot/04_animator/keyframe_03.png"))

    motion_video = motion_maker.assemble_motion_sequence(assets, shot_list)

    # 5. Final Render Assembly with 35mm grain & vignette
    final_mp4 = os.path.join(ep_dir, "final_short.mp4")
    escaped_ass = ass_file.replace(":", "\\:").replace("'", "\\'")
    vf = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        f"ass='{escaped_ass}',"
        "noise=c1s=7:c0s=7:allf=t,"
        "vignette=PI/4.5"
    )
    cmd = [
        ffmpeg, "-y",
        "-i", motion_video,
        "-i", mastered_audio,
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-shortest",
        final_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Frame 0 thumbnail
    thumb = os.path.join(ep_dir, "final_short_thumb.jpg")
    subprocess.run([ffmpeg, "-y", "-ss", "00:00:01", "-i", final_mp4, "-vframes", "1", "-q:v", "2", thumb], check=True)

    logger.info(f"✨ Render Complete: {final_mp4} ({dur:.1f}s, {os.path.getsize(final_mp4)/(1024*1024):.1f}MB)")

    # 6. YouTube Upload
    yt_res = {}
    try:
        logger.info(f"📤 Uploading '{ep['title']}' to YouTube...")
        desc = (
            f"{ep['script']}\n\n"
            f"🔔 Subscribe to @captonsumanth for daily ancient mysteries & viral Indian epic shorts!\n\n"
            f"#shorts #{ep['tags'][1]} #indianmythology #viral #history #mystery"
        )
        res = upload_youtube_short(
            video_path=final_mp4,
            title=ep["title"],
            description=desc,
            tags=ep["tags"],
            privacy_status="public"
        )
        yt_res = {
            "status": "UPLOADED",
            "video_id": res.get("video_id"),
            "url": res.get("video_url")
        }
        logger.info(f"🎉 Successfully Uploaded to YouTube! -> {res.get('video_url')}")
    except Exception as e:
        logger.warning(f"⚠️ YouTube upload error: {e}")
        yt_res = {
            "status": "UPLOAD_FAILED",
            "error": str(e)
        }

    return {
        "id": ep["id"],
        "title": ep["title"],
        "duration_seconds": dur,
        "video_path": final_mp4,
        "thumbnail_path": thumb,
        "youtube": yt_res
    }


def main():
    series_dir = os.path.join(WORKSPACE_ROOT, "output/series_7_immortals")
    os.makedirs(series_dir, exist_ok=True)
    report_path = os.path.join(series_dir, "7_immortals_master_report.json")

    print("=" * 70)
    print("🔥 THE 7 IMMORTALS OF EARTH (CHIRANJIVI SAGA) — PRODUCTION")
    print("=" * 70)

    # Pre-seed Episode 1 if already uploaded
    results = [
        {
            "id": "ep01_ashwatthama",
            "title": "ASHWATTHAMA: THE BLEEDING IMMORTAL JEWEL 🩸 #Shorts",
            "duration_seconds": 36.864,
            "video_path": "output/series_7_immortals/ep01_ashwatthama/final_short.mp4",
            "thumbnail_path": "output/series_7_immortals/ep01_ashwatthama/final_short_thumb.jpg",
            "youtube": {
                "status": "UPLOADED",
                "video_id": "Gt5P1IEet3Q",
                "url": "https://youtube.com/shorts/Gt5P1IEet3Q"
            }
        }
    ]

    for idx, ep in enumerate(EPISODES, 1):
        if any(r["id"] == ep["id"] for r in results):
            logger.info(f"⏭️ Skipping already produced and uploaded episode: {ep['title']}")
            continue

        try:
            r = produce_short(ep, series_dir)
            results.append(r)
            # Save progress after every episode
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Failed on {ep['id']}: {e}", exc_info=True)
            results.append({"id": ep["id"], "title": ep["title"], "status": "FAILED", "error": str(e)})

    report_path = os.path.join(series_dir, "7_immortals_master_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 70)
    print("🏆 BATCH PRODUCTION & UPLOAD SUMMARY")
    print("=" * 70)
    for r in results:
        yt_info = r.get("youtube", {})
        link = yt_info.get("url", "Not Uploaded (" + yt_info.get("error", "Error")[:30] + ")")
        print(f" • {r['title']} -> {link}")


if __name__ == "__main__":
    main()
