"""
pexels_connector.py — Pexels Free Stock Video Connector.
Accesses millions of HD portrait (9:16) stock videos.
Works with free Pexels API key from https://www.pexels.com/api/
"""

import os
import requests


def search_pexels_videos(query, limit=3, orientation="portrait"):
    """
    Search Pexels API for vertical stock video clips.
    """
    api_key = os.environ.get("PEXELS_API_KEY")
    if not api_key:
        return []

    headers = {"Authorization": api_key}
    params = {
        "query": query,
        "orientation": orientation,
        "per_page": limit,
    }

    try:
        r = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params, timeout=12)
        if r.status_code != 200:
            return []

        videos = r.json().get("videos", [])
        results = []
        for vid in videos:
            # Find best HD vertical link
            vfiles = vid.get("video_files", [])
            # Sort by height descending
            vfiles.sort(key=lambda x: x.get("height", 0), reverse=True)
            chosen = next((f["link"] for f in vfiles if f.get("link")), None)
            if chosen:
                results.append({
                    "title": f"Pexels Video {vid.get('id')}",
                    "url": chosen,
                    "source": "pexels",
                    "width": vid.get("width"),
                    "height": vid.get("height")
                })
        return results
    except Exception as e:
        print(f"Pexels connector notice: {e}")
        return []
