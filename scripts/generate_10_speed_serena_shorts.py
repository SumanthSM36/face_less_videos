#!/usr/bin/env python3
"""
generate_10_speed_serena_shorts.py — Batch Generator for 10 Viral YouTube Shorts
from IShowSpeed x Serena Williams ("Can I Return a 120 MPH Serve From Serena Williams?")
Source URL: https://youtu.be/jJ-zWCw85qA
Local Master: /tmp/serena_full.mp4
Subtitles: /tmp/speed_serena_subtitles.srt
"""

import os
import sys
import json
import logging
import subprocess

from agentic_pipeline.models.ffmpeg_utils import get_ffmpeg_path
from agentic_pipeline.clipper.smart_reframer import SmartReframer
from agentic_pipeline.clipper.caption_burner import ClipperCaptionBurner

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("SpeedSerena10Clips")

CLIPS_CONFIG = [
    {
        "id": "short_01_never_played_tennis",
        "start_time": "00:01:45",
        "duration": 32.0,
        "hook_header": "I NEVER PLAYED TENNIS IN MY LIFE!",
        "title": "I NEVER PLAYED TENNIS IN MY LIFE! 😱 #shorts",
        "description": "Speed admits to coach Jamir Jenkins that he has NEVER held a tennis racket before attempting to play Serena Williams!\n\n#shorts #ishowspeed #serenawilliams #tennis #funny #viral",
        "tags": ["shorts", "ishowspeed", "serena williams", "speed tennis", "funny", "viral", "highlights"]
    },
    {
        "id": "short_02_boxing_gym_training",
        "start_time": "00:12:30",
        "duration": 38.0,
        "hook_header": "SPEED BROUGHT TO BOXING GYM FOR TENNIS?!",
        "title": "SPEED BROUGHT TO BOXING GYM FOR TENNIS?! 🥊 #shorts",
        "description": "Speed's coach sends him to a secret training location... only to find out it's an elite boxing gym to prepare for Serena Williams!\n\n#shorts #ishowspeed #serenawilliams #boxing #tennis #funny",
        "tags": ["shorts", "ishowspeed", "serena williams", "boxing", "training", "viral", "funny"]
    },
    {
        "id": "short_03_kinetic_chain_secrets",
        "start_time": "00:14:00",
        "duration": 38.0,
        "hook_header": "BOXING SECRETS TO BEAT SERENA WILLIAMS",
        "title": "BOXING SECRETS TO BEAT SERENA WILLIAMS 🥊 #shorts",
        "description": "Trainers teach Speed how boxing footwork and the kinetic chain directly power a tennis forehand against Serena!\n\n#shorts #ishowspeed #serenawilliams #boxing #tennis #training",
        "tags": ["shorts", "ishowspeed", "serena williams", "kinetic chain", "tennis tutorial", "viral"]
    },
    {
        "id": "short_04_speed_meets_serena",
        "start_time": "00:16:22",
        "duration": 36.0,
        "hook_header": "SPEED MEETS SERENA WILLIAMS!",
        "title": "SPEED MEETS SERENA WILLIAMS FOR FIRST TIME! 😱 #shorts",
        "description": "The 23-time Grand Slam legend Serena Williams meets IShowSpeed on the court: 'Well, well, well, I heard you've been training!'\n\n#shorts #ishowspeed #serenawilliams #speedmeets #tennis #viral",
        "tags": ["shorts", "ishowspeed", "serena williams", "speed meets serena", "tennis", "legend"]
    },
    {
        "id": "short_05_serena_roasts_smash",
        "start_time": "00:17:36",
        "duration": 36.0,
        "hook_header": "SERENA ROASTS SPEED'S SMASH!",
        "title": "SERENA LAUGHS AT SPEED'S OVERHEAD SMASH! 💀 #shorts",
        "description": "Serena Williams can't hold back her laughter after watching Speed's jump smash: 'It's like my kid jumping on a basketball court!'\n\n#shorts #ishowspeed #serenawilliams #roast #funny #tennis",
        "tags": ["shorts", "ishowspeed", "serena williams", "roast", "overhead smash", "funny moments"]
    },
    {
        "id": "short_06_speed_hits_76mph",
        "start_time": "00:20:00",
        "duration": 44.0,
        "hook_header": "SPEED HITS A 76 MPH SERVE!",
        "title": "SPEED MAXES SERVE AT 76 MPH! ⚡ #shorts",
        "description": "Speed pumps up his serve from 54 mph to an explosive 76 mph and goes completely wild in front of Serena!\n\n#shorts #ishowspeed #serenawilliams #tennis #serve #celebration #viral",
        "tags": ["shorts", "ishowspeed", "serena williams", "76 mph serve", "tennis serve", "lets go"]
    },
    {
        "id": "short_07_serena_108mph_humble",
        "start_time": "00:20:48",
        "duration": 36.0,
        "hook_header": "SERENA HUMBLES SPEED (108 MPH SERVE)",
        "title": "SERENA HUMBLES SPEED WITH 108 MPH SERVE! 💀 #shorts",
        "description": "Right after Speed celebrates his 76 mph serve, Serena steps up cold and casually drops a 108 mph bomb to instantly humble him!\n\n#shorts #ishowspeed #serenawilliams #ace #tennis #humbled #funny",
        "tags": ["shorts", "ishowspeed", "serena williams", "108 mph", "tennis ace", "humbled"]
    },
    {
        "id": "short_08_cones_accuracy_disaster",
        "start_time": "00:21:28",
        "duration": 46.0,
        "hook_header": "CAN SPEED HIT A CONE IN 45 SECONDS?!",
        "title": "CAN SPEED HIT A CONE IN 45 SECONDS?! 😭 #shorts",
        "description": "Speed gets 45 seconds to knock over tennis cones... and hits exactly ZERO balls on target!\n\n#shorts #ishowspeed #serenawilliams #tennis #accuracy #funny #epicfail",
        "tags": ["shorts", "ishowspeed", "serena williams", "tennis cones", "funny fail", "viral"]
    },
    {
        "id": "short_09_speed_returns_serve",
        "start_time": "00:25:18",
        "duration": 42.0,
        "hook_header": "SPEED ACTUALLY RETURNS SERENA'S SERVE!",
        "title": "SPEED ACTUALLY RETURNS SERENA'S SERVE! 😱 #shorts",
        "description": "Against all odds, Speed connects and returns a Serena Williams serve using his boxing kinetic training!\n\n#shorts #ishowspeed #serenawilliams #tennis #miracle #insane #viral",
        "tags": ["shorts", "ishowspeed", "serena williams", "serve return", "miracle", "epic moment"]
    },
    {
        "id": "short_10_serena_brutal_truth",
        "start_time": "00:29:12",
        "duration": 38.0,
        "hook_header": "SERENA TELLS SPEED THE BRUTAL TRUTH!",
        "title": "SERENA TELLS SPEED THE BRUTAL TRUTH! 💀 #shorts",
        "description": "Speed asks Serena Williams: 'Do I have what it takes to go pro?' Her instant answer leaves him speechless!\n\n#shorts #ishowspeed #serenawilliams #tennis #truth #funny #gopro",
        "tags": ["shorts", "ishowspeed", "serena williams", "go pro", "brutal honesty", "funny"]
    }
]


