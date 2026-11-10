# Faceless Video & Shorts Production Suite

A complete, self-contained, open-source video generation studio running locally on your Mac.

## 🛠️ The Standard MCP Video Tools

Run through any MCP client or script via `mcp_server/server.py`:

```
1. generate_faceless_short    - Full end-to-end 9:16 short video generation
2. search_open_stock_videos   - Search NASA, Wikimedia Commons, Archive.org, Pexels, Pixabay
3. synthesize_speech          - Edge-TTS neural voiceover generator
4. burn_subtitles             - Kinetic ASS/SRT caption combustion
5. reframe_to_vertical        - 16:9 horizontal to 9:16 vertical re-framer
6. trim_video                 - Precision clip trimmer
7. concat_videos              - Multi-clip stitcher
8. mix_audio_ducking          - Automatic music ducking beneath speech
9. create_ken_burns_clip      - Still-to-video pan/zoom animator
10. extract_frames            - Thumbnail & frame grabber
11. inspect_media_file        - Media metadata & stream inspector
```

## 🌐 Open Connectors (`.agents/skills/make-faceless-short-free/scripts/connectors/`)

- **NASA Open Media Connector** (`images-api.nasa.gov`): Real space & earth observation video.
- **Wikimedia Commons Connector** (`commons.wikimedia.org`): CC and public domain footage.
- **Internet Archive Connector** (`archive.org`): Historical, documentary, and open archive reels.
- **Pexels & Pixabay Connectors**: Direct vertical stock video downloads.
- **Stock Cascade Aggregator**: Automatically tries the best source for your topic.

## 🎨 Skills (`.agents/skills/`)

- **`make-faceless-short-free`**: General vertical shorts (stock footage, AI stills, or procedural motion).
- **`cartoon-shorts-maker`**: 3D Pixar/Disney style animated story shorts.

## 🚀 Quick CLI Examples

```bash
# 1. Fact / Science Short (NASA Footage + Voice + Captions)
.venv/bin/python .agents/skills/make-faceless-short-free/scripts/generate_short.py \
  --title "Earth In Orbit" \
  --script "From space, national borders completely disappear. Astronauts call this the overview effect: a cognitive shift that makes you realize Earth is just one fragile oasis in the void." \
  --visuals "stock" \
  --keyword "earth" \
  --output "output/earth_orbit.mp4"

# 2. 3D Cartoon Story Short (Pip the Robot)
# See output/pip_cartoon_short.mp4
```
