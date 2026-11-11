#!/usr/bin/env python3
"""
upload_ramayana_3d.py — Uploads Ramayana 3D Shorts 2-5 to YouTube as PRIVATE
"""

import os
import sys
import json

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts"))
from connectors.youtube_connector import upload_youtube_short

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOADS = [
    {
        "id": "short_02_gayatri_cipher",
        "video": os.path.join(BASE_DIR, "short_02_gayatri_cipher_3d.mp4"),
        "title": "The Hidden 24-Letter Code in Ramayana 📜 #Shorts",
        "description": (
            "Sage Valmiki hid a mathematical secret in the Ramayana thousands of years ago: "
            "every 1,000th verse starts with a letter of the Gayatri Mantra!\n\n"
            "Subscribe to @captonsumanth for more original 3D stories!\n\n"
            "#shorts #ramayana #animation #pixar #3danimation #hindumythology #valmiki"
        ),
        "tags": ["shorts", "ramayana", "gayatri mantra", "valmiki", "3d animation", "pixar", "disney", "ancient code", "hindu mythology"]
    },
    {
        "id": "short_03_ravana_violin",
        "video": os.path.join(BASE_DIR, "short_03_ravana_violin_3d.mp4"),
        "title": "Why Ravana Ripped Out His Own Vein 🎻 #Shorts",
        "description": (
            "Crushed under Mount Kailash by Lord Shiva's toe, Ravana ripped out his own vein "
            "to invent the Ravanahatha violin and chant the Shiva Tandava.\n\n"
            "Subscribe to @captonsumanth for more original 3D stories!\n\n"
            "#shorts #ramayana #ravana #shiva #3danimation #pixar #animation #mythology"
        ),
        "tags": ["shorts", "ramayana", "ravana", "lord shiva", "ravanahatha", "shiva tandava", "3d animation", "pixar", "disney"]
    },
    {
        "id": "short_04_indrajit_astras",
        "video": os.path.join(BASE_DIR, "short_04_indrajit_astras_3d.mp4"),
        "title": "The Only Mortal With 3 Supreme Astras ⚡ #Shorts",
        "description": (
            "Only one mortal warrior possessed Brahmastra, Vaishnavastra, and Pashupatastra: Meghanada (Indrajit). "
            "Discover how Shani Dev altered his astrological destiny.\n\n"
            "Subscribe to @captonsumanth for more original 3D stories!\n\n"
            "#shorts #ramayana #indrajit #meghanada #3danimation #pixar #mythology"
        ),
        "tags": ["shorts", "ramayana", "indrajit", "meghanada", "astras", "shani dev", "3d animation", "pixar", "disney"]
    },
    {
        "id": "short_05_bharata_penance",
        "video": os.path.join(BASE_DIR, "short_05_bharata_penance_3d.mp4"),
        "title": "The King Who Slept In A 3-Foot Pit 👑 #Shorts",
        "description": (
            "Offered the golden throne of Ayodhya, Prince Bharata refused it, placed Lord Rama's wooden sandals "
            "on the throne, and slept in a 3-foot dirt pit for 14 years.\n\n"
            "Subscribe to @captonsumanth for more original 3D stories!\n\n"
            "#shorts #ramayana #bharata #lordrama #ayodhya #3danimation #pixar #mythology"
        ),
        "tags": ["shorts", "ramayana", "bharata", "lord rama", "ayodhya", "paduka", "3d animation", "pixar", "disney"]
    }
]


def main():
    print("=" * 60)
    print("🚀 UPLOADING RAMAYANA 3D SHORTS 2-5 TO YOUTUBE (PRIVATE)")
    print("=" * 60)

    results = []
    for item in UPLOADS:
        print(f"\n📤 Uploading: {item['title']}...")
        if not os.path.exists(item["video"]):
            print(f"❌ Error: Video file not found: {item['video']}")
            continue

        res = upload_youtube_short(
            video_path=item["video"],
            title=item["title"],
            description=item["description"],
            tags=item["tags"],
            privacy_status="private"
        )
        print(f"   Result: {res}")
        results.append({
            "id": item["id"],
            "title": item["title"],
            "result": res
        })

    out_file = os.path.join(BASE_DIR, "upload_results_3d.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 60)
    print(f"🎉 ALL UPLOADS COMPLETED! Results saved to {out_file}")
    print("=" * 60)
    for r in results:
        res = r["result"]
        if res.get("status") == "success":
            print(f"  ✅ {r['title']} -> {res.get('url')}")
        else:
            print(f"  ❌ {r['title']} -> {res.get('error')}")


if __name__ == "__main__":
    main()
