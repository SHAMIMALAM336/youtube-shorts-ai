import subprocess
import os
import glob
import json


def run(cmd):
    subprocess.run(cmd, check=True)


def get_audio_duration(audio):
    result = subprocess.check_output([
        "ffprobe",
        "-v","error",
        "-show_entries","format=duration",
        "-of","json",
        audio
    ])

    data=json.loads(result)

    return float(data["format"]["duration"])


def get_video_duration(video):
    result=subprocess.check_output([
        "ffprobe",
        "-v","error",
        "-show_entries","format=duration",
        "-of","json",
        video
    ])

    data=json.loads(result)

    return float(data["format"]["duration"])


def merge_video():

    if not os.path.exists("voice.mp3"):
        raise Exception("voice.mp3 missing")

    audio_length=get_audio_duration("voice.mp3")

    clips=sorted(glob.glob("clips/*.mp4"))

    if len(clips)==0:
        raise Exception("No clips downloaded")

    os.makedirs("normalized",exist_ok=True)

    for f in glob.glob("normalized/*.mp4"):
        os.remove(f)

    normalized=[]

    current=0

    index=1

    while current<audio_length:

        clip=clips[(index-1)%len(clips)]

        out=f"normalized/clip{index}.mp4"

        run([
            "ffmpeg",
            "-y",
            "-i",clip,
            "-an",
            "-vf","scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=30",
            "-pix_fmt","yuv420p",
            "-c:v","libx264",
            out
        ])

        normalized.append(out)

        current+=get_video_duration(out)

        index+=1


    with open("clips.txt","w") as f:
        for c in normalized:
            f.write(f"file '{os.path.abspath(c)}'\n")


    run([
        "ffmpeg",
        "-y",
        "-f","concat",
        "-safe","0",
        "-i","clips.txt",
        "-c","copy",
        "merged.mp4"
    ])


    run([
        "ffmpeg",
        "-y",
        "-i","merged.mp4",
        "-i","voice.mp3",
        "-map","0:v",
        "-map","1:a",
        "-shortest",
        "-c:v","copy",
        "-c:a","aac",
        "final.mp4"
    ])

    print("Final video created")