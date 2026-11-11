#!/usr/bin/env python3
import os
import subprocess

FFMPEG = "/Users/sumanth/Downloads/New/.venv/lib/python3.9/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
BRAIN = "/Users/sumanth/.gemini/antigravity/brain/6d62e7a1-85a9-449b-8870-3bd8b6c5c928"
SERIES2 = "/Users/sumanth/Downloads/New/output/ramayana_series_02"
BASE = "/Users/sumanth/Downloads/New/output/ramayana_animated_3d"

def prep(src, dst, vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"):
    cmd = [
        FFMPEG, "-y",
        "-i", src,
        "-vf", vf,
        dst
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sz = os.path.getsize(dst) / 1024
    print(f"Created {dst} ({sz:.1f} KB)")

# Short 02
d2 = os.path.join(BASE, "short_02_gayatri_cipher")
os.makedirs(d2, exist_ok=True)
prep(f"{BRAIN}/scene_01_1794376327458.jpg", f"{d2}/scene_01.png")
prep(f"{BRAIN}/scene_02_1794376348836.jpg", f"{d2}/scene_02.png")
prep(f"{BRAIN}/scene_03_1794376372807.jpg", f"{d2}/scene_03.png")
prep(f"{BRAIN}/scene_04_1794376395235.jpg", f"{d2}/scene_04.png")
prep(f"{BRAIN}/scene_03_1794376372807.jpg", f"{d2}/scene_05.png", vf="crop=in_w*0.8:in_h*0.8:in_w*0.1:in_h*0.1,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920")

# Short 03
d3 = os.path.join(BASE, "short_03_ravana_violin")
os.makedirs(d3, exist_ok=True)
prep(f"{BRAIN}/scene_01_1794376328280.jpg", f"{d3}/scene_01.png")
prep(f"{BRAIN}/scene_02_1794376352524.jpg", f"{d3}/scene_02.png")
prep(f"{BRAIN}/scene_03_1794376378308.jpg", f"{d3}/scene_03.png")
prep(f"{BRAIN}/scene_04_1794376405940.jpg", f"{d3}/scene_04.png")
prep(f"{BRAIN}/scene_04_1794376405940.jpg", f"{d3}/scene_05.png", vf="crop=in_w*0.8:in_h*0.8:in_w*0.1:in_h*0.15,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920")

# Short 04
d4 = os.path.join(BASE, "short_04_indrajit_astras")
os.makedirs(d4, exist_ok=True)
prep(f"{BRAIN}/scene_01_png_1794376360166.jpg", f"{d4}/scene_01.png")
prep(f"{BRAIN}/scene_02_png_1794376387028.jpg", f"{d4}/scene_02.png")
prep(f"{SERIES2}/short_04_indrajit_astras/scene_03.jpg", f"{d4}/scene_03.png")
prep(f"{SERIES2}/short_04_indrajit_astras/scene_04.jpg", f"{d4}/scene_04.png")
prep(f"{BRAIN}/scene_01_png_1794376360166.jpg", f"{d4}/scene_05.png", vf="crop=in_w*0.75:in_h*0.75:in_w*0.12:in_h*0.1,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920")

# Short 05
d5 = os.path.join(BASE, "short_05_bharata_penance")
os.makedirs(d5, exist_ok=True)
prep(f"{BRAIN}/scene_01_1794376407807.jpg", f"{d5}/scene_01.png")
prep(f"{SERIES2}/short_05_bharata_penance/scene_02.jpg", f"{d5}/scene_02.png")
prep(f"{SERIES2}/short_05_bharata_penance/scene_03.jpg", f"{d5}/scene_03.png")
prep(f"{SERIES2}/short_05_bharata_penance/scene_04.jpg", f"{d5}/scene_04.png")
prep(f"{BRAIN}/scene_01_1794376407807.jpg", f"{d5}/scene_05.png", vf="crop=in_w*0.75:in_h*0.75:in_w*0.12:in_h*0.08,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920")

print("All assets prepared successfully!")
