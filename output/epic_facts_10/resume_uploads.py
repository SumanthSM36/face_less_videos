#!/usr/bin/env python3
"""
resume_uploads.py — Resume YouTube uploads for any pending videos once daily quota resets.
"""

import os
import sys
import json
import time

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts"))
from connectors.youtube_connector import upload_youtube_short

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
RESULTS_FILE = os.path.join(BASE_DIR, "epic_facts_10_results.json")

def main():
    print("=" * 60)
    print("🚀 RESUMING YOUTUBE UPLOADS FOR PENDING EPIC SHORTS")
    print("=" * 60)

    if not os.path.exists(RESULTS_FILE):
        print(f"❌ Error: {RESULTS_FILE} not found.")
        return

    with open(RESULTS_FILE, "r") as f:
        records = json.load(f)

    updated = False
    for r in records:
        up = r.get("upload", {})
        if up.get("success"):
            print(f"  ⏩ Already uploaded: {r['title']} -> {up.get('video_url')}")
            continue

        mp4 = r["mp4"]
        if not os.path.exists(mp4):
            print(f"  ❌ File missing: {mp4}")
            continue

        print(f"\n📤 Uploading {r['title']}...")
        try:
            up_res = upload_youtube_short(
                video_path=mp4,
                title=r["title"],
                description=f"Ancient Indian Epic Fact Short. Subscribe to @captonsumanth for more!\n\n#shorts #ramayana #mahabharata #hindumythology",
                tags=["shorts", "ramayana", "mahabharata", "ancientlore", "hindumythology"],
                privacy_status="private"
            )
            print(f"   Result: {up_res}")
            r["upload"] = up_res
            updated = True
            time.sleep(3.0)
        except Exception as e:
            err = str(e)
            print(f"   ⚠️ Upload failed: {err}")
            if "uploadLimitExceeded" in err:
                print("   🛑 YouTube daily upload limit is still active. Please try again later.")
                break

    if updated:
        with open(RESULTS_FILE, "w") as f:
            json.dump(records, f, indent=2)
        print(f"\n💾 Updated results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    main()
