import requests
import os
import random

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


def download_pexels(query):

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    r = requests.get(
        "https://api.pexels.com/videos/search",
        headers=headers,
        params={
            "query": query,
            "per_page": 15,
            "orientation": "portrait"
        }
    )

    data = r.json()

    if len(data["videos"]) == 0:
        raise Exception("No videos found")

    video = random.choice(data["videos"])

    files = sorted(
        video["video_files"],
        key=lambda x: x["width"],
        reverse=True
    )

    url = files[0]["link"]

    print("Downloading:", url)

    v = requests.get(url)

    with open("video.mp4", "wb") as f:
        f.write(v.content)

    print("✅ HD Video Downloaded")