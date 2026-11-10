#!/usr/bin/env python3
"""
upload_ramayana_series.py — Batch Uploader for the 5-Part Ramayana Fact Shorts Series.
Uploads each video to YouTube as 'private' with rich descriptions, SEO tags, and summaries.
"""

import os
import sys
import json
import time

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
CONNECTORS_DIR = os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts/connectors")
sys.path.insert(0, CONNECTORS_DIR)

from youtube_connector import upload_youtube_short

SHORTS_METADATA = [
    {
        "file": os.path.join(os.path.dirname(__file__), "short_01_ram_setu.mp4"),
        "title": "The 7,000-Year Mystery of Ram Setu: Science vs Lore 🌊 #shorts",
        "description": (
            "How did a thirty-mile bridge of floating stones cross the ocean thousands of years ago?\n\n"
            "In the ancient Valmiki Ramayana, the divine Vanara architects Nala and Nila inscribed sacred symbols onto porous limestone boulders, allowing an entire army to march across the sea to Lanka.\n\n"
            "Fast forward to modern times: NASA satellite imagery and geological core drillings revealed a 30-kilometer chain of natural limestone shoals between Rameswaram, India, and Mannar Island, Sri Lanka. While the upper coral layers date to roughly 4,000 years ago, geological carbon-dating of the underlying boulders dates back over 7,000 years—directly matching the historical antiquity of the Treta Yuga.\n\n"
            "Could ancient engineering and sacred lore be describing the exact same prehistoric engineering feat?\n\n"
            "💬 What do you think: A natural geological phenomenon, or remnants of ancient engineering? Let us know in the comments!\n\n"
            "🔔 Subscribe to @captonsumanth for more untold history, ancient mysteries, and mind-bending facts! 🧐"
        ),
        "tags": [
            "shorts", "ramayana", "ram setu", "adams bridge", "ancient mysteries",
            "indian history", "sanatan dharma", "archaeology", "history facts",
            "invisible indian", "floating stones", "nasa"
        ]
    },
    {
        "file": os.path.join(os.path.dirname(__file__), "short_02_ravana_10_heads.mp4"),
        "title": "The Hidden Meaning Behind Ravana's 10 Heads 👑 #shorts",
        "description": (
            "Did the demon king Ravana actually possess ten physical human heads?\n\n"
            "While popular folklore often depicts Dashanatha with ten literal heads, ancient Vedic scholars and philosophers reveal a far more profound allegorical reality:\n\n"
            "1️⃣ Mastery of Ancient Knowledge: Ravana was one of the greatest scholars of all time, mastering the 4 sacred Vedas and the 6 Vedic Shastras.\n"
            "2️⃣ The 10 Facets of Human Ego: His ten heads symbolize the ten complex mental faculties and egoistic impulses: Kama (Lust), Krodha (Anger), Moha (Delusion), Lobha (Greed), Mada (Pride), Matsarya (Jealousy), Manas (Mind), Buddhi (Intellect), Chitta (Memory), and Ahankara (Ego).\n\n"
            "By severing one of his heads in supreme penance to Lord Shiva, Ravana demonstrated ultimate sacrifice. Yet in the end, it was untamed ego that led to the downfall of golden Lanka.\n\n"
            "💬 Was Ravana a fallen devotee or the ultimate villain of human pride? Share your thoughts below!\n\n"
            "🔔 Subscribe to @captonsumanth for more mythological philosophy, ancient wisdom, and deep dives! 🧐"
        ),
        "tags": [
            "shorts", "ramayana", "ravana", "mythology facts", "ancient wisdom",
            "vedas", "philosophy", "hinduism", "indian mythology", "invisible indian",
            "dashanatha", "spiritual"
        ]
    },
    {
        "file": os.path.join(os.path.dirname(__file__), "short_03_hanuman_forgotten_power.mp4"),
        "title": "Why Hanuman Was Cursed to Forget His Superpowers 🐒 #shorts",
        "description": (
            "The strongest entity in the cosmos was once tricked into forgetting his own power.\n\n"
            "As an infant, the son of the wind god Vayu saw the blazing golden sun and mistaking it for a sweet ripe fruit, leapt thousands of leagues into the cosmic sky to consume it. Terrified that cosmic equilibrium would collapse, Lord Indra struck the child with his thunderbolt (Vajra).\n\n"
            "Although the gods granted infant Hanuman boundless boons—immortality, invulnerability, and shape-shifting—his playful antics began disrupting the sacred rituals of forest hermits.\n\n"
            "To maintain balance in the universe, the assembly of Rishis placed a gentle protective curse upon him: Hanuman would completely forget his omnipotent power, until an elder or devotee reminded him of his true identity.\n\n"
            "It wasn’t until the Vanara army stood defeated on the shores of the vast southern ocean that Jambavan awakened the sleeping titan within him.\n\n"
            "💬 Have you ever doubted your own potential until someone reminded you who you are?\n\n"
            "🔔 Subscribe to @captonsumanth for more inspiring legends and ancient facts! 🧐"
        ),
        "tags": [
            "shorts", "ramayana", "hanuman", "hanumanji", "bajrangbali",
            "mythology facts", "ancient legends", "hindu mythology", "invisible indian",
            "jambavan", "ramayan", "shorts feed"
        ]
    },
    {
        "file": os.path.join(os.path.dirname(__file__), "short_04_kumbhakarna_sleep.mp4"),
        "title": "Kumbhakarna's Slumber: A Single Mispronounced Word 😴 #shorts",
        "description": (
            "The colossal giant Kumbhakarna was meant to conquer the heavens—until one mispronounced letter changed his destiny forever.\n\n"
            "After enduring a thousand years of grueling penance (Tapasya), Lord Brahma appeared before the mighty demon warrior, ready to grant him any boon he requested. Kumbhakarna intended to demand 'Indra-asana'—the supreme celestial throne of the gods.\n\n"
            "Terrified that Kumbhakarna's boundless strength would subjugate the three worlds, the Devas rushed to Goddess Saraswati, pleading for her divine intervention.\n\n"
            "As Kumbhakarna opened his mouth to speak, the Goddess of Speech manifested on his tongue for a fraction of a second, gracefully twisting his words into 'Nidra-asana'—the desire for endless, unbroken slumber.\n\n"
            "Brahma granted the boon instantly: 'Tathastu!' When Kumbhakarna broke down realizing his tragic slip of the tongue, Brahma softened the decree: he would sleep for six months at a time, awakening for just one single day of feasting.\n\n"
            "💬 What's the most costly slip of the tongue in human history? Drop your thoughts below!\n\n"
            "🔔 Subscribe to @captonsumanth for intriguing historical stories and mythological gems! 🧐"
        ),
        "tags": [
            "shorts", "ramayana", "kumbhakarna", "storytelling", "ancient facts",
            "mythology stories", "hinduism", "invisible indian", "brahma",
            "saraswati", "ramayan facts"
        ]
    },
    {
        "file": os.path.join(os.path.dirname(__file__), "short_05_lakshmana_sleepless_vow.mp4"),
        "title": "The Warrior Who Did Not Sleep for 14 Years ⚔️ #shorts",
        "description": (
            "How did Prince Lakshmana defeat Meghanada (Indrajit), an invincible warrior that even the gods could not vanquish?\n\n"
            "Indrajit possessed a formidable cosmic boon granted by Brahma: he could only be slain on the battlefield by a warrior who had not slept for fourteen consecutive years.\n\n"
            "On the very first night of Lord Rama’s exile into the dark forest, Nidra Devi (the Goddess of Sleep) appeared before Lakshmana. Knowing danger lurked in the wilderness, Lakshmana made an extraordinary sacrifice: he begged the Goddess of Sleep to leave his body for the entirety of their 14-year banishment so he could stand guard over Rama and Sita day and night without closing his eyes.\n\n"
            "The Goddess agreed on one condition—someone else had to bear his sleep. Lakshmana's devoted wife, Princess Urmila, took upon herself both her own sleep and Lakshmana’s sleep for 14 uninterrupted years in Ayodhya.\n\n"
            "Because of this supreme sacrifice, Lakshmana became the only warrior in existence with the power to pierce Indrajit’s invulnerability.\n\n"
            "💬 True strength often lies in silent sacrifice. What did you think of Urmila and Lakshmana's vow?\n\n"
            "🔔 Subscribe to @captonsumanth for more profound historical and mythological insights! 🧐"
        ),
        "tags": [
            "shorts", "ramayana", "lakshmana", "indrajit", "urmila",
            "ancient warriors", "epic stories", "sanatan dharma", "mythology facts",
            "invisible indian", "valmiki ramayana"
        ]
    }
]


