#!/usr/bin/env python3
"""
download_and_prep_assets.py — Download and reframe masterwork assets for 10 Epic Shorts.
"""

import os
import sys
import time
import requests
import subprocess

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
FFMPEG = os.path.join(WORKSPACE_ROOT, ".venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

BROWSER_HEADERS = {
    "User-Agent": "EpicShortsStudio/1.0 (contact: sumanthsm36@gmail.com; educational non-profit) requests/2.31"
}

# 10 Shorts Asset Plan
# Each short has primary masterwork URLs; if 2-3 are available, crops/focal zooms generate all 5 1080x1920 scenes.
SHORTS_ASSETS = {
    "short_01_urmila_slumber": [
        "https://upload.wikimedia.org/wikipedia/commons/9/98/Ramayana_-_Marriage_of_Rama_Bharata_Lakshmana_and_Shatrughna.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/1b/Sunaina_%28Sunayana%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/e0/Draupadi_and_Pandavas.jpg"
    ],
    "short_02_shabari_devotion": [
        "https://upload.wikimedia.org/wikipedia/commons/b/ba/0010922_8th_century_Kharod_Maa_Shabari_Temple_Chhattisgarh_041.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/0010922_8th_century_Kharod_Maa_Shabari_Temple_Chhattisgarh_047.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/6/67/Rama_with_the_chiefs_of_his_army.jpg"
    ],
    "short_03_jatayu_valour": [
        "https://upload.wikimedia.org/wikipedia/commons/c/cf/Jatayu_Confronting_Ravana_to_Save_Sita.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/bb/Ravana_fighting_with_Jatayu.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/ef/Jatayu_Attacks_Ravana_to_Save_Sita_and_Shatters_his_Chariot_-_early_18th-century.jpg"
    ],
    "short_04_floating_bridge": [
        "https://upload.wikimedia.org/wikipedia/commons/6/67/Rama_with_the_chiefs_of_his_army.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d2/Akshay_Vat%2C_The_Banyan_Tree_Witness_to_The_Gita%2C_Kurukshetra%2C_India.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/16/Vibhishana_Meets_Rama.jpg"
    ],
    "short_05_vibhishana_refuge": [
        "https://upload.wikimedia.org/wikipedia/commons/1/16/Vibhishana_Meets_Rama.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/59/Vibhishana_showing_Vimana_to_Rama.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/48/%22The_Court_of_Ravana%22%2C_Folio_from_a_Ramayana_MET_DP103081.jpg"
    ],
    "short_06_gita_wisdom": [
        "https://upload.wikimedia.org/wikipedia/commons/b/b5/Krishna_Arjuna_Gita.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d9/Krishna_and_Arjuna_on_Chariot_Painting.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/fc/Bhagavad_Gita_-_The_Song_of_God.jpg"
    ],
    "short_07_bhishma_vow": [
        "https://upload.wikimedia.org/wikipedia/commons/2/21/Bhisma_is_lying_on_a_bed_of_arrows_with_Arjuna_standing_above_him_with_bow_drawn_and_pointed..jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/23/Bhisma_on_arrows_bed.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/57/Bhishma_Pitamah%2C_lying_on_a_bed_of_arrows%2C_Razmnama_Illustration%2C_circa_1598_CE%2C_CSMVS%2C_Mumbai.jpg"
    ],
    "short_08_karna_generosity": [
        "https://upload.wikimedia.org/wikipedia/commons/f/f9/Karna_Statue.png",
        "https://upload.wikimedia.org/wikipedia/commons/6/6f/Arjuna_and_His_Charioteer_Krishna_Confront_Karna.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/45/Arjuna_and_karna_in_war%2C_krishna_as_arjuna_charioter.jpg"
    ],
    "short_09_yuyutsu_righteousness": [
        "https://upload.wikimedia.org/wikipedia/commons/a/a5/Sri_Krishna_as_Envoy.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/e/e0/Draupadi_and_Pandavas.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b4/The_Graet_Gambling_Scene_of_the_Mahabharata%2C_Albert_Hall_Museum%2C_Jaipur.jpg"
    ],
    "short_10_arjuna_chariot": [
        "https://upload.wikimedia.org/wikipedia/commons/0/0e/Arjuna%27s_chariot_in_Geethopadesam_park%2C_Tirumala_%28May_2019%29_2.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3b/Cirebonese_Art_Batik_-_Mahabharat_Scene_with_Arjun_%26_Krishna_in_Chariot_-_Gita.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/37/Krishna_and_Arjun_on_the_chariot%2C_Mahabharata%2C_18th-19th_century%2C_India.jpg"
    ]
}


def download_file(url, target_path, retries=3):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 50000:
        return True
    for attempt in range(1, retries + 1):
        try:
            time.sleep(0.8)
            r = requests.get(url, headers=BROWSER_HEADERS, timeout=25)
            if r.status_code == 200 and len(r.content) > 30000:
                with open(target_path, "wb") as f:
                    f.write(r.content)
                return True
            elif r.status_code == 429:
                time.sleep(attempt * 2.5)
            else:
                time.sleep(1.5)
        except Exception:
            time.sleep(2.0)
    return False


def reframe(src, dst, vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"):
    cmd = [
        FFMPEG, "-y",
        "-i", src,
        "-vf", vf,
        dst
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main():
    print("=" * 60)
    print("📥 DOWNLOADING & PREPARING ASSETS FOR 10 EPIC SHORTS")
    print("=" * 60)

    for short_id, urls in SHORTS_ASSETS.items():
        s_dir = os.path.join(BASE_DIR, short_id)
        os.makedirs(s_dir, exist_ok=True)
        print(f"\n📂 Processing {short_id}...")

        downloaded_raws = []
        for idx, url in enumerate(urls, 1):
            raw_ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
            raw_path = os.path.join(s_dir, f"raw_{idx:02d}{raw_ext}")
            if download_file(url, raw_path):
                downloaded_raws.append(raw_path)
            else:
                print(f"   ⚠️ Could not download {url}")

        if not downloaded_raws:
            raise RuntimeError(f"No assets could be downloaded for {short_id}")

        # Create 5 distinct scenes using the downloaded masterworks and cinematic focal crops
        # Scene 1: First masterwork wide
        reframe(downloaded_raws[0], os.path.join(s_dir, "scene_01.png"))
        
        # Scene 2: First masterwork punch-in hero crop
        reframe(downloaded_raws[0], os.path.join(s_dir, "scene_02.png"), 
                vf="crop=in_w*0.75:in_h*0.75:in_w*0.12:in_h*0.12,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920")
        
        # Scene 3: Second masterwork wide (or third if available)
        raw_scene_3 = downloaded_raws[1] if len(downloaded_raws) > 1 else downloaded_raws[0]
        reframe(raw_scene_3, os.path.join(s_dir, "scene_03.png"))
        
        # Scene 4: Second masterwork close-up crop
        reframe(raw_scene_3, os.path.join(s_dir, "scene_04.png"),
                vf="crop=in_w*0.8:in_h*0.8:in_w*0.1:in_h*0.15,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920")
        
        # Scene 5: Third masterwork wide (or illuminated variant)
        raw_scene_5 = downloaded_raws[2] if len(downloaded_raws) > 2 else downloaded_raws[0]
        reframe(raw_scene_5, os.path.join(s_dir, "scene_05.png"))

        for i in range(1, 6):
            p = os.path.join(s_dir, f"scene_{i:02d}.png")
            sz = os.path.getsize(p) / 1024
            print(f"   ✅ scene_{i:02d}.png ({sz:.1f} KB)")

    print("\n🎉 All 50 scene assets (5 scenes x 10 shorts) prepared at 1080x1920 HD!")


if __name__ == "__main__":
    main()
