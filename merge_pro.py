import subprocess
import os

def merge_video(output="final.mp4"):

    if not os.path.exists("voice.mp3"):
        raise Exception("voice.mp3 not found")

    clips = sorted([
        os.path.join("clips", f)
        for f in os.listdir("clips")
        if f.endswith(".mp4")
    ])

    if not clips:
        raise Exception("No clips found")

    # Create concat list
    with open("clips.txt", "w", encoding="utf-8") as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")

    print("Merging clips...")

    # Re-encode while merging (more reliable than -c copy)
    subprocess.run([
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "clips.txt",

        "-vf",
        "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30",

        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",

        "-pix_fmt", "yuv420p",

        "merged.mp4"
    ], check=True)

    print("Adding voice...")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", "merged.mp4",
        "-i", "voice.mp3",

        "-c:v", "copy",

        "-c:a", "aac",
        "-b:a", "128k",

        "-shortest",

        "-movflags", "+faststart",

        output
    ], check=True)

    print("✅ Professional Video Created")