# Faceless Video & Shorts Production Rules

When authoring or generating short-form vertical videos (YouTube Shorts, TikTok, Instagram Reels), adhere to these mandatory production rules:

## 1. Visual Safe Zones (1080×1920)
- **Top 15% (0 - 280px):** Reserve for platform search, profile links, and status bar. Do not place critical text here.
- **Bottom 20% (1540 - 1920px):** Reserve for platform title, description, audio pill, and engagement buttons. Subtitles must stay in the safe vertical band between Y=1350px and Y=1500px.
- **Right Edge 15% (920 - 1080px):** Avoid right side icon column (like, comment, share, bookmark).
- **Core Action:** Keep primary action centered horizontally and vertically between 20% and 75%.

## 2. Pacing & Script Grammar
- **Hook (0 to 2.5s):** The very first sentence and frame must immediately deliver visual and intellectual curiosity. Frame 0 is thumbnail-grade.
- **Pacing:** 2.5 to 3.5 seconds per visual cut. Never linger on a static frame.
- **Sentence Length:** Keep sentences punchy (under 12 words per sentence).
- **Infinite Loop:** End on the key revelation or punchline that blends directly back into the opening hook phrase so viewers watch twice.

## 3. Kinetic Subtitles
- Format: ASS subtitles with high-contrast primary color (Yellow `#00FFFF` or White `#FFFFFF`) and a thick dark border (`Outline=6`).
- Split dialogue into 2–4 word bursts so text pops on screen in tight rhythm with spoken syllables.

## 4. Audio & Ducking
- Voice is the hero track: clean, normalized to approximately -16 LUFS.
- Background music must be ducked to 15%–25% volume during speech.

## 5. YouTube Monetization & Anti-Demonetization Safeguards
- **Original Value First:** Never scrape generic articles or generate cookie-cutter text. Every video must feature an original creative story, bespoke insight, or deep-dive educational analysis.
- **Transformative Editing:** Never loop single unedited stock clips. Layer kinetic captions, scene cuts every 2.5–3.5s, Ken Burns camera motion, and ducked musical scores.
- **Natural Delivery:** Avoid monotone or robotic voices. Use expressive neural narration with calibrated speed and pacing.
- **Unique Assets:** For story shorts, use bespoke scene artwork and character continuity. Unique creative animation is 100% eligible for the YouTube Partner Program (YPP).

## 6. Strict Copyright & Content ID Immunity Rules
- **Audio Immunity:** Background music must strictly be generated via algorithmic harmonic synthesis (`aevalsrc`) or verified Public Domain/CC0 tracks. Never use unverified external commercial MP3s.
- **Visual Sourcing Guard:** Open video search is restricted to verified Public Domain (NASA under 17 U.S.C. § 105, Prelinger Archive, FedFlix) or CC-BY/Pexels commercial-licensed media.
- **Fingerprint Transformation:** Always apply the cinematic 35mm grain, color curves, lens vignette, and burned ASS captions to generate a 100% unique pixel fingerprint, eliminating false-positive Content ID claims.

## 7. Dynamic Cartoon & Animation Interstitials (High-Engagement Inserts)
- **Visual Variety:** Intersperse stylized animation or expressive cartoon-like reaction clips/illustrations in between realistic or archival documentary scenes.
- **Dopamine & Retention:** Pure static or realistic sequences risk audience fatigue. Adding fun, animated visual metaphors or stylized cuts every 2–3 scenes drastically boosts watch time, viewer delight, and Shorts algorithm retention.

## 8. Strict Visual Fidelity & Asset Quality Gate (Anti-Blur Safeguard)
- **Zero Low-Resolution Fallbacks:** Never accept blurry, deformed, or low-resolution fallback images (e.g. 576x1024 or sub-500KB compressed renders).
- **Mandatory Quality Threshold:** All cartoon/animated frames must be high-definition (minimum 768x1376 native, rendered at 1080x1920) with crisp 3D Pixar/Disney RenderMan lighting, tactile metallic textures, and character fidelity.
- **Fail-Safe Policy:** If high-definition AI image capacity is temporarily exhausted, never substitute degraded models. Pause and inform the user or utilize verified masterwork assets to maintain uncompromising visual beauty.

## 9. YouTube Channel Pre-Flight Verification & Duplicate Prevention Gate
- **Mandatory Pre-Flight Scan:** Before writing a script, generating visual assets, or rendering a new video, the agent MUST scan the authenticated YouTube channel's uploaded catalog (`scripts/check_youtube_duplicates.py`).
- **Zero Duplicates Policy:** If a proposed story topic, historical event, scientific paradox, or character adventure has already been covered on the channel, HALT production immediately.
- **Collision Resolution:** Present the user with the direct link to the published video (`https://youtube.com/shorts/<id>`) and provide 3 fresh, unexplored alternative angles or chronological sequels. Never produce redundant content.
