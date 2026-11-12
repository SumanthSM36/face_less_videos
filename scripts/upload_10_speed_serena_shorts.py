#!/usr/bin/env python3
"""
upload_10_speed_serena_shorts.py — Batch Uploader for 10 IShowSpeed x Serena Williams Shorts.
Reads speed_serena_master_report.json and uploads each short to YouTube.
"""

import os
import sys
import json
import logging

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(WORKSPACE_ROOT, ".agents/skills/make-faceless-short-free/scripts"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SpeedSerenaUploader")

from connectors.youtube_connector import upload_youtube_short, get_channel_info

REPORT_PATH = os.path.join(WORKSPACE_ROOT, "output/speed_serena_10_shorts/speed_serena_master_report.json")


def main():
    if not os.path.exists(REPORT_PATH):
        logger.error(f"Master report not found: {REPORT_PATH}")
        sys.exit(1)

    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        shorts_list = json.load(f)

    logger.info("=" * 70)
    logger.info("🚀 INITIATING YOUTUBE UPLOADS FOR 10 SPEED x SERENA SHORTS")
    logger.info("=" * 70)

    try:
        ch_info = get_channel_info()
        logger.info(f"Connected Channel: {ch_info.get('title')} ({ch_info.get('custom_url')})")
        logger.info(f"Current Video Count: {ch_info.get('video_count')}")
    except Exception as e:
        logger.warning(f"Could not fetch channel info: {e}")

    updated_shorts = []
    quota_exceeded = False

    for idx, short in enumerate(shorts_list, start=1):
        title = short["title"]
        video_path = short["video_path"]
        desc = short["description"]
        tags = short.get("tags", [])

        # Check if already uploaded
        if short.get("youtube", {}).get("status") == "UPLOADED":
            logger.info(f"⏭️ [{idx}/{len(shorts_list)}] Already uploaded: {short['youtube'].get('url')}")
            updated_shorts.append(short)
            continue

        if quota_exceeded:
            logger.warning(f"⚠️ Skipping Short #{idx} due to earlier upload limit.")
            short["youtube"] = {"status": "SKIPPED_QUOTA_EXCEEDED"}
            updated_shorts.append(short)
            continue

        logger.info(f"\n📤 [{idx}/{len(shorts_list)}] Uploading to YouTube: '{title}'...")
        logger.info(f"   Video: {video_path}")

        try:
            res = upload_youtube_short(
                video_path=video_path,
                title=title,
                description=desc,
                tags=tags,
                privacy_status="public"
            )
            vid = res.get("video_id")
            url = res.get("video_url")
            logger.info(f"✅ Success! Published to YouTube: {url}")

            short["youtube"] = {
                "status": "UPLOADED",
                "video_id": vid,
                "url": url,
                "privacy": "public"
            }
        except Exception as e:
            err_str = str(e)
            logger.error(f"❌ Failed to upload Short #{idx}: {err_str}")
            if "uploadLimitExceeded" in err_str:
                logger.error("🚫 YouTube Daily Upload Limit reached (uploadLimitExceeded).")
                short["youtube"] = {"status": "FAILED_QUOTA_EXCEEDED", "error": err_str}
                quota_exceeded = True
            else:
                short["youtube"] = {"status": "FAILED", "error": err_str}

        updated_shorts.append(short)

        # Save progress after every upload
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(updated_shorts + shorts_list[len(updated_shorts):], f, indent=2)

    logger.info("\n=======================================================")
    logger.info(f"🏁 Finished Batch Upload. Updated report -> {REPORT_PATH}")
    logger.info("=======================================================")


if __name__ == "__main__":
    main()
