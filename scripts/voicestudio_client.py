#!/usr/bin/env python3
"""
voicestudio_client.py — VoiceStudio (debpalash/voicestudio) Integration Client.

Connects to VoiceStudio's local REST API & MCP server (default: http://127.0.0.1:3900)
to provide local, zero-cost, ElevenLabs-quality voice cloning and voice design.
"""

import os
import sys
import json
import urllib.request
import urllib.error

VOICESTUDIO_HOST = os.environ.get("OMNIVOICE_HOST", "http://127.0.0.1:3900")


def check_voicestudio_running() -> bool:
    """Checks if VoiceStudio backend is active and reachable."""
    try:
        url = f"{VOICESTUDIO_HOST}/api/health"
        req = urllib.request.Request(url, headers={"User-Agent": "Antigravity/1.0"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            return resp.status in (200, 204)
    except Exception:
        # Fallback check on root /mcp
        try:
            url = f"{VOICESTUDIO_HOST}/mcp"
            req = urllib.request.Request(url, headers={"User-Agent": "Antigravity/1.0"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                return resp.status in (200, 204, 404, 405)
        except Exception:
            return False


def list_profiles():
    """Lists available voice profiles from VoiceStudio."""
    url = f"{VOICESTUDIO_HOST}/api/voices"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as e:
        print(f"⚠️ Could not list VoiceStudio profiles: {e}")
        return []


def design_voice(description: str, name: str) -> str:
    """
    Designs a unique voice persona using natural language description.
    Returns the created profile_id.
    """
    url = f"{VOICESTUDIO_HOST}/api/voice/design"
    payload = json.dumps({
        "name": name,
        "description": description
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            profile_id = data.get("profile_id") or data.get("id")
            print(f"✅ Voice designed successfully: {name} (ID: {profile_id})")
            return profile_id
    except Exception as e:
        print(f"❌ Failed to design voice with VoiceStudio: {e}")
        return None


def synthesize_speech(text: str, output_path: str, profile_id: str = None, language: str = "en"):
    """
    Synthesizes speech using VoiceStudio's local engine.
    Saves audio directly to output_path.
    """
    url = f"{VOICESTUDIO_HOST}/api/generate"
    payload_data = {
        "text": text,
        "language": language,
        "format": "wav" if output_path.endswith(".wav") else "mp3"
    }
    if profile_id:
        payload_data["profile_id"] = profile_id

    payload = json.dumps(payload_data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60.0) as resp:
            with open(output_path, "wb") as f:
                f.write(resp.read())
            print(f"✅ VoiceStudio synthesized {len(text)} chars -> {output_path}")
            return output_path
    except Exception as e:
        print(f"❌ VoiceStudio synthesis error: {e}")
        raise


if __name__ == "__main__":
    is_up = check_voicestudio_running()
    print(f"VoiceStudio server ({VOICESTUDIO_HOST}): {'ONLINE 🟢' if is_up else 'OFFLINE ⚪'}")
