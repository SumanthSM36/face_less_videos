"""
wikimedia_connector.py — 100% Free & Safe Wikimedia Commons Open Media Connector.
No API key required. Sourced from Wikimedia Commons public domain & Creative Commons catalogue.
"""

import re
import urllib.parse
import requests


def search_wikimedia_videos(query, limit=3):
    """
    Search Wikimedia Commons for open video files.
    Returns list of direct video download URLs.
    """
    clean_query = re.sub(r"[^a-zA-Z0-9\s]", "", query).strip()
    if not clean_query:
        clean_query = "nature"

    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filemime:video/webm {clean_query}",
        "gsrnamespace": "6",
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|mime|size",
    }
    headers = {"User-Agent": "AntigravityFacelessShorts/1.0 (https://github.com)"}

    try:
        r = requests.get("https://commons.wikimedia.org/w/api.php", params=params, headers=headers, timeout=15)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        results = []
        for pid, page in pages.items():
            ii = page.get("imageinfo", [{}])[0]
            url = ii.get("url")
            clean_path = url.split("?")[0].lower() if url else ""
            if url and any(clean_path.endswith(ext) for ext in [".webm", ".mp4", ".ogv"]):
                # Ensure URL is properly quoted
                clean_url = urllib.parse.quote(url, safe=":/%?=&")
                results.append({
                    "title": page.get("title", ""),
                    "url": clean_url,
                    "source": "wikimedia"
                })
        return results
    except Exception as e:
        print(f"Wikimedia search warning: {e}")
        return []
