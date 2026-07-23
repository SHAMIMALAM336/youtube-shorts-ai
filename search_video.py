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
            "per_page": 5,
            "orientation": "portrait"
        }
    )

    data = response.json()

    if not data.get("videos"):
        return None

    # First video
    video = data["videos"][0]

    # Choose a smaller file (720p–1080p)
    selected = None

    for f in video["video_files"]:
        height = f.get("height", 9999)

        if height <= 1280:
            selected = f
            break

    if selected is None:
        selected = video["video_files"][-1]

    video_url = selected["link"]

    print("Downloading:", video_url)

    r = requests.get(video_url, stream=True)

    with open("video.mp4", "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)

    print("✅ video.mp4 downloaded")

    return "video.mp4"