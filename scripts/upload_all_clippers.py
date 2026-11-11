#!/usr/bin/env python3
"""
upload_all_clippers.py — Automated Uploader for All YouTube Clipped Shorts.
Uploads all 4 viral clipped shorts directly to the authenticated YouTube channel.
"""

import os
import sys
import json
import logging
from typing import List, Dict, Any

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ClipperUploader")

from connectors.youtube_connector import get_youtube_service, upload_youtube_short

CLIPPED_SHORTS: List[Dict[str, Any]] = [
    {
        "id": "speed_short_01",
        "title": "HOW TO BEAT A ROBBERY (SPEED UNDERCOVER) 😱 #shorts",
        "video_path": os.path.join(WORKSPACE_ROOT, "output/agentic_studio/clipping_viral_video_highlights/short_01_and_that_s_chat/final_clipped_short.mp4"),
        "description": (
            "Speed shows how to beat a robbery while undercover in the Spiderman suit in NYC!\n\n"
            "🔔 Subscribe for more daily viral clips & stream highlights!\n\n"
            "#shorts #ishowspeed #viral #funny #spiderman #speed"
        ),
        "tags": ["shorts", "ishowspeed", "viral", "funny", "spiderman", "speed", "trending"]
    },
    {
        "id": "speed_short_02",
        "title": "SPEED MEETS THE VILLAIN ACTOR 😱 #shorts",
        "video_path": os.path.join(WORKSPACE_ROOT, "output/agentic_studio/clipping_viral_video_highlights/short_02_oh_brother/final_clipped_short.mp4"),
        "description": (
            "Speed meets the villain actor on a rooftop before going undercover as Spiderman!\n\n"
            "🔔 Subscribe for more daily viral clips & stream highlights!\n\n"
            "#shorts #ishowspeed #viral #funny #spiderman #rooftop #speed"
        ),
        "tags": ["shorts", "ishowspeed", "viral", "funny", "spiderman", "trending", "speed"]
    },
    {
        "id": "speed_short_03",
        "title": "WHY DIDN'T YOU SHOW UP?! (SPEED HEATED) 😱 #shorts",
        "video_path": os.path.join(WORKSPACE_ROOT, "output/agentic_studio/clipping_viral_video_highlights/short_03_if_you_don_t_why_you_never_sh/final_clipped_short.mp4"),
        "description": (
            "Speed confronts his crew while undercover in NYC!\n\n"
            "🔔 Subscribe for more daily viral clips & stream highlights!\n\n"
            "#shorts #ishowspeed #viral #funny #spiderman #speed #confrontation"
        ),
        "tags": ["shorts", "ishowspeed", "viral", "funny", "spiderman", "trending", "speed"]
    },
    {
        "id": "avengers_doomsday",
        "title": "COUNTDOWN TO AVENGERS: DOOMSDAY 🤯 #shorts",
        "video_path": os.path.join(WORKSPACE_ROOT, "output/agentic_studio/clipping_viral_video_highlights/final_clipped_short.mp4"),
        "description": (
            "Countdown to Avengers: Doomsday! The multiverse returns on Disney+.\n\n"
            "🔔 Subscribe for more Marvel movie updates & cinematic shorts!\n\n"
            "#shorts #marvel #avengers #avengersdoomsday #doctorstrange #mcu"
        ),
        "tags": ["shorts", "marvel", "avengers", "avengers doomsday", "mcu", "doctor strange"]
    }
]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Upload all clipped shorts to YouTube")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "unlisted", "private"])
    args = parser.parse_args()

    print("=" * 70)
    print("📤 AUTOMATED YOUTUBE UPLOADER — VIRAL CLIPPERS")
    print("=" * 70)

    results = []

    for idx, short in enumerate(CLIPPED_SHORTS, start=1):
        v_path = short["video_path"]
        title = short["title"]
        print(f"\n[{idx}/{len(CLIPPED_SHORTS)}] Uploading: {title}...")
        print(f"     Path: {v_path}")

        if not os.path.exists(v_path):
            print(f"❌ Video file does not exist: {v_path}")
            results.append({"id": short["id"], "status": "FILE_NOT_FOUND"})
            continue

        try:
            res = upload_youtube_short(
                video_path=v_path,
                title=title,
                description=short["description"],
                tags=short["tags"],
                privacy_status=args.privacy
            )
            print(f"✅ Success! YouTube Video ID: {res.get('id')}")
            print(f"   URL: https://youtube.com/shorts/{res.get('id')}")
            results.append({"id": short["id"], "status": "UPLOADED", "youtube_id": res.get("id"), "url": f"https://youtube.com/shorts/{res.get('id')}"})
        except Exception as e:
            err_msg = str(e)
            if "uploadLimitExceeded" in err_msg:
                print(f"⚠️ YouTube Quota Error: Daily channel upload limit exceeded for today.")
                print(f"   YouTube resets upload limits 24 hours after your last bulk uploads.")
                results.append({"id": short["id"], "status": "LIMIT_EXCEEDED", "error": "uploadLimitExceeded"})
                break
            else:
                print(f"❌ Upload failed: {err_msg[:200]}")
                results.append({"id": short["id"], "status": "ERROR", "error": err_msg})

    print("\n" + "=" * 70)
    print("📊 UPLOAD SUMMARY:")
    for r in results:
        print(f" - {r['id']}: {r['status']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