def slice_local_video(ffmpeg: str, input_file: str, start_time: str, duration: float, output_file: str) -> str:
    cmd = [
        ffmpeg, "-y",
        "-ss", start_time,
        "-i", input_file,
        "-t", str(duration),
        "-c", "copy",
        output_file
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_file


def extract_thumbnail(ffmpeg: str, video_path: str, thumb_path: str):
    cmd = [
        ffmpeg, "-y",
        "-ss", "00:00:01",
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        thumb_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_video = "/tmp/serena_full.mp4"
    srt_path = "/tmp/speed_serena_subtitles.srt"
    output_base = os.path.join(root_dir, "output", "speed_serena_10_shorts")
    os.makedirs(output_base, exist_ok=True)

    if not os.path.exists(source_video):
        logger.error(f"Source video not found: {source_video}")
        sys.exit(1)

    ffmpeg = get_ffmpeg_path()
    logger.info(f"🚀 [SpeedSerena10Clips] Initializing batch production for 10 Shorts...")
    logger.info(f"Source: {source_video} | SRT: {srt_path}")

    results = []

    for idx, clip in enumerate(CLIPS_CONFIG, start=1):
        clip_id = clip["id"]
        clip_dir = os.path.join(output_base, clip_id)
        os.makedirs(clip_dir, exist_ok=True)

        logger.info(f"\n==========================================")
        logger.info(f"🎬 Producing Short {idx}/10: {clip['title']}")
        logger.info(f"   Timestamp: {clip['start_time']} | Duration: {clip['duration']}s")
        logger.info(f"==========================================")

        raw_slice = os.path.join(clip_dir, "raw_slice.mp4")
        slice_local_video(ffmpeg, source_video, clip["start_time"], clip["duration"], raw_slice)

        reframer = SmartReframer(clip_dir)
        reframed_mp4 = os.path.join(clip_dir, "reframed_vertical_916.mp4")
        reframer.reframe_to_vertical(
            input_media=raw_slice,
            output_mp4=reframed_mp4,
            start_time="00:00:00",
            duration=clip["duration"],
            preset="dynamic_angles"
        )

        captioner = ClipperCaptionBurner(clip_dir)
        final_mp4 = os.path.join(clip_dir, "final_clipped_short.mp4")
        captioner.burn_subtitles_onto_clip(
            video_path=reframed_mp4,
            srt_path=srt_path,
            start_time_ts=clip["start_time"],
            clip_duration=clip["duration"],
            output_mp4=final_mp4,
            preset="hormozi_pop",
            header_title=clip["hook_header"]
        )

        thumb_path = os.path.join(clip_dir, "final_clipped_short_thumb.jpg")
        extract_thumbnail(ffmpeg, final_mp4, thumb_path)

        meta = {
            "index": idx,
            "id": clip_id,
            "title": clip["title"],
            "hook_header": clip["hook_header"],
            "start_time": clip["start_time"],
            "duration": clip["duration"],
            "video_path": final_mp4,
            "thumbnail_path": thumb_path,
            "description": clip["description"],
            "tags": clip["tags"]
        }
        with open(os.path.join(clip_dir, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        results.append(meta)
        logger.info(f"✅ Finished Short #{idx}: {final_mp4}")

    report_path = os.path.join(output_base, "speed_serena_master_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    logger.info(f"\n🎉 ALL 10 SHORTS SUCCESSFULLY GENERATED! Report -> {report_path}")


if __name__ == "__main__":
    main()
