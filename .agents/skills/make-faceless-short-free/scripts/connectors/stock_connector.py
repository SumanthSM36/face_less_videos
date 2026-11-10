"""
stock_connector.py — Safe, multi-source open stock footage aggregator.
Routes across NASA, Wikimedia Commons, Archive.org, and optional Pexels/Pixabay.
"""

import os
import requests
from .wikimedia_connector import search_wikimedia_videos
from .nasa_connector import search_nasa_videos
from .archive_org_connector import search_archive_org_videos
from .pexels_connector import search_pexels_videos
from .pixabay_connector import search_pixabay_videos


def search_all_open_sources(query, limit=5, prefer_nasa=False):
    """
    Search all active connectors and return unified candidate video list.
    """
    candidates = []

    # 1. Pexels (if key provided, highest quality vertical footage)
    pexels_hits = search_pexels_videos(query, limit=limit)
    if pexels_hits:
        candidates.extend(pexels_hits)

    # 2. Pixabay (if key provided)
    pixabay_hits = search_pixabay_videos(query, limit=limit)
    if pixabay_hits:
        candidates.extend(pixabay_hits)

    # 3. NASA (if astronomy, earth, planetary)
    space_keywords = ["space", "earth", "planet", "nasa", "star", "galaxy", "moon", "sun", "orbit", "mars", "astronomy"]
    is_space = prefer_nasa or any(k in query.lower() for k in space_keywords)
    if is_space:
        nasa_hits = search_nasa_videos(query, limit=limit)
        if nasa_hits:
            candidates.extend(nasa_hits)

    # 4. Wikimedia Commons (universal public domain & CC)
    wiki_hits = search_wikimedia_videos(query, limit=limit)
    if wiki_hits:
        candidates.extend(wiki_hits)

    # 5. Archive.org (historical, vintage, documentary)
    archive_hits = search_archive_org_videos(query, limit=limit)
    if archive_hits:
        candidates.extend(archive_hits)

    return candidates


def fetch_open_stock_video(query, out_path, prefer_nasa=False):
    """
    Search available open connectors and download the best candidate video.
    Returns True if downloaded successfully, False otherwise.
    """
    candidates = search_all_open_sources(query, limit=3, prefer_nasa=prefer_nasa)

    for cand in candidates:
        url = cand["url"]
        try:
            print(f"  [Open Connector] Checking clip from {cand['source'].upper()}: '{cand['title'][:40]}'")
            r = requests.get(url, stream=True, timeout=12, headers={"User-Agent": "AntigravityVideo/1.0"})
            if r.status_code == 200:
                content_len = int(r.headers.get("content-length", 0))
                # Skip giant files (> 45 MB) to ensure fast rendering
                if content_len > 45 * 1024 * 1024:
                    print(f"    (Skipping large file: {content_len / 1024 / 1024:.1f} MB)")
                    continue

                print(f"  [Open Connector] Downloading clip from {cand['source'].upper()}...")
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                if os.path.getsize(out_path) > 100000:
                    return True
        except Exception as e:
            print(f"    (Notice: Failed downloading from {cand['source']}: {e})")
            continue

    return False
