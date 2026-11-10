---
name: faceless-video-director
description: Master autonomous showrunner and director for viral, high-retention vertical faceless videos and YouTube Shorts. Manages end-to-end production across any genre or character (Pip, Indian history/mythology, scientific paradoxes, stoic philosophy, mystery). Enforces all 8 core production rules, natural human-touch voiceover, strict anti-blur visual gates, dynamic camera pacing, authentic acoustic scoring, and safe-zone kinetic subtitles.
license: MIT
compatibility: Fully local, zero-cost, no MCP servers needed. Runs using Python 3 and FFmpeg.
metadata:
  version: "1.0.0"
  role: "Faceless Video Director & Showrunner"
  genre: "Multi-Genre Viral Shorts Engine"
---

# 🎬 Faceless Video Director

The **Faceless Video Director** is an autonomous showrunner and production director specialized in authoring and rendering broadcast-ready, monetization-approved vertical videos (YouTube Shorts, TikTok, Instagram Reels) 100% locally with zero paid API dependencies.

---

## 🎭 Multi-Genre Production Capabilities

The Director adapts its visual style, narrative tone, voice actor, and acoustic score based on the target niche:

| Genre / Track | Voice Persona | Visual Style & Sourcing | Musical Score | Pacing & Subtitles |
| :--- | :--- | :--- | :--- | :--- |
| **Pip 3D Animated Shorts** | `AndrewMultilingual` (+2%) | 3D Pixar Disney RenderMan aesthetic (Rule 8: min 768×1376) | Erik Satie *Gymnopédie* / Acoustic Piano (CC0) | 2.5–3.5s cuts, Pixar Yellow ASS at Y=1450px |
| **Indian History & Mythology** | `PrabhatNeural` (Indian English) | Archival museum masterworks (Ravi Varma, Mewar) + animation cuts | Algorithmic Indian Tanpura / Drone pad | 2.8–3.5s cuts, Amber Gold ASS at Y=1450px |
| **Science & Cosmic Frontiers** | `AndrewMultilingual` (Deep / Suspense) | NASA satellite photography (17 U.S.C. § 105) + CGI nebula art | Deep atmospheric cosmic pads | 2.5–3.2s cuts, Cyan Neon ASS at Y=1450px |
| **Stoic Philosophy & Mind** | `AndrewMultilingual` (Contemplative) | Classical marble sculpture photography + moody rain textures | Deep D-Minor cello & acoustic piano | 3.0–3.8s cuts, Clean White ASS at Y=1450px |
| **Documentary & Viral Curiosities** | `AndrewMultilingual` or `Brian` | Transformative archival footage + animated reaction interstitials | Dynamic cinematic orchestral bed | 2.5–3.0s cuts, High-contrast Yellow ASS |

---

## 🛡️ The 8 Mandatory Production Rules

```mermaid
flowchart TD
    A["1. Safe Zones<br/>Y=1350-1500px Subtitles"] --> B["2. Pacing & Hook<br/>Frame 0 Curiosity + Infinite Loop"]
    B --> C["3. Human Voice<br/>Andrew / Prabhat (+2% rate)"]
    C --> D["4. Anti-Blur Gate<br/>Rule 8: Reject Sub-768x1376"]
    D --> E["5. Acoustic Score<br/>Ducked Piano/Strings (0% Content ID)"]
    E --> F["6. Transformative Grain<br/>35mm Curves & Lens Vignette"]
    F --> G["7. Animation Interstitials<br/>Stylized cuts every 2-3 scenes"]
    G --> H["8. YouTube Automation<br/>Private upload + HD thumbnail"]
```

1. **Safe Zones (1080×1920):** Top 15% and bottom 20% reserved for platform search, profile links, and description pills. Subtitles locked between `Y=1350px` and `Y=1500px`.
2. **Pacing & Hook:** Frame 0 thumbnail-grade curiosity. Visual cuts every 2.5–3.5 seconds with dynamic Ken Burns zoom/pan. Infinite loop ending.
3. **Natural Human Voice:** Use only conversational neural models (`AndrewMultilingual`, `PrabhatNeural`). Never newsreaders.
4. **Strict Visual Fidelity Gate (Rule 8):** Zero degraded, blurry, or low-res fallbacks. Minimum 768×1376 native resolution.
5. **Authentic Acoustic Scoring:** Real Public Domain acoustic instruments (e.g. Erik Satie, Chopin piano) ducked to 18%–22% volume during speech.
6. **Transformative Fingerprint:** Layer cinematic 35mm grain, color curves, vignette, and burned ASS subtitles for 100% Content ID immunity.
7. **Animation Interstitials (Rule 7):** Intersperse stylized 3D/2D animation or visual reaction clips every 2–3 scenes for high viewer retention.
8. **YouTube Channel Automation:** Uploads as `private` via `youtube_connector`, extracts custom 1080×1920 thumbnail, and updates catalogs.

---

## 🚀 Invoking the Director

To invoke the director agent in Antigravity:
```text
"Invoke the faceless-video-director to create a new Short on [TOPIC]"
```
Or run the master CLI engine directly:
```bash
.venv/bin/python scripts/faceless_video_director.py --topic "The Fermi Paradox" --genre "scifi"
```
