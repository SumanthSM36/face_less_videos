"""
youtube_connector.py — YouTube Channel Integration & Automated Short Uploader.
Uses YouTube Data API v3 and OAuth 2.0.
"""

import os
import json
import sys
import socket

# Force IPv4 resolution to prevent macOS IPv6 route stall/timeout
_orig_getaddrinfo = socket.getaddrinfo
def _getaddrinfo_ipv4_first(*args, **kwargs):
    res = _orig_getaddrinfo(*args, **kwargs)
    ipv4 = [r for r in res if r[0] == socket.AF_INET]
    return ipv4 if ipv4 else res
socket.getaddrinfo = _getaddrinfo_ipv4_first

CONNECTOR_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(CONNECTOR_DIR, "../../../../../"))
CLIENT_SECRETS_FILE = os.path.join(WORKSPACE_ROOT, "client_secret.json")
TOKEN_FILE = os.path.join(WORKSPACE_ROOT, "token.json")

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]


def get_youtube_service():
    """
    Authenticate and return an authorized YouTube Data API service instance.
    """
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                raise FileNotFoundError(
                    f"client_secret.json not found at {CLIENT_SECRETS_FILE}.\n"
                    "To connect your YouTube channel, download OAuth 2.0 Client credentials (Desktop App) "
                    "from Google Cloud Console (https://console.cloud.google.com/apis/credentials) and place it as 'client_secret.json' in your workspace root."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def get_channel_info():
    """
    Get profile stats for the connected YouTube channel.
    """
    youtube = get_youtube_service()
    request = youtube.channels().list(part="snippet,statistics,contentDetails", mine=True)
    response = request.execute()

    items = response.get("items", [])
    if not items:
        return {"error": "No channel found for authenticated account."}

    channel = items[0]
    snippet = channel.get("snippet", {})
    stats = channel.get("statistics", {})

    return {
        "channel_id": channel.get("id"),
        "title": snippet.get("title"),
        "custom_url": snippet.get("customUrl"),
        "subscribers": stats.get("subscriberCount"),
        "total_views": stats.get("viewCount"),
        "video_count": stats.get("videoCount"),
        "description": snippet.get("description", "")[:120]
    }


def upload_youtube_short(video_path, title, description="", tags=None, privacy_status="private"):
    """
    Upload a short video to YouTube.
    privacy_status: 'private', 'unlisted', or 'public'.
    """
    from googleapiclient.http import MediaFileUpload

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    youtube = get_youtube_service()

    # Append #shorts tag for algorithm discovery
    full_title = title if "#shorts" in title.lower() else f"{title} #shorts"
    full_desc = f"{description}\n\n#shorts #shortsvideo #viral"

    body = {
        "snippet": {
            "title": full_title[:100],
            "description": full_desc[:5000],
            "tags": tags or ["shorts", "short", "educational"],
            "categoryId": "27"  # Education
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, chunksize=1024*1024*4, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Uploading: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    video_url = f"https://youtube.com/shorts/{video_id}"

    return {
        "success": True,
        "video_id": video_id,
        "video_url": video_url,
        "privacy": privacy_status
    }
