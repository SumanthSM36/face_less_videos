#!/usr/bin/env python3
"""
video_studio_mcp.py — Standard Open-Source MCP Server for Complete Video Generation.
Full JSON-RPC 2.0 protocol compliance over stdio.
Exposes a comprehensive suite of video tools:
1. generate_faceless_short
2. search_open_stock_videos
3. synthesize_speech
4. burn_subtitles
5. reframe_to_vertical
6. trim_video
7. concat_videos
8. mix_audio_ducking
9. create_ken_burns_clip
10. extract_frames
11. inspect_media_file
"""

import json
import os
import re
import subprocess
import sys
import asyncio
import warnings

warnings.filterwarnings("ignore")

# Workspace Paths
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(SERVER_DIR, ".."))
VENV_PYTHON = os.path.join(WORKSPACE_ROOT, ".venv/bin/python")
FFMPEG_EXE = os.path.join(WORKSPACE_ROOT, ".venv/bin/ffmpeg")
SKILL_SCRIPT = os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts/generate_short.py")

# Ensure connectors are importable
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts"))
try:
    from connectors.stock_connector import search_all_open_sources, fetch_open_stock_video
    from connectors.wikimedia_connector import search_wikimedia_videos
    from connectors.nasa_connector import search_nasa_videos
    from connectors.archive_org_connector import search_archive_org_videos
except Exception as e:
    search_all_open_sources = None
    fetch_open_stock_video = None


def run_ffmpeg(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"FFmpeg command failed: {' '.join(cmd)}\n{p.stdout}")
    return p.stdout


