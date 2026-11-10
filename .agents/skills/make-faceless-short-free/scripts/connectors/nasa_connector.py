"""
nasa_connector.py — 100% Free NASA Public Domain Image and Video Connector.
No API key required. Sourced from images-api.nasa.gov.
"""

import requests


def search_nasa_videos(query, limit=3):
    """
    Search NASA open media library for space/earth video footage.
    Returns list of direct MP4 URLs.
    """
    url = "https://images-api.nasa.gov/search"
    params = {"q": query, "media_type": "video"}

    try:
        r = requests.get(url, params=params, timeout=15)
        data = r.json()
        items = data.get("collection", {}).get("items", [])[:limit]
        results = []

        for item in items:
            title = item.get("data", [{}])[0].get("title", "")
            manifest_url = item.get("href")
            if not manifest_url:
                continue

            m_resp = requests.get(manifest_url, timeout=10)
            files = m_resp.json()
            # Pick medium or orig mp4
            mp4s = [f for f in files if isinstance(f, str) and f.endswith(".mp4")]
            if mp4s:
                # Prefer medium quality for faster download
                chosen = next((f for f in mp4s if "~medium.mp4" in f), mp4s[0])
                # Ensure https
                if chosen.startswith("http://"):
                    chosen = "https://" + chosen[7:]
                results.append({
                    "title": title,
                    "url": chosen,
                    "source": "nasa"
                })
        return results
    except Exception as e:
        print(f"NASA search warning: {e}")
        return []
