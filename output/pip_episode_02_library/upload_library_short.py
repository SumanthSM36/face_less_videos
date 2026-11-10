#!/usr/bin/env python3
"""
upload_library_short.py — Uploads Pip & The Forgotten Library to YouTube as Private.
"""

import os
import sys

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
CONNECTORS_DIR = os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts/connectors")
sys.path.insert(0, CONNECTORS_DIR)

from youtube_connector import upload_youtube_short

VIDEO_FILE = "/Users/sumanth/Downloads/New/output/pip_episode_02_library/pip_and_the_forgotten_library.mp4"
TITLE = "The Robot Who Found Mankind's Last Words 🤖📖 #shorts"

DESCRIPTION = """Wandering through a world of dead rust, Pip stepped into a towering forgotten library, seeking the one answer that haunted his circuits: Who made me... and where did they go?

Beneath cathedral arches choked with vines, he gently blew the dust off an ancient picture book, showing green trees, laughter, and a sky of boundless blue.

In the dark, Pip plugged his rusted cord into a flickering terminal screen. Static gave way to a final human message from centuries past:
"To whoever finds this... take care of what remains."

Pip looked down at the tiny glowing sprout nestled safely inside his chest casing.
He was not abandoned.
He was chosen.
To be the gentle guardian of a brand new world.

💬 What did this story make you feel? Share your thoughts below! 👇
🔔 Subscribe to @captonsumanth for more heartwarming animated stories and Pip's continuing journey! ✨

#shorts #animation #pixar #robot #wholesomestories #cgi #scifiart #theforgottenlibrary #piptherobot #invisibleindian"""

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
        print("🎉 UPLOAD SUCCESSFUL! 🎉")
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