def get_tool_definitions():
    return [
        {
            "name": "generate_faceless_short",
            "description": "Generate an end-to-end 9:16 vertical short video (1080x1920 MP4) with neural voiceover, dynamic kinetic captions, ducked music, and open-source visuals.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title or concept of the short video"},
                    "genre": {
                        "type": "string",
                        "enum": ["general", "mystery", "scifi", "mythology", "philosophy", "cartoon", "psychology", "history"],
                        "default": "general",
                        "description": "Content genre that sets the voice, musical harmonics, color grade, and atmosphere"
                    },
                    "script": {"type": "string", "description": "Narration script (80-140 words recommended)"},
                    "visuals": {
                        "type": "string",
                        "enum": ["stock", "ai", "motion", "broll"],
                        "default": "stock",
                        "description": "Visual engine: 'stock' (Wikimedia/NASA/Archive open footage), 'ai' (AI stills with Ken Burns zoom), 'motion' (procedural animated backdrop), or 'broll' (user custom video)"
                    },
                    "keyword": {"type": "string", "description": "Search keyword for stock clips (e.g. 'earth', 'space', 'ocean', 'city')"},
                    "broll_path": {"type": "string", "description": "Path to local video file for broll mode"},
                    "voice": {"type": "string", "default": "en-US-ChristopherNeural", "description": "Neural voice ID"},
                    "output_path": {"type": "string", "description": "Destination MP4 path"}
                },
                "required": ["title", "script"]
            }
        },
        {
            "name": "search_open_stock_videos",
            "description": "Search open-access, public domain, and Creative Commons video repositories (NASA, Wikimedia Commons, Archive.org, Pexels, Pixabay).",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query terms"},
                    "limit": {"type": "integer", "default": 5, "description": "Max results to return"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "synthesize_speech",
            "description": "Synthesize studio-quality voiceover audio (.mp3) from text using Edge-TTS.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Script text to speak"},
                    "output_path": {"type": "string", "description": "Output .mp3 file path"},
                    "voice": {"type": "string", "default": "en-US-ChristopherNeural", "description": "Voice identifier"},
                    "rate": {"type": "string", "default": "+0%", "description": "Speed offset, e.g. '+5%' or '-3%'"}
                },
                "required": ["text", "output_path"]
            }
        },
        {
            "name": "burn_subtitles",
            "description": "Burn ASS or SRT subtitle captions directly into a video with custom font sizing and safe-zone placement.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "video_path": {"type": "string", "description": "Input video file path"},
                    "subtitle_path": {"type": "string", "description": "Input .ass or .srt file path"},
                    "output_path": {"type": "string", "description": "Output video file path"}
                },
                "required": ["video_path", "subtitle_path", "output_path"]
            }
        },
        {
            "name": "reframe_to_vertical",
            "description": "Reframe or convert any horizontal (16:9) or arbitrary video into vertical 9:16 (1080x1920) with blurred background or smart center crop.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "input_path": {"type": "string", "description": "Source video path"},
                    "output_path": {"type": "string", "description": "Output vertical video path"},
                    "mode": {
                        "type": "string",
                        "enum": ["blur_background", "crop_fill"],
                        "default": "crop_fill",
                        "description": "'crop_fill' crops sides to fill 1080x1920; 'blur_background' fits original video centered over a blurred enlarged version"
                    }
                },
                "required": ["input_path", "output_path"]
            }
        },
        {
            "name": "trim_video",
            "description": "Trim or slice a video between start and end timestamps.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "input_path": {"type": "string", "description": "Input video path"},
                    "output_path": {"type": "string", "description": "Output video path"},
                    "start_sec": {"type": "number", "description": "Start timestamp in seconds"},
                    "end_sec": {"type": "number", "description": "End timestamp in seconds"}
                },
                "required": ["input_path", "output_path", "start_sec", "end_sec"]
            }
        },
        {
            "name": "concat_videos",
            "description": "Stitch multiple video clips into one continuous video file.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "video_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Ordered list of video file paths"
                    },
                    "output_path": {"type": "string", "description": "Output concatenated video path"}
                },
                "required": ["video_paths", "output_path"]
            }
        },
        {
            "name": "mix_audio_ducking",
            "description": "Duck a background music track beneath a voice narration track so speech is clear and crisp.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "voice_path": {"type": "string", "description": "Voiceover audio file path"},
                    "music_path": {"type": "string", "description": "Background music file path"},
                    "output_path": {"type": "string", "description": "Output mixed audio path"},
                    "music_volume": {"type": "number", "default": 0.20, "description": "Volume of background music (0.1 to 0.35 recommended)"}
                },
                "required": ["voice_path", "music_path", "output_path"]
            }
        },
        {
            "name": "create_ken_burns_clip",
            "description": "Turn a static image into a dynamic vertical motion video clip (1080x1920) with smooth Ken Burns pan and zoom.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string", "description": "Input image path (.jpg or .png)"},
                    "output_path": {"type": "string", "description": "Output video path (.mp4)"},
                    "duration_sec": {"type": "number", "default": 5.0, "description": "Duration of the video clip in seconds"},
                    "direction": {"type": "string", "enum": ["zoom_in", "zoom_out"], "default": "zoom_in", "description": "Camera motion direction"}
                },
                "required": ["image_path", "output_path"]
            }
        },
        {
            "name": "extract_frames",
            "description": "Extract still images or thumbnails from a video at specified seconds.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "video_path": {"type": "string", "description": "Source video file path"},
                    "timestamp_sec": {"type": "number", "default": 0.0, "description": "Timestamp in seconds to extract"},
                    "output_image_path": {"type": "string", "description": "Target image path (.jpg or .png)"}
                },
                "required": ["video_path", "output_image_path"]
            }
        },
        {
            "name": "inspect_media_file",
            "description": "Inspect video/audio duration, dimensions, codecs, and bitrate using native FFmpeg.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "File path to inspect"}
                },
                "required": ["file_path"]
            }
        },
        {
            "name": "upload_to_youtube",
            "description": "Upload a finished short video directly to your authenticated YouTube channel.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "video_path": {"type": "string", "description": "Local MP4 video path to upload"},
                    "title": {"type": "string", "description": "Video title (includes #shorts)"},
                    "description": {"type": "string", "description": "Video description text"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "List of tags"},
                    "privacy_status": {"type": "string", "enum": ["private", "unlisted", "public"], "default": "private", "description": "Privacy status on YouTube"}
                },
                "required": ["video_path", "title"]
            }
        },
        {
            "name": "get_youtube_channel_stats",
            "description": "Get channel statistics (subscribers, views, video count) from connected YouTube channel.",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
    ]


def handle_generate_faceless_short(args):
    title = args.get("title", "Untitled Short")
    genre = args.get("genre", "general")
    script = args.get("script", "")
    visuals = args.get("visuals", "stock")
    voice = args.get("voice")
    keyword = args.get("keyword", "")
    broll = args.get("broll_path")
    out_path = args.get("output_path") or os.path.join(WORKSPACE_ROOT, f"output/{re.sub(r'[^a-zA-Z0-9_]', '_', title.lower())}.mp4")

    cmd = [
        VENV_PYTHON, SKILL_SCRIPT,
        "--title", title,
        "--genre", genre,
        "--script", script,
        "--visuals", visuals,
        "--output", out_path
    ]
    if voice:
        cmd += ["--voice", voice]
    if keyword:
        cmd += ["--keyword", keyword]
    if broll and os.path.exists(broll):
        cmd += ["--broll", broll]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if res.returncode != 0:
        return f"Error executing short video generation:\n{res.stdout}"
    return f"Success! Video created at: {out_path}\nPipeline summary:\n{res.stdout[-500:]}"


