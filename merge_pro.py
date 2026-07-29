import subprocess
import os
import glob
import json
import random
import math


# ==========================================
# RUN FFMPEG
# ==========================================

def run(cmd):

    print(" ".join(cmd), flush=True)

    subprocess.run(
        cmd,
        check=True
    )


# ==========================================
# GET MEDIA DURATION
# ==========================================

def get_duration(file):

    result = subprocess.check_output([

        "ffprobe",

        "-v",
        "error",

        "-show_entries",
        "format=duration",

        "-of",
        "json",

        file

    ])

    data = json.loads(result)

    return float(data["format"]["duration"])


# ==========================================
# AUDIO DURATION
# ==========================================

def get_audio_duration():

    if not os.path.exists("voice.mp3"):

        raise Exception("voice.mp3 missing")

    return get_duration("voice.mp3")


# ==========================================
# VIDEO DURATION
# ==========================================

def get_video_duration(video):

    return get_duration(video)


# ==========================================
# CLEAN DIRECTORY
# ==========================================

def clean_folder(folder):

    os.makedirs(folder, exist_ok=True)

    for f in glob.glob(os.path.join(folder, "*")):

        if os.path.isfile(f):

            os.remove(f)


# ==========================================
# RANDOM START POSITION
# ==========================================

def random_start(video, target):

    duration = get_video_duration(video)

    if duration <= target:

        return 0

    return round(

        random.uniform(

            0,

            duration - target

        ),

        2

    )


# ==========================================
# NORMALIZE CLIP
# ==========================================

def normalize_clip(

        input_clip,

        output_clip,

        target_duration

):

    start = random_start(

        input_clip,

        target_duration

    )

    run([

        "ffmpeg",

        "-y",

        "-ss",

        str(start),

        "-i",

        input_clip,

        "-t",

        str(target_duration),

        "-an",

        "-vf",

        (
            "scale=720:1280:"
            "force_original_aspect_ratio=increase,"
            "crop=720:1280,"
            "fps=30"
        ),

        "-pix_fmt",

        "yuv420p",

        "-c:v",

        "libx264",

        "-preset",

        "veryfast",

        "-crf",

        "23",

        output_clip

    ])


# ==========================================
# CREATE CONCAT FILE
# ==========================================

def build_concat_file(clips):

    with open(

        "clips.txt",

        "w",

        encoding="utf-8"

    ) as f:

        for clip in clips:

            path = os.path.abspath(

                clip

            ).replace(

                "\\",

                "/"

            )

            f.write(

                f"file '{path}'\n"

            )
            # ==========================================
# MERGE VIDEO
# ==========================================

def merge_video():

    # -----------------------------
    # CHECK VOICE
    # -----------------------------

    if not os.path.exists("voice.mp3"):
        raise Exception("voice.mp3 missing")

    audio_length = get_audio_duration()

    print("=" * 50)
    print("VOICE LENGTH :", round(audio_length, 2))
    print("=" * 50)

    # -----------------------------
    # LOAD CLIPS
    # -----------------------------

    clips = sorted(glob.glob("clips/*.mp4"))

    if len(clips) == 0:
        raise Exception("No clips found")

    print(f"Total Clips : {len(clips)}")

    # -----------------------------
    # CLEAN OUTPUT
    # -----------------------------

    clean_folder("normalized")

    normalized = []

    # -----------------------------
    # TARGET DURATION
    # -----------------------------

    target = max(2.5, audio_length / len(clips))

    print(f"Target Duration : {round(target,2)} sec")

    # -----------------------------
    # NORMALIZE EVERY CLIP
    # -----------------------------

    for i, clip in enumerate(clips, start=1):

        out = f"normalized/clip{i}.mp4"

        print("--------------------------------")
        print(f"Clip {i}")
        print(clip)

        normalize_clip(
            clip,
            out,
            target
        )

        normalized.append(out)

    # -----------------------------
    # BUILD CONCAT FILE
    # -----------------------------

    build_concat_file(normalized)

    # -----------------------------
    # MERGE ALL CLIPS
    # -----------------------------

    print("=" * 50)
    print("MERGING CLIPS")
    print("=" * 50)

    if os.path.exists("merged.mp4"):
        os.remove("merged.mp4")

    run([

        "ffmpeg",

        "-y",

        "-f",
        "concat",

        "-safe",
        "0",

        "-i",
        "clips.txt",

        "-c:v",
        "libx264",

        "-preset",
        "veryfast",

        "-crf",
        "23",

        "-pix_fmt",
        "yuv420p",

        "merged.mp4"

    ])
        # -----------------------------
    # ADD AI VOICE
    # -----------------------------

    print("=" * 50)
    print("ADDING VOICE")
    print("=" * 50)

    if os.path.exists("final.mp4"):
        os.remove("final.mp4")

    run([

        "ffmpeg",

        "-y",

        "-i",
        "merged.mp4",

        "-i",
        "voice.mp3",

        "-map",
        "0:v:0",

        "-map",
        "1:a:0",

        "-c:v",
        "copy",

        "-c:a",
        "aac",

        "-b:a",
        "192k",

        "-shortest",

        "-movflags",
        "+faststart",

        "final.mp4"

    ])

    # -----------------------------
    # VERIFY
    # -----------------------------

    if not os.path.exists("final.mp4"):
        raise Exception("final.mp4 not created")

    size = os.path.getsize("final.mp4")

    if size < 100000:
        raise Exception("Video too small")

    print("=" * 50)
    print("VIDEO CREATED SUCCESSFULLY")
    print("=" * 50)
    print(f"Audio Length : {round(audio_length,2)} sec")
    print(f"Output Size  : {round(size/(1024*1024),2)} MB")
    print("=" * 50)