---
name: video-director-clipper
description: >-
  Director for video clipping and viral repurposing. Ingests uploaded MP4s, YouTube URLs,
  or web links, extracts high-retention viral segments, reframes to 9:16 vertical, and generates kinetic subtitles.
---

# Video Director for Video Clipping

Automates extraction and vertical repurposing from long videos into viral Shorts ($1080\times1920$).

## Workflow
1. Ingests video from YouTube URL (via `yt-dlp`), direct web link, or local uploaded file.
2. Identifies key emotional peaks, punchlines, or revelations.
3. Reframes 16:9 media to 9:16 vertical format (smart center crop or stacked blurred background).
4. Transcribes dialogue and burns synchronized ASS kinetic captions in the safe zone.