def handle_search_open_stock_videos(args):
    query = args.get("query", "")
    limit = args.get("limit", 5)

    if not search_all_open_sources:
        return "Search connectors not initialized."

    results = search_all_open_sources(query, limit=limit)
    if not results:
        return f"No open videos found for query: '{query}'"

    formatted = [f"Found {len(results)} open media assets for '{query}':"]
    for i, r in enumerate(results[:limit], 1):
        formatted.append(f"{i}. [{r.get('source', '').upper()}] {r.get('title', 'Video')}\n   URL: {r.get('url')}")
    return "\n".join(formatted)


def handle_synthesize_speech(args):
    text = args.get("text", "")
    output_path = args.get("output_path", "output/speech.mp3")
    voice = args.get("voice", "en-US-ChristopherNeural")
    rate = args.get("rate", "+0%")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cmd = [
        VENV_PYTHON, "-c",
        f"import asyncio, edge_tts; asyncio.run(edge_tts.Communicate({repr(text)}, {repr(voice)}, rate={repr(rate)}).save({repr(output_path)}))"
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if res.returncode != 0:
        return f"TTS generation error:\n{res.stdout}"
    return f"Voiceover successfully synthesized and saved to: {output_path}"


def handle_burn_subtitles(args):
    vpath = args["video_path"]
    spath = args["subtitle_path"]
    opath = args["output_path"]

    if not os.path.exists(vpath):
        return f"Error: Video not found: {vpath}"
    if not os.path.exists(spath):
        return f"Error: Subtitles not found: {spath}"

    os.makedirs(os.path.dirname(os.path.abspath(opath)), exist_ok=True)
    escaped_sub = spath.replace(":", "\\:").replace("'", "\\'")
    cmd = [
        FFMPEG_EXE, "-y", "-i", vpath,
        "-vf", f"subtitles='{escaped_sub}'",
        "-c:v", "libx264", "-c:a", "copy",
        opath
    ]
    run_ffmpeg(cmd)
    return f"Subtitles burned successfully: {opath}"


def handle_reframe_to_vertical(args):
    ipath = args["input_path"]
    opath = args["output_path"]
    mode = args.get("mode", "crop_fill")

    if not os.path.exists(ipath):
        return f"Error: Input video not found: {ipath}"

    os.makedirs(os.path.dirname(os.path.abspath(opath)), exist_ok=True)
    if mode == "blur_background":
        vf = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=lr=30:cr=30[bg];"
            "[0:v]scale=1080:-1[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2[out]"
        )
        cmd = [
            FFMPEG_EXE, "-y", "-i", ipath,
            "-filter_complex", vf, "-map", "[out]", "-map", "0:a?",
            "-c:v", "libx264", "-c:a", "aac",
            opath
        ]
    else:
        vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        cmd = [
            FFMPEG_EXE, "-y", "-i", ipath,
            "-vf", vf,
            "-c:v", "libx264", "-c:a", "copy",
            opath
        ]
    run_ffmpeg(cmd)
    return f"Video reframed to 1080x1920 vertical: {opath}"


def handle_trim_video(args):
    ipath = args["input_path"]
    opath = args["output_path"]
    s = args["start_sec"]
    e = args["end_sec"]
    dur = e - s

    cmd = [
        FFMPEG_EXE, "-y", "-ss", str(s), "-i", ipath,
        "-t", str(dur),
        "-c:v", "libx264", "-c:a", "aac",
        opath
    ]
    run_ffmpeg(cmd)
    return f"Trimmed clip from {s}s to {e}s: {opath}"


def handle_concat_videos(args):
    paths = args["video_paths"]
    opath = args["output_path"]
    temp_list = opath + ".txt"

    with open(temp_list, "w") as f:
        for p in paths:
            f.write(f"file '{os.path.abspath(p)}'\n")

    cmd = [
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0", "-i", temp_list,
        "-c", "copy",
        opath
    ]
    try:
        run_ffmpeg(cmd)
    except Exception:
        # Fallback to re-encode if codecs mismatch
        cmd = [
            FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0", "-i", temp_list,
            "-c:v", "libx264", "-c:a", "aac",
            opath
        ]
        run_ffmpeg(cmd)
    finally:
        if os.path.exists(temp_list):
            os.remove(temp_list)

    return f"Videos concatenated: {opath}"


def handle_mix_audio_ducking(args):
    vpath = args["voice_path"]
    mpath = args["music_path"]
    opath = args["output_path"]
    vol = args.get("music_volume", 0.20)

    cmd = [
        FFMPEG_EXE, "-y", "-i", vpath, "-i", mpath,
        "-filter_complex", f"[1:a]volume={vol}[bgm];[0:a][bgm]amix=inputs=2:duration=first[out]",
        "-map", "[out]",
        opath
    ]
    run_ffmpeg(cmd)
    return f"Audio ducked and mixed: {opath}"


