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
            "per_page": 10,
            "orientation": "portrait"
        }
    )

    data = r.json()

    if "videos" not in data or len(data["videos"]) == 0:
        raise Exception("No videos found")

    video = random.choice(data["videos"])

    # 720p/1080p choose karo (4K avoid)
    selected = None

    for f in video["video_files"]:

        width = f.get("width", 0)

        if 720 <= width <= 1080:
            selected = f
            break

    # Agar na mile to sabse chhoti file le lo
    if selected is None:
        selected = min(
            video["video_files"],
            key=lambda x: x.get("width", 99999)
        )

    url = selected["link"]

    print("Downloading:", url)

    v = requests.get(url)

    with open("video.mp4", "wb") as f:
        f.write(v.content)

    print("✅ HD Video Downloaded")