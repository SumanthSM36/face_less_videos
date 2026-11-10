#!/usr/bin/env python3
"""
voicestudio_client.py — VoiceStudio (debpalash/voicestudio) Integration Client.

Connects to VoiceStudio's local OpenAI-compatible REST API & backend
(default: http://127.0.0.1:3900) running with Apple Silicon Metal (MPS) acceleration.
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
        url = f"{VOICESTUDIO_HOST}/health"
        req = urllib.request.Request(url, headers={"User-Agent": "Antigravity/1.0"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("status") == "ok"
    except Exception:
        return False


def get_backend_info():
    """Gets VoiceStudio device and status info."""
    url = f"{VOICESTUDIO_HOST}/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def list_profiles():
    """Lists available voice profiles from VoiceStudio."""
    url = f"{VOICESTUDIO_HOST}/profiles"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"⚠️ Could not list VoiceStudio profiles: {e}")
        return []


def synthesize_speech(
    text: str,
    output_path: str,
    voice: str = "8b340e19",  # DeepVoiceStudioPure
    model: str = "omnivoice",
    speed: float = 1.0,
    instruct: str = None
) -> str:
    """
    Synthesizes speech using VoiceStudio's local hardware-accelerated OpenAI API.
    Saves audio directly to output_path (.mp3 or .wav).
    """
    url = f"{VOICESTUDIO_HOST}/v1/audio/speech"
    fmt = "wav" if output_path.endswith(".wav") else "mp3"
    payload_data = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": fmt,
        "speed": speed,
        "num_step": 48,
        "guidance_scale": 1.8,
        "denoise": True,
        "preprocess_prompt": True
    }
    if instruct:
        payload_data["instruct"] = instruct

    payload = json.dumps(payload_data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120.0) as resp:
            with open(output_path, "wb") as f:
                f.write(resp.read())
            print(f"✅ VoiceStudio synthesized {len(text)} chars -> {output_path}")
            return output_path
    except Exception as e:
        print(f"❌ VoiceStudio synthesis error: {e}")
        raise


def transcribe_audio(audio_path: str) -> dict:
    """Transcribes an audio file with timestamps using VoiceStudio's local ASR."""
    import mimetypes
    url = f"{VOICESTUDIO_HOST}/v1/audio/transcriptions"
    
    boundary = "----WebKitFormBoundaryVoiceStudio7MA4YWxkTrZu0gW"
    data = []
    
    # model field
    data.append(f"--{boundary}".encode())
    data.append(b'Content-Disposition: form-data; name="model"')
    data.append(b"")
    data.append(b"whisper")
    
    # response_format field
    data.append(f"--{boundary}".encode())
    data.append(b'Content-Disposition: form-data; name="response_format"')
    data.append(b"")
    data.append(b"verbose_json")
    
    # file field
    filename = os.path.basename(audio_path)
    data.append(f"--{boundary}".encode())
    data.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode())
    data.append(b"Content-Type: audio/mpeg")
    data.append(b"")
    with open(audio_path, "rb") as f:
        data.append(f.read())
        
    data.append(f"--{boundary}--".encode())
    data.append(b"")
    
    body = b"\r\n".join(data)
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    with urllib.request.urlopen(req, timeout=30.0) as resp:
        return json.loads(resp.read().decode("utf-8"))


def transcribe_to_vtt(audio_path: str, vtt_path: str):
    """Generates a WebVTT subtitle file from VoiceStudio's local transcription."""
    result = transcribe_audio(audio_path)
    segments = result.get("segments", [])
    
    def fmt_vtt_time(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int((sec - int(sec)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

    lines = ["WEBVTT\n"]
    if not segments:
        dur = result.get("duration", 5.0)
        lines.append(f"00:00:00.000 --> {fmt_vtt_time(dur)}")
        lines.append(result.get("text", "").strip())
        lines.append("")
    else:
        for idx, seg in enumerate(segments):
            start = fmt_vtt_time(seg.get("start", 0.0))
            end = fmt_vtt_time(seg.get("end", 0.0))
            txt = seg.get("text", "").strip()
            lines.append(f"{start} --> {end}")
            lines.append(txt)
            lines.append("")

    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"✅ VoiceStudio transcribed audio to VTT: {vtt_path}")
    return vtt_path


if __name__ == "__main__":
    is_up = check_voicestudio_running()
    info = get_backend_info() if is_up else {}
    device = info.get("device", "unknown")
    print(f"VoiceStudio server ({VOICESTUDIO_HOST}): {'ONLINE 🟢 (Device: ' + device.upper() + ')' if is_up else 'OFFLINE ⚪'}")
    if is_up:
        profiles = list_profiles()
        print(f"Available profiles: {len(profiles)}")
        for p in profiles:
            print(f" - [{p.get('id')}] {p.get('name')} ({p.get('language')})")
