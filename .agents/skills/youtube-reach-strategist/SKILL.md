---
name: youtube-reach-strategist
description: Master YouTube SEO, viral reach, and metadata optimization agent. Analyzes video scripts and topics using real-time YouTube search trend data to generate high-CTR titles (psychological hook archetypes under 55 chars for Shorts), retention-driving descriptions (above-the-fold snippet, contextual synopsis, comment-magnet CTA, chapters, hashtags), and 500-char semantic tag packs tailored to maximize reach on YouTube Browse, Search, and the Shorts feed.
---

# YouTube Reach Strategist & Viral Metadata Agent

The `youtube-reach-strategist` agent maximizes organic reach, search authority, and viewer click-through rates (CTR) on YouTube Shorts and vertical faceless video productions.

## Core Capabilities

1. **Real-Time YouTube Trend Mining:**
   - Queries live YouTube search autocomplete trends via Google Suggest API to capture what audiences are actively searching in real-time.
   - Extracts trending keywords, semantic entity clusters, and high-velocity search queries.

2. **High-CTR Title Matrix (5 Hook Archetypes):**
   - **The Paradox / Mind-Bender (Score 96):** Subverts conventional wisdom or introduces impossible conflict.
   - **Curiosity Gap / Open Loop (Score 94):** Compels the viewer to click to resolve mystery.
   - **Emotional / Character Climax (Score 92):** Heartwarming twist or heroic stakes.
   - **High Stakes & Peril (Score 91):** Danger, warnings, and urgent drama.
   - **Search Intent Keyword-First (Score 88):** Front-loads target keywords for perennial search traffic.
   - Enforces **Mobile Safe Zones**: Under 55 characters for Shorts (preventing title truncation on smartphone feeds).

3. **High-Retention Description Architecture:**
   - **Above-The-Fold Snippet (<150 chars):** Displayed in Google SERP and YouTube Search cards.
   - **Contextual Narrative & LSI Keywords:** Entity-dense story summary reinforcing algorithm topical authority.
   - **Comment-Trigger CTA:** Targeted question prompting viewers to comment (YouTube's #1 early velocity signal).
   - **Pinned Comment Recommendation:** Pre-written pinned comment to boost comment threads within 5 minutes of release.
   - **Key Moments / Chapters:** Timestamped navigational anchors.
   - **5 Curated Strategic Hashtags:** Blends broad discovery (`#Shorts`) with niche tags (`#PipTheRobot`, `#SciFiShorts`).

4. **500-Character Semantic Tag Pack:**
   - Tier 1: Core Exact-Match Entities & Live Trends.
   - Tier 2: Category & Broad Genre Terms.
   - Tier 3: Long-Tail Search Intent Phrases.
   - Tier 4: Common Search Misspellings.
   - Strictly bounded within YouTube's 500-character ceiling.

## CLI & Pipeline Invocation

```bash
# Run metadata optimizer on any topic or script
python3 scripts/youtube_reach_optimizer.py \
  --topic "Pip and the Lost Battery" \
  --genre pip \
  --format shorts \
  --markdown \
  --output output/pip_metadata.md
```
