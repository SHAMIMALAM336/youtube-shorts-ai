import requests
import os
import re
import random

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# ==========================================
# AI VISUAL MAPPING
# ==========================================

AI_MAP = {

    "google": [
        "google office",
        "google technology",
        "software developer"
    ],

    "gemini": [
        "artificial intelligence",
        "ai technology",
        "robot"
    ],

    "openai": [
        "artificial intelligence",
        "computer",
        "server room"
    ],

    "chatgpt": [
        "artificial intelligence",
        "typing computer",
        "office computer"
    ],

    "nvidia": [
        "gpu",
        "data center",
        "computer server"
    ],

    "tesla": [
        "electric car",
        "factory",
        "automation"
    ],

    "robot": [
        "robot",
        "artificial intelligence"
    ],

    "coding": [
        "software developer",
        "programming",
        "computer"
    ],

    "developer": [
        "software developer",
        "coding"
    ],

    "cloud": [
        "cloud computing",
        "data center"
    ],

    "server": [
        "data center",
        "server room"
    ],

    "startup": [
        "startup office",
        "business meeting"
    ],

    "business": [
        "office work",
        "business team"
    ],

    "future": [
        "future technology",
        "innovation"
    ]
}

# ==========================================
# FALLBACK SEARCHES
# ==========================================

DEFAULT_SEARCHES = [

    "artificial intelligence",

    "technology",

    "software developer",

    "computer",

    "robot",

    "data center",

    "coding",

    "future technology"
]

STOP_WORDS = {

    "this","that","with","have","will","they","them",
    "their","from","into","your","about","after",
    "before","there","would","could","should","just",
    "than","then","what","when","where","which",
    "because","while","every","today","tomorrow",
    "video","shorts","follow","subscribe","comment",
    "share","watch","works","launched","launch",
    "using","daily","background","manage","life",
    "hours","called","built","running","instead",
    "takes","toward","below"

}

# ==========================================
# CREATE SEARCH LIST
# ==========================================

def clean_keywords(script):

    words = re.findall(
        r"[A-Za-z]+",
        script.lower()
    )

    searches = []

    for word in words:

        if len(word) < 4:
            continue

        if word in STOP_WORDS:
            continue

        if word in AI_MAP:

            for item in AI_MAP[word]:

                if item not in searches:
                    searches.append(item)

        else:

            if word not in searches:
                searches.append(word)

    for item in DEFAULT_SEARCHES:

        if item not in searches:
            searches.append(item)

    return searches[:15]
# ==========================================
# BEST VIDEO
# ==========================================

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


# ==========================================
# DOWNLOAD PEXELS
# ==========================================

def download_pexels(script):

    os.makedirs("clips", exist_ok=True)

    for f in os.listdir("clips"):

        os.remove(
            os.path.join("clips", f)
        )

    headers = {

        "Authorization": PEXELS_API_KEY

    }

    searches = clean_keywords(script)

    print("=" * 50)
    print("SEARCH TERMS")
    print("=" * 50)

    for s in searches:
        print("•", s)

    downloaded = set()

    clip = 1

    for keyword in searches:

        try:

            print(f"\nSearching : {keyword}")

            r = requests.get(

                "https://api.pexels.com/videos/search",

                headers=headers,

                params={

                    "query": keyword,

                    "per_page": 15,

                    "orientation": "portrait"

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

                key=lambda v: abs(
                    v.get("duration", 8) - 6
                )

            )

            selected = None

            random.shuffle(videos)

            for video in videos:

                try:

                    url = best_video(video)

                except Exception:

                    continue

                if url in downloaded:
                    continue

                downloaded.add(url)

                selected = url

                break

            if selected is None:
                continue

            print("Downloading...")

            response = requests.get(

                selected,

                timeout=60

            )

            with open(

                f"clips/clip{clip}.mp4",

                "wb"

            ) as f:

                f.write(response.content)

            print(f"Saved clip{clip}.mp4")

            clip += 1

            if clip > 8:
                break

        except Exception as e:

            print("Skipped:", keyword)

            print(e)

    if clip == 1:

        raise Exception(
            "No clips downloaded."
        )

    print("=" * 50)
    print(f"Downloaded {clip-1} clips")
    print("=" * 50)