def handle_create_ken_burns_clip(args):
    ipath = args["image_path"]
    opath = args["output_path"]
    dur = args.get("duration_sec", 5.0)
    direction = args.get("direction", "zoom_in")
    frames = int(dur * 30)

    if direction == "zoom_in":
        zf = f"zoompan=z='min(zoom+0.0015,1.25)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
    else:
        zf = f"zoompan=z='if(lte(zoom,1.0),1.25,max(1.001,zoom-0.0015))':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"

    cmd = [
        FFMPEG_EXE, "-y", "-loop", "1", "-i", ipath,
        "-vf", zf,
        "-t", str(dur),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        opath
    ]
    run_ffmpeg(cmd)
    return f"Ken Burns clip created: {opath}"


def handle_extract_frames(args):
    vpath = args["video_path"]
    opath = args["output_image_path"]
    ts = args.get("timestamp_sec", 0.0)

    cmd = [
        FFMPEG_EXE, "-y", "-ss", str(ts), "-i", vpath,
        "-vframes", "1",
        opath
    ]
    run_ffmpeg(cmd)
    return f"Frame extracted at {ts}s: {opath}"


def handle_inspect_media_file(args):
    path = args.get("file_path", "")
    if not os.path.exists(path):
        return f"File does not exist: {path}"

    cmd = [FFMPEG_EXE, "-i", path]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    lines = [line for line in res.stdout.splitlines() if any(k in line for k in ["Duration:", "Stream #", "bitrate:"])]
    return f"Media Inspection for {path}:\n" + "\n".join(lines)


def handle_upload_to_youtube(args):
    try:
        from connectors.youtube_connector import upload_youtube_short
        vpath = args["video_path"]
        title = args["title"]
        desc = args.get("description", "")
        tags = args.get("tags")
        privacy = args.get("privacy_status", "private")
        res = upload_youtube_short(vpath, title, description=desc, tags=tags, privacy_status=privacy)
        return (
            f"✅ Video Uploaded Successfully to YouTube!\n"
            f"Video ID: {res['video_id']}\n"
            f"Short URL: {res['video_url']}\n"
            f"Status: {res['privacy'].upper()}"
        )
    except Exception as e:
        return f"YouTube upload error: {str(e)}"


def handle_get_youtube_channel_stats(args):
    try:
        from connectors.youtube_connector import get_channel_info
        info = get_channel_info()
        if "error" in info:
            return f"Error: {info['error']}"
        return (
            f"YouTube Channel Connected:\n"
            f"Title: {info.get('title')}\n"
            f"Custom URL: {info.get('custom_url')}\n"
            f"Subscribers: {info.get('subscribers')}\n"
            f"Total Views: {info.get('total_views')}\n"
            f"Total Videos: {info.get('video_count')}"
        )
    except Exception as e:
        return f"YouTube connection notice: {str(e)}"


def run_server():
    """Main JSON-RPC stdio protocol loop."""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "video-studio-mcp",
                            "version": "2.0.0"
                        }
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            elif method == "notifications/initialized":
                pass

            elif method == "ping":
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": get_tool_definitions()
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})

                dispatch = {
                    "generate_faceless_short": handle_generate_faceless_short,
                    "search_open_stock_videos": handle_search_open_stock_videos,
                    "synthesize_speech": handle_synthesize_speech,
                    "burn_subtitles": handle_burn_subtitles,
                    "reframe_to_vertical": handle_reframe_to_vertical,
                    "trim_video": handle_trim_video,
                    "concat_videos": handle_concat_videos,
                    "mix_audio_ducking": handle_mix_audio_ducking,
                    "create_ken_burns_clip": handle_create_ken_burns_clip,
                    "extract_frames": handle_extract_frames,
                    "inspect_media_file": handle_inspect_media_file,
                    "upload_to_youtube": handle_upload_to_youtube,
                    "get_youtube_channel_stats": handle_get_youtube_channel_stats,
                }

                if name in dispatch:
                    try:
                        text = dispatch[name](args)
                    except Exception as ex:
                        text = f"Tool execution failed: {str(ex)}"
                else:
                    text = f"Unknown tool: {name}"

                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": text}]
                    }
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            else:
                if req_id is not None:
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32601, "message": f"Method not found: {method}"}
                    }
                    sys.stdout.write(json.dumps(resp) + "\n")
                    sys.stdout.flush()

        except Exception as e:
            if req_id is not None:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                }
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    run_server()
