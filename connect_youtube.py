#!/usr/bin/env python3
"""
connect_youtube.py — Interactive YouTube Channel Connector & Status Checker.
Run this after placing your 'client_secret.json' in this folder.
"""

import os
import sys

# Ensure connectors can be imported
sys.path.insert(0, os.path.abspath(".agents/skills/make-faceless-short-free/scripts/connectors"))

try:
    from youtube_connector import get_channel_info, CLIENT_SECRETS_FILE, TOKEN_FILE
except ImportError as e:
    print(f"Error importing youtube_connector: {e}")
    sys.exit(1)


def main():
    print("=" * 60)
    print("🎬 YouTube Channel Connection Setup")
    print("=" * 60)

    if not os.path.exists(CLIENT_SECRETS_FILE):
        print("\n❌ client_secret.json NOT FOUND!")
        print(f"Expected location: {CLIENT_SECRETS_FILE}\n")
        print("To connect your YouTube channel, follow these 3 quick steps:")
        print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
        print("2. Enable 'YouTube Data API v3' under APIs & Services > Library.")
        print("3. Under APIs & Services > Credentials, click 'Create Credentials' > 'OAuth 2.0 Client ID':")
        print("   - Application Type: Desktop App")
        print("   - Name: Faceless Video Studio")
        print("4. Download the JSON credentials file and rename/save it as:")
        print(f"   {CLIENT_SECRETS_FILE}")
        print("\nOnce placed, rerun this script to authenticate your channel.\n")
        sys.exit(1)

    print("\n✅ Found client_secret.json!")
    if os.path.exists(TOKEN_FILE):
        print("🔑 Existing authorization token found. Checking channel status...")
    else:
        print("🌐 Opening your default browser for a one-time Google OAuth authorization...")

    try:
        info = get_channel_info()
        if "error" in info:
            print(f"❌ Error: {info['error']}")
            sys.exit(1)

        print("\n🎉 SUCCESSFULLY CONNECTED TO YOUTUBE CHANNEL!")
        print("-" * 40)
        print(f"  Channel Title : {info.get('title')}")
        print(f"  Channel ID    : {info.get('channel_id')}")
        print(f"  Custom URL    : {info.get('custom_url') or 'N/A'}")
        print(f"  Subscribers   : {info.get('subscribers', 0)}")
        print(f"  Total Views   : {info.get('total_views', 0)}")
        print(f"  Total Videos  : {info.get('video_count', 0)}")
        print("-" * 40)
        print("✅ You are now ready to publish Shorts directly from chat or MCP tools!")

    except Exception as exc:
        print(f"\n❌ Authentication failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
