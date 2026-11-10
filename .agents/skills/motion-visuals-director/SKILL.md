---
name: motion-visuals-director
description: Generates dynamic motion visuals, moving video footage, and procedural living motion specifically tailored for vertical YouTube Shorts. Uses 100% legal, open-source, commercial-use public domain footage (NASA, Wikimedia Commons, Prelinger/Archive.org) and 2.5D parallax optical motion to produce broadcast-grade vertical MP4s (1080x1920) with fast 2.5s-3.5s pacing cuts.
---

# Dynamic Motion Visuals Director Agent

The `motion-visuals-director` agent replaces static screenshot slideshows with living, continuous running video and dynamic motion visuals tailored for YouTube Shorts.

## Core Capabilities

1. **100% Legal Open Stock Video Retrieval:**
   - **NASA Open Access Video Archives** (17 U.S.C. § 105: Public Domain, commercial use free, zero copyright liability).
   - **Wikimedia Commons** (Public Domain & CC0 verified motion media).
   - **Internet Archive Prelinger & FedFlix Collections** (Historical, documentary, and vintage reels).
   - Automatically reframes horizontal 16:9 footage into crisp 9:16 vertical (1080x1920) with smart center crop or dynamic motion blur fill.

2. **Procedural Living Motion Engine (2.5D Parallax & Living Atmosphere):**
   - For custom artwork (e.g. 3D Pip illustrations, historical paintings):
     - Applies continuous multi-plane optical flow and bezier camera sweeps (`cosmic_drift`, `dramatic_push`, `slow_orbit`, `hero_pan`).
     - Adds procedural running atmospheric particles (space dust, light leaks, 35mm grain, lens vignette).
     - Guarantees that every frame has continuous motion, eliminating viewer swipe-away fatigue.

3. **Fast Dynamic Pacing (YouTube Shorts Standard):**
   - Cuts every 2.5s to 3.5s to maintain algorithmic retention above 85%.

## CLI Usage

```bash
# Generate a vertical motion clip from NASA open footage
python3 scripts/motion_visuals_director.py \
  --query "deep space galaxy" \
  --duration 3.0 \
  --output output/cuts/cut_01.mp4

# Transform artwork into living 2.5D motion
python3 scripts/motion_visuals_director.py \
  --image output/assets/pip_scene.jpg \
  --style dramatic_push \
  --duration 3.0 \
  --output output/cuts/cut_02.mp4
```
