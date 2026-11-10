---
name: make-faceless-short-free
description: Make a narrated, captioned vertical faceless short video (YouTube Shorts, TikTok, Instagram Reels) 100% locally and free without depending on any MCP server or paid credits. Generates natural neural voiceover via edge-tts, extracts word-level timestamps for kinetic captions, sources matching motion visuals, and renders a 1080x1920 MP4 via FFmpeg.
license: MIT
compatibility: Fully local, zero-cost, no MCP servers needed. Runs using Python 3 and FFmpeg.
metadata:
  version: "2.0.0"
  mcp_dependent: false
  cost: "0.00"
---

# Make Faceless Short (Multi-Genre Studio Engine)

Generate high-retention 9:16 vertical short videos end-to-end completely locally, with **no MCP servers, no credit subscriptions, and no paid API keys**.

## 🎭 Multi-Genre Ideation & Production Framework

This engine is **genre-agnostic by default**: it can create breakthrough short-form content across any genre or topic, or adapt instantly to a specific genre requested by the user.

### When the User Says: "Make a video" (No genre specified)
The agent autonomously invents a high-curiosity, paradox-driven topic from diverse niches:
- **Mind/Psychology Paradoxes:** (e.g. *The Paradox of Choice*, *The Baader-Meinhof Phenomenon*, *The 90-Minute Cortisol Rule*).
- **Ancient Mysteries & Archaeology:** (e.g. *The Antikythera Mechanism*, *The Library of Alexandria*, *The Underground City of Derinkuyu*).
- **Cosmic Frontiers & Physics:** (e.g. *The Overview Effect*, *Time Dilation at Event Horizons*, *The Fermi Paradox*).
- **Stoic Philosophy & Resilience:** (e.g. *The Dichotomy of Control*, *Amor Fati*, *The 4AM Monk Habit*).
- **Wholesome/Fantasy Lore:** (e.g. *The Clockmaker of Chronos*, *The Forgotten Garden*).

### When the User Asks for a Specific Genre
Use the `--genre <name>` flag to automatically configure voice, soundbed harmonics, color grading, and visual tone:

| Genre (`--genre`) | Tone & Pacing | Voice Actor | Harmonic Soundbed | Color Grade & Texture |
| :--- | :--- | :--- | :--- | :--- |
| **`mystery`** | Suspenseful, slow revelation | `AndrewMultilingual` (Human conversational) | Low tense drone (98Hz) | High contrast, desaturated, dark vignette |
| **`scifi`** | Awe-inspiring, cosmic | `AndrewMultilingual` (Deep conversational) | Cosmic ambient pad (110Hz) | Deep blacks, vivid cyan/violet, space glow |
| **`mythology`** | Epic, ancient, legendary | `PrabhatNeural` (Authentic Indian English) | Majestic ancient pad (130Hz) | Radiant warm amber, golden highlights |
| **`philosophy`** | Contemplative, profound | `AndrewMultilingual` (Authentic cadence) | Deep D-minor pad (146Hz) | Timeless filmic contrast, clean white captions |
| **`cartoon`** | Whimsical, heartwarming | `AndrewMultilingual` / `JennyNeural` | Uplifting major chords (196Hz) | Vibrant saturation, 3D animated style |
| **`psychology`** | Intellectual, thought-provoking | `AndrewMultilingual` (Warm podcast tone) | Resonant introspective drone | Crisp high-contrast, yellow kinetic text |
| **`history`** | Archival, dramatic | `AndrewMultilingual` / `PrabhatNeural` | Dramatic period pad (130Hz) | Authentic archival tone, subtle 35mm grain |
| **`general`** | Balanced, energetic | `AndrewMultilingual` (Natural human tone) | Ambient C-maj9 pad | Standard cinematic 35mm film curve |

---

## Production Pipeline

```
1. SCRIPT & HOOK  ──▶ 2. EDGE-TTS VOICEOVER ──▶ 3. WORD-LEVEL CAPTIONS (ASS)
                                                           │
4. FINAL 1080x1920 MP4 ◀── 6. FFMPEG RENDER ◀── 5. OPEN CONNECTORS (Wikimedia/NASA/B-Roll)
```

## Quick Commands

```bash
# 1. Mystery Genre (Suspense pad, Christopher voice, moody grading):
.venv/bin/python .agents/skills/make-faceless-short-free/scripts/generate_short.py \
  --title "The Lost Expedition" \
  --genre "mystery" \
  --script "In nineteen twenty-five, British explorer Percy Fawcett walked into the Amazon jungle in search of the lost city of Z. He and his entire team vanished without a single trace. To this day, over a hundred explorers who went searching for him have also disappeared." \
  --visuals "stock" \
  --keyword "amazon jungle" \
  --output "output/lost_expedition.mp4"

# 2. Philosophy Genre (Stoic D-minor pad, Ryan voice):
.venv/bin/python .agents/skills/make-faceless-short-free/scripts/generate_short.py \
  --title "Marcus Aurelius Rule" \
  --genre "philosophy" \
  --script "You have power over your mind, not outside events. Realize this, and you will find strength. The Roman Emperor Marcus Aurelius wrote these words during a deadly plague while sleeping on a military camp cot." \
  --visuals "stock" \
  --keyword "statue" \
  --output "output/stoic_mind.mp4"

# 3. 3D Cartoon / Whimsical Story:
.venv/bin/python .agents/skills/make-faceless-short-free/scripts/generate_short.py \
  --title "The Magic Sprout" \
  --genre "cartoon" \
  --script "A tiny robot found a single green sprout in a world of scrap metal. With one drop of care, an entire forest bloomed." \
  --visuals "ai" \
  --output "output/magic_sprout.mp4"
```

---

## Monetization Rules (Guaranteed YPP Approval)

1. **Original Angle:** Always deliver unique commentary, surprising facts, or proprietary storytelling. Never scrape Wikipedia articles verbatim.
2. **Transformative Visuals:** Cuts occur every 2.5–3.5s with dynamic Ken Burns camera motion, cinematic 35mm film grain, and lens vignette.
3. **Audio Normalization:** Voice normalized to approximately -16 LUFS with ducked harmonic soundbed (15%–23% volume).
4. **Mobile Safe Zones:** Captions positioned strictly in the Y=1350–1500px band.
5. **Dynamic Cartoon & Animation Interstitials:** Intersperse stylized animation or expressive cartoon-like reaction clips every 2–3 scenes to elevate visual variety, humor, and audience retention.
