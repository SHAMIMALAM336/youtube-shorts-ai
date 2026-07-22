import subprocess
import os


def merge_video(
    video="video.mp4",
    audio="voice.mp3",
    output="final.mp4"
):

    if not os.path.exists(video):
        raise Exception("video.mp4 not found")

    if not os.path.exists(audio):
        raise Exception("voice.mp3 not found")

    command = [
        "ffmpeg",
        "-y",

        "-stream_loop", "-1",
        "-i", video,

        "-i", audio,

        "-vf",
        (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            "eq=contrast=1.08:brightness=0.03:saturation=1.15"
        ),

        "-map", "0:v:0",
        "-map", "1:a:0",

        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",

        "-c:a", "aac",
        "-b:a", "192k",

        "-shortest",

        output
    ]

    subprocess.run(command, check=True)

    print("✅ Professional Video Created")