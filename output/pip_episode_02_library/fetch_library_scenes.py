#!/usr/bin/env python3
"""
fetch_library_scenes.py — Fetches 5 bespoke 3D Pixar scenes for Pip & The Forgotten Library.
Gracefully handles the 45-second rate limit of Pollinations AI free tier.
"""

import os
import re
import sys
import time
import urllib.request
import urllib.parse

DEST_DIR = "/Users/sumanth/Downloads/New/output/pip_episode_02_library"
os.makedirs(DEST_DIR, exist_ok=True)

PROMPTS = [
    ("scene_01.jpg", "3D Pixar Disney animation style vertical 9:16 portrait. Pip the tiny cute rusty robot with glowing blue round eyes and small antenna standing at the grand entrance of a giant overgrown ancient library with moss, climbing ivy, golden sunbeams through broken ceiling."),
    ("scene_02.jpg", "3D Pixar Disney animation style vertical 9:16 portrait. Close-up of Pip the cute rusty robot gently blowing dust motes off an ancient hardbound picture book showing human city, green trees, smiling people, blue skies. Wonder and tenderness."),
    ("scene_03.jpg", "3D Pixar Disney animation style vertical 9:16 portrait. Pip the small scrap robot standing on a wooden chair plugging a copper wire into an old green CRT computer screen. Glowing pixel text displays TAKE CARE OF WHAT REMAINS."),
    ("scene_04.jpg", "3D Pixar Disney animation style vertical 9:16 portrait. Macro close-up of Pip looking down at his open chest casing. Nestled next to his glowing amber core battery is a tiny glowing green plant sprout with dew drops. Pure love and purpose."),
    ("scene_05.jpg", "3D Pixar Disney animation style vertical 9:16 portrait. Pip standing on the sunlit stone threshold of the overgrown library looking out across the vast horizon where wildflowers bloom among scrap dunes. Warm golden halo, chest glowing with life.")
]

def is_valid_jpg(path):
    if not os.path.exists(path) or os.path.getsize(path) < 10000:
        return False
    with open(path, "rb") as f:
        head = f.read(10)
        return head.startswith(b"\xff\xd8")  # JPEG header

headers = {"User-Agent": "Mozilla/5.0"}

for filename, prompt in PROMPTS:
    out_path = os.path.join(DEST_DIR, filename)
    if is_valid_jpg(out_path):
        print(f"✅ {filename} is already downloaded and valid ({os.path.getsize(out_path)} bytes).")
        continue

    print(f"\n🔄 Generating {filename}...")
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true"

    while True:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = resp.read()
                if data.startswith(b"\xff\xd8") and len(data) > 10000:
                    with open(out_path, "wb") as f:
                        f.write(data)
                    print(f"🎉 Successfully saved {filename} ({len(data)} bytes)!")
                    break
                else:
                    # Might be json error
                    txt = data.decode("utf-8", errors="ignore")
                    m = re.search(r"Retry after (\d+)s", txt)
                    wait_s = int(m.group(1)) + 2 if m else 45
                    print(f"⏳ Rate limited. Waiting {wait_s}s...")
                    time.sleep(wait_s)
        except urllib.error.HTTPError as e:
            txt = e.read().decode("utf-8", errors="ignore")
            m = re.search(r"Retry after (\d+)s", txt)
            wait_s = int(m.group(1)) + 2 if m else 46
            print(f"⏳ HTTP {e.code}: Rate limited. Waiting {wait_s}s...")
            time.sleep(wait_s)
        except Exception as ex:
            print(f"⚠️ Error: {ex}. Waiting 20s...")
            time.sleep(20)

    # Cooldown before requesting the next image
    print("Sleeping 46s before next image...")
    time.sleep(46)

print("\n🚀 All 5 scenes successfully generated!")
