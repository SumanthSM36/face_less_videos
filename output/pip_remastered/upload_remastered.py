#!/usr/bin/env python3
"""
upload_remastered.py — Uploads the Remastered Pip Short to YouTube as Private.
"""

import os
import sys

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
CONNECTORS_DIR = os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts/connectors")
sys.path.insert(0, CONNECTORS_DIR)

from youtube_connector import upload_youtube_short

VIDEO_FILE = "/Users/sumanth/Downloads/New/output/pip_remastered/the_robot_who_found_mankinds_last_words.mp4"
TITLE = "The Robot Who Found Mankind's Last Words 🤖🌸 (Remastered) #shorts"

DESCRIPTION = """Wandering through a wasteland of cold iron, Pip searched for the answer that haunted his circuits: Who made me... and where did they go?

Until buried beneath the ruins, he uncovered an impossible spark: a single fragile sprout, glowing with bioluminescent life.

And resting beside it was humanity's final message:
"To whoever finds this... take care of what remains."

Pip looked down with gentle awe.
He was not abandoned.
He was chosen.
To be the guardian of a brand new world.

And with one warm drop of devotion, life exploded across the horizon, blooming into an endless sea of golden light.
Proving that love will always outlive rust.

🎵 Music: Erik Satie — Gymnopédie No. 1 (Acoustic Classical Piano, Public Domain)
🎙️ Voice: Andrew Multilingual Neural

💬 What did this story make you feel? Share your thoughts below! 👇
🔔 Subscribe to @captonsumanth for more heartwarming animated stories and Pip's continuing journey! ✨

#shorts #animation #pixarstyle #robot #wholesomestories #cgi #scifiart #piptherobot #invisibleindian #3danimation"""

TAGS = [
    "shorts", "animation", "pixar", "robot", "wholesome",
    "scifi", "the wild robot", "walle", "story short", "pip",
    "invisible indian", "cgi short", "heartwarming", "emotional stories"
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
    if res.get("success"):
        vid = res.get("video_id")
        url = res.get("video_url")
        print("\n==========================================")
        print("🎉 REMASTER UPLOAD SUCCESSFUL! 🎉")
        print(f"Video ID:  {vid}")
        print(f"Watch URL: {url}")
        print(f"Privacy:   PRIVATE")
        print("==========================================")
        return vid, url
    else:
        print(f"Upload failed: {res}")
        sys.exit(1)

if __name__ == "__main__":
    main()
