import os
from voice import create_voice
from download_pexels import download_pexels
from merge_pro import merge_video

title = "Google Just Made AI Automation 10x Cheaper"

script = """
AI automation just got TEN TIMES cheaper!

Google just dropped Gemini Flash and it changes everything.

It is insanely fast, super smart, and costs almost nothing to run.

This could completely change how creators and small businesses use AI automation.
"""

# Clean old files
for f in [
    "voice.mp3",
    "final.mp4",
    "merged.mp4",
    "clips.txt"
]:
    if os.path.exists(f):
        os.remove(f)

# Clean old clips
os.makedirs("clips", exist_ok=True)

for file in os.listdir("clips"):
    path = os.path.join("clips", file)

    if os.path.isfile(path):
        os.remove(path)

print("=== 1. GENERATING VOICE ===", flush=True)
create_voice(script)

print("=== 2. DOWNLOADING CLIPS ===", flush=True)
download_pexels(title)

print("=== 3. CREATING FINAL VIDEO ===", flush=True)
merge_video()

if not os.path.exists("final.mp4"):
    raise Exception("final.mp4 was not created")

size = os.path.getsize("final.mp4")

print(f"=== FINAL VIDEO CREATED: {size} bytes ===", flush=True)

if size < 100000:
    raise Exception("final.mp4 appears too small/corrupt")

print("=== SUCCESS ===", flush=True)