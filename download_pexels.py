import requests
import os
import re

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

SEARCH_KEYWORDS = [
    "artificial intelligence",
    "technology",
    "computer",
    "coding",
    "robot"
]


def clean_keywords(title):

    words = re.findall(r"[A-Za-z]+", title.lower())

    keywords = []

    for w in words:
        if len(w) > 3:
            keywords.append(w)

    keywords.extend(SEARCH_KEYWORDS)

    seen = []

    for k in keywords:
        if k not in seen:
            seen.append(k)

    return seen[:3]


def best_video(video):

    for f in video["video_files"]:

        w = f.get("width", 0)

        if 720 <= w <= 1080:
            return f["link"]

    return min(
        video["video_files"],
        key=lambda x: x.get("width", 99999)
    )["link"]


def download_pexels(title):

    os.makedirs("clips", exist_ok=True)

    for f in os.listdir("clips"):
        os.remove(os.path.join("clips", f))

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    keywords = clean_keywords(title)

    clip = 1

    for keyword in keywords:

        try:

            print(f"Searching: {keyword}")

            r = requests.get(
                "https://api.pexels.com/videos/search",
                headers=headers,
                params={
                    "query": keyword,
                    "per_page": 3,
                    "orientation": "portrait"
                },
                timeout=20
            )

            data = r.json()

            if "videos" not in data:
                continue

            if len(data["videos"]) == 0:
                continue

            url = best_video(data["videos"][0])

            print("Downloading clip...")

            video = requests.get(
                url,
                timeout=60
            )

            with open(f"clips/clip{clip}.mp4", "wb") as f:
                f.write(video.content)

            print(f"Downloaded clip{clip}")

            clip += 1

        except Exception as e:

            print("Skipped:", keyword)
            print(str(e))

    if clip == 1:
        raise Exception("No clips downloaded")

    print("All clips downloaded.")