#!/usr/bin/env python3
"""
download_and_prep_mahabharata.py — Download and reframe 25 museum masterworks for 5 Mahabharata Shorts.
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
    "User-Agent": "MahabharataShortsStudio/1.0 (contact: sumanthsm36@gmail.com; educational non-profit) requests/2.31"
}

ASSETS_PLAN = {
    "short_01_barbarika_arrows": [
        "https://upload.wikimedia.org/wikipedia/commons/b/b5/Khatushyam.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/d2/Akshay_Vat%2C_The_Banyan_Tree_Witness_to_The_Gita%2C_Kurukshetra%2C_India.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/37/Krishna_and_Arjun_on_the_chariot%2C_Mahabharata%2C_18th-19th_century%2C_India.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c1/Shree_Shree_Khatu_Shyam_Temple.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/12/Khatu_Shyam_Ji_Entrance_Gate.jpg"
    ],
    "short_02_karna_armor": [
        "https://upload.wikimedia.org/wikipedia/commons/e/ed/Arjuna_Karna_final_battle%2C_Kurukshetra_war%2C_12th-century_Mahabharata_relief%2C_Hoysalesvara_temple_Halebidu.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/6/6f/Arjuna_and_His_Charioteer_Krishna_Confront_Karna.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/f9/Karna_Statue.png",
        "https://upload.wikimedia.org/wikipedia/commons/9/9f/Karna%2C_one_of_the_Kauravas%2C_slays_the_Pandavas%27_nephew_Ghatotkacha_with_a_weapon_given_to_him_by_Indra%2C_the_king_of_the_gods%2C_from_a_manuscript_of_the_Razmnama.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/45/Arjuna_and_karna_in_war%2C_krishna_as_arjuna_charioter.jpg"
    ],
    "short_03_abhimanyu_womb": [
        "https://upload.wikimedia.org/wikipedia/commons/c/c3/Subhadra%2C_the_half_sister_of_Krishna%2C_drives_a_chariot_away_from_Dwarka_with_Arjuna_and_Krishna_inside.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/1a/Abhimanyu_Hunting%2C_Scene_from_the_Story_of_the_Marriage_of_Abhimanyu_and_Vatsala%2C_Folio_from_a_Mahabharata_%28%28War_of_the%29_Great_Bharatas%29_LACMA_M.85.297.8.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/00/Abhimanyu_on_Foot.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/21/Abhimanyu_Shashirekha_by_Aman_Varma.png",
        "https://upload.wikimedia.org/wikipedia/commons/5/5d/Abhimanyu_Kilss_Lakshmana.jpg"
    ],
    "short_04_sahadeva_curse": [
        "https://upload.wikimedia.org/wikipedia/commons/e/e0/Draupadi_and_Pandavas.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/a/a3/One_of_the_Pandava_twins%2C_probably_Sahadeva.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b4/The_Graet_Gambling_Scene_of_the_Mahabharata%2C_Albert_Hall_Museum%2C_Jaipur.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/09/Death_of_Draupadi_-_Illustrations_from_the_Barddhaman_edition_of_Mahabharata.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/a/a3/India%2C_Maharashtra%2C_Paithan_school%2C_c._1800_-_Illustration_to_the_Mahabharata_-_2005.68_-_Cleveland_Museum_of_Art.jpg"
    ],
    "short_05_eklavya_sacrifice": [
        "https://upload.wikimedia.org/wikipedia/commons/7/76/Myths_of_the_Hindus_%26_Buddhists_-_Ekalavya.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/03/Eklavya_at_the_shrine.png",
        "https://upload.wikimedia.org/wikipedia/commons/2/23/Ekalavya_Award.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/cd/Illustration_of_the_Mahabharata.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/a/aa/A_painting_from_the_Mahabharata_Balabhadra_fighting_Jarasandha.jpg"
    ]
}


def download_file(url, target_path, retries=3):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 50000:
        return True
    for attempt in range(1, retries + 1):
        try:
            time.sleep(1.0)
            r = requests.get(url, headers=BROWSER_HEADERS, timeout=25)
            if r.status_code == 200 and len(r.content) > 30000:
                with open(target_path, "wb") as f:
                    f.write(r.content)
                return True
            elif r.status_code == 429:
                print(f"   ⏳ Rate limit 429, waiting {attempt * 2.5}s...")
                time.sleep(attempt * 2.5)
            else:
                time.sleep(1.5)
        except Exception as e:
            print(f"   ⚠️ Download error: {e}, retry {attempt}...")
            time.sleep(2.0)
    return False


def reframe_image(src, dst):
    cmd = [
        FFMPEG, "-y",
        "-i", src,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        dst
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main():
    print("=" * 60)
    print("📥 DOWNLOADING & PREPARING 25 MAHABHARATA MASTERWORK ASSETS")
    print("=" * 60)

    for short_id, urls in ASSETS_PLAN.items():
        s_dir = os.path.join(BASE_DIR, short_id)
        os.makedirs(s_dir, exist_ok=True)
        print(f"\n📂 Processing {short_id}...")

        for idx, url in enumerate(urls, 1):
            raw_ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
            raw_path = os.path.join(s_dir, f"raw_scene_{idx:02d}{raw_ext}")
            final_png = os.path.join(s_dir, f"scene_{idx:02d}.png")

            ok = download_file(url, raw_path)
            if not ok:
                print(f"   ❌ Failed to download {url}")
                continue

            reframe_image(raw_path, final_png)
            sz = os.path.getsize(final_png) / 1024
            print(f"   ✅ scene_{idx:02d}.png created ({sz:.1f} KB)")

    print("\n🎉 All 25 Mahabharata scene assets downloaded and reframed!")


if __name__ == "__main__":
    main()
