"""
pixabay_connector.py — Pixabay Free Stock Video Connector.
Accesses thousands of royalty-free stock clips and animations.
Works with free Pixabay API key from https://pixabay.com/api/docs/
"""

import os
import requests


def search_pixabay_videos(query, limit=3):
    """
    Search Pixabay API for stock video clips.
    """
    api_key = os.environ.get("PIXABAY_API_KEY")
    if not api_key:
        return []

    params = {
        "key": api_key,
        "q": query,
        "video_type": "all",
        "per_page": limit,
    }

    try:
        r = requests.get("https://pixabay.com/api/videos/", params=params, timeout=12)
        if r.status_code != 200:
            return []

        hits = r.json().get("hits", [])
        results = []
        for hit in hits:
            v_sizes = hit.get("videos", {})
            # Prefer medium or large
            chosen = v_sizes.get("medium", {}).get("url") or v_sizes.get("large", {}).get("url") or v_sizes.get("small", {}).get("url")
            if chosen:
                results.append({
                    "title": hit.get("tags", "Pixabay Clip"),
                    "url": chosen,
                    "source": "pixabay"
                })
        return results
    except Exception as e:
        print(f"Pixabay connector notice: {e}")
        return []
