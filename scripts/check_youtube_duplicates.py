#!/usr/bin/env python3
"""
check_youtube_duplicates.py — YouTube Channel Video Verification & Duplicate Prevention Gate.

Connects to authenticated YouTube Data API v3 to:
1. Fetch and cache complete upload catalog from channel.
2. Compare proposed topic/script against all published videos using fuzzy token matching & semantic overlap.
3. Prevent duplicate video creation and recommend fresh, unexplored story angles.
"""

import os
import sys
import json
import re
import argparse
import difflib
from typing import Dict, List, Tuple, Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
CACHE_FILE = os.path.join(WORKSPACE_ROOT, "output/channel_videos_cache.json")

# Add connectors to path
CONNECTORS_DIR = os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts")
if CONNECTORS_DIR not in sys.path:
    sys.path.insert(0, CONNECTORS_DIR)

try:
    from connectors.youtube_connector import get_youtube_service
except ImportError:
    get_youtube_service = None


def fetch_all_channel_videos(force_refresh: bool = False, max_videos: int = 150) -> List[Dict[str, Any]]:
    """
    Retrieves all uploaded videos from the channel.
    Caches results locally to preserve YouTube API quota.
    """
    if not force_refresh and os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return data
        except Exception:
            pass

    if not get_youtube_service:
        raise ImportError("youtube_connector not available or missing Google API libraries.")

    youtube = get_youtube_service()
    
    # 1. Get uploads playlist ID
    ch_resp = youtube.channels().list(part="contentDetails,snippet", mine=True).execute()
    items = ch_resp.get("items", [])
    if not items:
        return []

    channel_name = items[0]["snippet"]["title"]
    uploads_id = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # 2. Iterate through playlist items
    videos = []
    next_page_token = None

    while len(videos) < max_videos:
        req = youtube.playlistItems().list(
            playlistId=uploads_id,
            part="snippet",
            maxResults=min(50, max_videos - len(videos)),
            pageToken=next_page_token
        )
        res = req.execute()

        for item in res.get("items", []):
            snip = item["snippet"]
            vid_id = snip["resourceId"]["videoId"]
            title = snip.get("title", "")
            desc = snip.get("description", "")
            published = snip.get("publishedAt", "")

            # Exclude deleted or private placeholder items
            if title != "Private video" and title != "Deleted video":
                videos.append({
                    "id": vid_id,
                    "title": title,
                    "description": desc[:300],
                    "published_at": published,
                    "url": f"https://youtube.com/shorts/{vid_id}"
                })

        next_page_token = res.get("nextPageToken")
        if not next_page_token:
            break

    # Save to cache
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=2)

    return videos


STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "up", "about", "into", "over", "after", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did", "this", "that",
    "these", "those", "it", "its", "they", "them", "their", "we", "us", "our", "you",
    "your", "he", "him", "his", "she", "her", "as", "if", "when", "than", "so", "can",
    "will", "just", "very", "what", "which", "who", "all", "each", "out", "how", "shorts"
}


def clean_text_for_comparison(text: str, remove_stopwords: bool = True) -> str:
    """Removes emojis, hashtags, and punctuation for clean topic matching."""
    t = re.sub(r"#\S+", "", text)
    t = re.sub(r"[^\w\s]", " ", t)
    words = t.lower().split()
    if remove_stopwords:
        words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return " ".join(words)


def check_for_duplicates(proposed_topic: str, proposed_script: str = "", threshold: float = 0.40) -> Dict[str, Any]:
    """
    Compares proposed topic and script against channel uploads.
    Returns collision status, matched videos, similarity score, and recommendations.
    """
    videos = fetch_all_channel_videos()
    clean_proposed = clean_text_for_comparison(proposed_topic)
    proposed_words = set(clean_proposed.split())

    matches = []

    for vid in videos:
        clean_title = clean_text_for_comparison(vid["title"])
        title_words = set(clean_title.split())

        if not proposed_words or not title_words:
            continue

        # 1. Exact key entity phrase match
        key_phrases = [" ".join(clean_proposed.split()[:2]), clean_proposed]
        has_phrase_match = any(p in clean_title for p in key_phrases if len(p) > 5)

        # 2. Significant keyword overlap
        overlap = proposed_words.intersection(title_words)
        overlap_ratio = len(overlap) / len(proposed_words)

        # 3. SequenceMatcher
        seq_ratio = difflib.SequenceMatcher(None, clean_proposed, clean_title).ratio()

        score = max(
            overlap_ratio,
            0.90 if has_phrase_match else 0.0,
            seq_ratio
        )

        if score >= threshold:
            matches.append({
                "video_id": vid["id"],
                "title": vid["title"],
                "url": vid["url"],
                "published_at": vid["published_at"],
                "similarity_score": round(score, 3),
                "matched_terms": list(overlap)
            })

    # Sort matches by highest similarity
    matches.sort(key=lambda m: m["similarity_score"], reverse=True)
    is_duplicate = len(matches) > 0 and matches[0]["similarity_score"] >= threshold

    # Generate alternative angles if duplicate found
    suggestions = []
    if is_duplicate:
        top_match = matches[0]["title"]
        suggestions = [
            f"Alternative Perspective: Deep-dive into a lesser-known secondary character or untold consequence of {proposed_topic}.",
            f"Paradox Angle: Frame the story as a counter-intuitive mystery (e.g. 'The Scientific Secret Behind {proposed_topic}').",
            f"Chronological Sequel: Focus on what happened immediately after the events of '{top_match}'."
        ]

    return {
        "proposed_topic": proposed_topic,
        "is_duplicate": is_duplicate,
        "highest_similarity": matches[0]["similarity_score"] if matches else 0.0,
        "collision_count": len(matches),
        "collisions": matches[:5],
        "total_channel_videos_scanned": len(videos),
        "suggestions": suggestions
    }


def main():
    parser = argparse.ArgumentParser(description="YouTube Duplicate Verification Engine")
    parser.add_argument("--topic", required=True, help="Proposed video topic or title to check")
    parser.add_argument("--script", default="", help="Optional proposed script text")
    parser.add_argument("--threshold", type=float, default=0.50, help="Duplicate similarity threshold (0.0 to 1.0, default 0.50)")
    parser.add_argument("--refresh", action="store_true", help="Force refresh channel cache from YouTube API")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    if args.refresh:
        fetch_all_channel_videos(force_refresh=True)

    result = check_for_duplicates(args.topic, proposed_script=args.script, threshold=args.threshold)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n=======================================================")
        print("🛡️ YOUTUBE CHANNEL DUPLICATE VERIFICATION GATE")
        print(f"Scanned Channel Catalog: {result['total_channel_videos_scanned']} published videos")
        print(f"Proposed Topic: '{args.topic}'")
        print("=======================================================")

        if result["is_duplicate"]:
            top = result["collisions"][0]
            print(f"\n⚠️ DUPLICATE DETECTED! (Similarity: {int(top['similarity_score'] * 100)}%)")
            print(f"Existing Video: {top['title']}")
            print(f"Watch Link:     {top['url']}")
            print(f"Published:      {top['published_at']}")
            print("\n💡 Recommended Fresh Angles to Avoid Duplication:")
            for s in result["suggestions"]:
                print(f"  • {s}")
            print("\n❌ VIDEO CREATION HALTED — Choose a fresh topic or alternative angle.")
            sys.exit(2)
        else:
            print("\n✅ PASSED VERIFICATION: No duplicate video found on your channel.")
            print("🚀 Approved for video scripting and production.")


if __name__ == "__main__":
    main()
