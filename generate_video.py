import os
from voice import create_voice
from download_pexels import download_pexels
from merge_pro import merge_video

title = "Google Just Made AI Automation 10x Cheaper"

script = """
AI automation just got TEN TIMES cheaper!
Google just dropped Gemini Flash and it changes everything.
It is insanely fast, super smart, and costs almost nothing to run.
"""

# ===========================
# Delete old files
# ===========================

for f in [
    "voice.mp3",
    "final.mp4",
    "merged.mp4",
    "clips.txt"
]:
    if os.path.exists(f):
        os.remove(f)

if os.path.exists("clips"):
    for file in os.listdir("clips"):
        path = os.path.join("clips", file)

        if os.path.isfile(path):
            os.remove(path)
else:
    os.makedirs("clips")

print("=================================")
print("Generating Professional Voice")
print("=================================")

create_voice(script)

print("=================================")
print("Downloading HD Clips")
print("=================================")

download_pexels(title)

print("=================================")
print("Creating Professional Video")
print("=================================")

merge_video()

print("=================================")
print("DONE")
print("=================================")