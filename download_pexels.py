import requests
import os
import re

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

SEARCH_KEYWORDS = [
    "artificial intelligence",
    "ai technology",
    "robot",
    "computer",
    "software",
    "coding",
    "technology",
    "startup",
    "business",
    "future"
]

STOP_WORDS = {
    "this","that","with","have","will","they","them","their","from",
    "into","your","about","after","before","there","would","could",
    "should","just","than","then","what","when","where","which",
    "because","while","every","today","yesterday","tomorrow","video",
    "shorts","follow","subscribe","comment","share","watch"
}


def clean_keywords(script):

    words = re.findall(r"[A-Za-z]+", script.lower())

    keywords = []

    for word in words:

        if len(word) < 4:
            continue

        if word in STOP_WORDS:
            continue

        if word not in keywords:
            keywords.append(word)

    keywords.extend(SEARCH_KEYWORDS)

    unique = []

    for k in keywords:
        if k not in unique:
            unique.append(k)

    return unique[:8]


def best_video(video):

    files = sorted(
        video["video_files"],
        key=lambda x: x.get("width", 0),
        reverse=True
    )

    for f in files:

        w = f.get("width", 0)

        if 720 <= w <= 1080:
            return f["link"]

    return files[0]["link"]


def download_pexels(script):

    os.makedirs("clips", exist_ok=True)

    for f in os.listdir("clips"):
        os.remove(os.path.join("clips", f))

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    keywords = clean_keywords(script)

    print("=" * 40)
    print("SEARCH KEYWORDS")
    print("=" * 40)

    for k in keywords:
        print(k)

    clip = 1

    downloaded = set()

    for keyword in keywords:

        try:

            print(f"\nSearching: {keyword}")

            r = requests.get(
                "https://api.pexels.com/videos/search",
                headers=headers,
                params={
                    "query": keyword,
                    "per_page": 8,
                    "orientation": "portrait",
                    "size": "medium"
                },
                timeout=20
            )

            data = r.json()

            if "videos" not in data:
                continue

            if len(data["videos"]) == 0:
                continue

            videos = sorted(
                data["videos"],
                key=lambda v: v.get("duration", 999)
            )

            selected = None

            for video in videos:

                url = best_video(video)

                if url not in downloaded:
                    downloaded.add(url)
                    selected = url
                    break

            if selected is None:
                continue

            print("Downloading clip...")

            video = requests.get(
                selected,
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

    print("=" * 40)
    print(f"Downloaded {clip-1} clips")
    print("=" * 40)