#!/usr/bin/env python3
"""
run_agent_pipeline.py — Master CLI Entrypoint for the Agentic Video Studio.
Dispatches user prompts to Agent Manager, routes through Directors and Subagents,
enforces Audience Review, and protects execution via Agent Healer.
"""

import os
import sys
import argparse
import json

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, WORKSPACE_ROOT)

from scripts.agentic_pipeline.agent_manager import AgentManager


def main():
    parser = argparse.ArgumentParser(description="Autonomous Video Studio Agentic Pipeline")
    parser.add_argument("prompt", type=str, help="User request/instruction (e.g., 'create short video on Shabari devotion')")
    parser.add_argument("--duration", type=float, default=45.0, help="Target video duration in seconds")
    parser.add_argument("--url", type=str, default=None, help="Source URL for video clipping")
    parser.add_argument("--file", type=str, default=None, help="Source file for video clipping")
    parser.add_argument("--start", type=str, default="00:00:10", help="Clipping start timestamp (e.g. 00:00:15)")
    parser.add_argument("--caption-style", type=str, default="hormozi_pop", choices=["hormozi_pop", "beast_neon", "pixar_gold", "cyber_cyan"], help="Kinetic typography style preset")
    parser.add_argument("--reframe", type=str, default="blurred_backdrop", choices=["blurred_backdrop", "split_screen", "crop_center"], help="Vertical 9:16 reframe preset")

    args = parser.parse_args()

    print("=" * 70)
    print("🤖 AUTONOMOUS VIDEO STUDIO — AGENTIC PIPELINE")
    print("=" * 70)

    manager = AgentManager(workspace_root=WORKSPACE_ROOT)
    params = {
        "duration": args.duration,
        "source_url": args.url,
        "source_file": args.file,
        "start_time": args.start,
        "caption_preset": args.caption_style,
        "reframe_preset": args.reframe
    }

    try:
        summary = manager.process_user_request(args.prompt, params)
        print("\n" + "=" * 70)
        print("🎯 PRODUCTION COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print(json.dumps(summary, indent=2))
    except Exception as e:
        print(f"\n❌ Pipeline failed with unrecoverable error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
