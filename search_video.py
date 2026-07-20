import os
import requests

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def search_video(query):

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    response = requests.get(
        "https://api.pexels.com/videos/search",
        headers=headers,
        params={
            "query": query,
            "per_page": 1,
            "orientation": "portrait"
        }
    )

    data = response.json()

    if len(data["videos"]) == 0:
        return None

    video_url = data["videos"][0]["video_files"][0]["link"]

    print("Downloading:", video_url)

    video = requests.get(video_url)

    with open("video.mp4", "wb") as f:
        f.write(video.content)

    print("✅ video.mp4 downloaded")

    return "video.mp4"