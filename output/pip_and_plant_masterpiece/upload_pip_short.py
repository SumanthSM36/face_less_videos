#!/usr/bin/env python3
"""
upload_pip_short.py — Uploads Pip & The Iron Blossom short to YouTube as Private.
"""

import os
import sys

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
CONNECTORS_DIR = os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts/connectors")
sys.path.insert(0, CONNECTORS_DIR)

from youtube_connector import upload_youtube_short

VIDEO_FILE = "/Users/sumanth/Downloads/New/output/pip_and_plant_masterpiece/pip_and_the_iron_blossom.mp4"
TITLE = "Pip & The Iron Blossom: Even in Rust, Love Blooms 🤖🌸 #shorts"

DESCRIPTION = """In a dead world of rusted steel and silence, a tiny scrap robot named Pip found the impossible: a single fragile sprout glowing with bioluminescent life.

While the older machines ignored it, Pip carried it to the highest peak and shielded it through acid storms, giving it the last drop of clean moisture from his coolant tank.

When dawn broke, life exploded across the gray horizon. A colossal golden blossom erupted into the sky, covering the wasteland in wildflowers and starlight.

Proving that even in a world of cold rust and forgotten scrap, the smallest spark of devotion can bloom an entire universe.

💬 What did Pip's story make you feel? Share your thoughts below! 👇
🔔 Subscribe to @captonsumanth for more heartwarming animated stories and mind-expanding shorts! ✨

#shorts #animation #pixarstyle #scifiart #robotlove #piptherobot #wholesomestories #cgi #3danimation #invisibleindian"""

TAGS = [
    "shorts", "animation", "pixar", "robot", "wholesome",
    "scifi", "3d animation", "story short", "pip", "invisible indian",
    "cgi short", "heartwarming", "emotional stories"
]

def main():
    print(f"Uploading '{TITLE}' to YouTube as PRIVATE...")
    res = upload_youtube_short(
        video_path=VIDEO_FILE,
        title=TITLE,
        description=DESCRIPTION,
        tags=TAGS,
        privacy_status="private"
    )
    if res.get("status") == "success":
        vid = res.get("video_id")
        url = res.get("video_url")
        print("\n==========================================")
        print("🎉 UPLOAD SUCCESSFUL! 🎉")
        print(f"Video ID:  {vid}")
        print(f"Watch URL: {url}")
        print(f"Privacy:   PRIVATE")
        print("==========================================")
    else:
        print(f"Upload failed: {res.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
