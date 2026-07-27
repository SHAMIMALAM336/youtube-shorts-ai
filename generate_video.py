import os
import json
import urllib.request

from voice import create_voice
from download_pexels import download_pexels
from merge_pro import merge_video


# ==========================================
# GET TOPIC + SCRIPT FROM GITHUB EVENT
# ==========================================

title = os.getenv("VIDEO_TITLE")
script = os.getenv("VIDEO_SCRIPT")

if not title or not script:
    raise Exception(
        "VIDEO_TITLE or VIDEO_SCRIPT missing. "
        "GitHub Actions did not receive the new topic."
    )

print("=================================", flush=True)
print("NEW VIDEO DATA", flush=True)
print("=================================", flush=True)

print("TITLE:", title, flush=True)
print("SCRIPT:", script, flush=True)


# ==========================================
# DELETE OLD FILES
# ==========================================

for f in [
    "voice.mp3",
    "final.mp4",
    "merged.mp4",
    "clips.txt"
]:
    if os.path.exists(f):
        os.remove(f)


# ==========================================
# DELETE OLD CLIPS
# ==========================================

os.makedirs("clips", exist_ok=True)

for file in os.listdir("clips"):

    path = os.path.join("clips", file)

    if os.path.isfile(path):
        os.remove(path)


# ==========================================
# STEP 1 — VOICE
# ==========================================

print("=================================", flush=True)
print("=== 1. GENERATING VOICE ===", flush=True)
print("=================================", flush=True)

create_voice(script)


# ==========================================
# STEP 2 — PEXELS
# ==========================================

print("=================================", flush=True)
print("=== 2. DOWNLOADING CLIPS ===", flush=True)
print("=================================", flush=True)

# IMPORTANT:
# Use full script instead of only title
# This improves keyword extraction for visuals
download_pexels(script)


# ==========================================
# STEP 3 — VIDEO
# ==========================================

print("=================================", flush=True)
print("=== 3. CREATING FINAL VIDEO ===", flush=True)
print("=================================", flush=True)

merge_video()


# ==========================================
# VERIFY
# ==========================================

if not os.path.exists("final.mp4"):
    raise Exception("final.mp4 was not created")


size = os.path.getsize("final.mp4")

print(
    f"=== FINAL VIDEO CREATED: {size} bytes ===",
    flush=True
)

if size < 100000:
    raise Exception(
        "final.mp4 appears too small/corrupt"
    )

print("=================================", flush=True)
print("=== SUCCESS ===", flush=True)
print("=================================", flush=True)