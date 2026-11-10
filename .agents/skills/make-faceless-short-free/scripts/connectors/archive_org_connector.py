"""
archive_org_connector.py — Internet Archive Open Video Library Connector.
Public domain and Creative Commons archival footage (prelinger archive, historical reels, nature).
Zero API key needed.
"""

import requests
import urllib.parse


def search_archive_org_videos(query, limit=3):
    """
    Search Internet Archive (archive.org) for public domain videos.
    Returns list of direct video download URLs.
    """
    clean_query = urllib.parse.quote(query)
    # Strictly limit to verified public domain archives (Prelinger, US Fedflix, Public Domain movies)
    url = (
        f"https://archive.org/advancedsearch.php?q={clean_query}+AND+mediatype:movies+AND+(collection:prelinger+OR+collection:fedflix+OR+licenseurl:*publicdomain*)"
        f"&fl[]=identifier,title,description&sort[]=-downloads&rows={limit}&page=1&output=json"
    )

    try:
        r = requests.get(url, timeout=15)
        docs = r.json().get("response", {}).get("docs", [])
        results = []

        for doc in docs:
            ident = doc.get("identifier")
            title = doc.get("title", ident)
            if not ident:
                continue

            # Fetch metadata files for this item
            meta_url = f"https://archive.org/metadata/{ident}/files"
            m_resp = requests.get(meta_url, timeout=10)
            files = m_resp.json().get("result", [])

            # Find best MP4
            mp4_file = next(
                (f.get("name") for f in files if f.get("name", "").endswith(".mp4") and "512kb" in f.get("name", "").lower()),
                next((f.get("name") for f in files if f.get("name", "").endswith(".mp4")), None)
            )

            if mp4_file:
                download_url = f"https://archive.org/download/{ident}/{urllib.parse.quote(mp4_file)}"
                results.append({
                    "title": title,
                    "url": download_url,
                    "source": "archive_org",
                    "identifier": ident
                })

        return results
    except Exception as e:
        print(f"Archive.org search notice: {e}")
        return []
