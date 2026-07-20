import os
import requests

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


def search_video(query):

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    url = "https://api.pexels.com/videos/search"

    params = {
        "query": query,
        "per_page": 1,
        "orientation": "portrait"
    }

    response = requests.get(url, headers=headers, params=params)

    data = response.json()

    if "videos" not in data or len(data["videos"]) == 0:
        print("No video found.")
        return None

    video_url = data["videos"][0]["video_files"][0]["link"]

    print("Video URL:", video_url)

    return video_url