def main():
    print("=" * 65)
    print("🚀 BATCH UPLOADING 5 RAMAYANA SHORTS TO YOUTUBE (PRIVATE)")
    print("=" * 65)

    results = []
    total = len(SHORTS_METADATA)

    for idx, item in enumerate(SHORTS_METADATA, 1):
        f_path = item["file"]
        title = item["title"]
        desc = item["description"]
        tags = item["tags"]

        print(f"\n[{idx}/{total}] Uploading: {title}...")
        if not os.path.exists(f_path):
            print(f"❌ Video file missing: {f_path}")
            continue

        size_mb = os.path.getsize(f_path) / (1024 * 1024)
        print(f"    File: {f_path} ({size_mb:.2f} MB)")

        try:
            res = upload_youtube_short(
                video_path=f_path,
                title=title,
                description=desc,
                tags=tags,
                privacy_status="private"
            )
            res["title"] = title
            results.append(res)
            print(f"    ✅ Uploaded successfully! Video ID: {res['video_id']}")
            print(f"    🔗 URL: {res['video_url']}")
            # Small 2s delay between API upload calls
            time.sleep(2)
        except Exception as e:
            print(f"    ❌ Upload failed: {e}")

    print("\n" + "=" * 65)
    print("🎉 BATCH UPLOAD COMPLETE!")
    print("=" * 65)
    for r in results:
        print(f"  • {r['title']}")
        print(f"    Video URL : {r['video_url']}")
        print(f"    Studio    : https://studio.youtube.com/video/{r['video_id']}/edit\n")

    summary_file = os.path.join(os.path.dirname(__file__), "upload_results.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to: {summary_file}")


if __name__ == "__main__":
    main()
