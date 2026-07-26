import subprocess
import os
import glob


def run_ffmpeg(command):
    print("Running FFmpeg...", flush=True)

    subprocess.run(
        command,
        check=True,
        timeout=180
    )


def merge_video(output="final.mp4"):

    if not os.path.exists("voice.mp3"):
        raise Exception("voice.mp3 not found")

    clips = sorted(glob.glob("clips/*.mp4"))

    if not clips:
        raise Exception("No clips found")

    print(f"Found {len(clips)} clips", flush=True)

    # ---------------------------------
    # STEP 1: Normalize every clip
    # ---------------------------------

    os.makedirs("normalized", exist_ok=True)

    for f in os.listdir("normalized"):
        path = os.path.join("normalized", f)
        if os.path.isfile(path):
            os.remove(path)

    normalized = []

    for i, clip in enumerate(clips, start=1):

        out = f"normalized/clip{i}.mp4"

        print(f"Normalizing clip {i}: {clip}", flush=True)

        run_ffmpeg([
            "ffmpeg",
            "-y",
            "-i", clip,

            "-an",

            "-vf",
            (
                "scale=720:1280:"
                "force_original_aspect_ratio=increase,"
                "crop=720:1280,"
                "fps=30,"
                "format=yuv420p"
            ),

            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "28",

            "-r", "30",
            "-pix_fmt", "yuv420p",

            "-movflags", "+faststart",

            out
        ])

        normalized.append(out)

    # ---------------------------------
    # STEP 2: Create concat list
    # ---------------------------------

    with open("clips.txt", "w", encoding="utf-8") as f:

        for clip in normalized:
            absolute_path = os.path.abspath(clip).replace("\\", "/")
            f.write(f"file '{absolute_path}'\n")

    print("Normalized clips ready.", flush=True)

    # ---------------------------------
    # STEP 3: Merge normalized clips
    # ---------------------------------

    if os.path.exists("merged.mp4"):
        os.remove("merged.mp4")

    print("Merging normalized clips...", flush=True)

    run_ffmpeg([
        "ffmpeg",
        "-y",

        "-f", "concat",
        "-safe", "0",

        "-i", "clips.txt",

        "-c", "copy",

        "-movflags", "+faststart",

        "merged.mp4"
    ])

    # ---------------------------------
    # STEP 4: Add AI voice
    # ---------------------------------

    if os.path.exists(output):
        os.remove(output)

    print("Adding AI voice...", flush=True)

    run_ffmpeg([
        "ffmpeg",
        "-y",

        "-i", "merged.mp4",
        "-i", "voice.mp3",

        "-map", "0:v:0",
        "-map", "1:a:0",

        "-c:v", "copy",

        "-c:a", "aac",
        "-b:a", "128k",

        "-shortest",

        "-movflags", "+faststart",

        output
    ])

    # ---------------------------------
    # STEP 5: Verify
    # ---------------------------------

    if not os.path.exists(output):
        raise Exception("final.mp4 was not created")

    size = os.path.getsize(output)

    print(
        f"✅ Professional Video Created: "
        f"{size / (1024 * 1024):.2f} MB",
        flush=True
    )