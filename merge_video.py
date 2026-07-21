import subprocess
import os

def merge_video(video_file="video.mp4",
                audio_file="voice.mp3",
                output_file="final.mp4"):

    if not os.path.exists(video_file):
        raise Exception("video.mp4 not found")

    if not os.path.exists(audio_file):
        raise Exception("voice.mp3 not found")

    command = [
        "ffmpeg",
        "-y",
        "-i", video_file,
        "-i", audio_file,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_file
    ]

    subprocess.run(command, check=True)

    print("✅ final.mp4 created")