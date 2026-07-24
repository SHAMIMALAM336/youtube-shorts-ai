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

# Delete old files
for f in ["voice.mp3", "video.mp4", "final.mp4"]:
    if os.path.exists(f):
        os.remove(f)

print("Generating voice...")
create_voice(script)

print("Downloading video...")
download_pexels(title)

print("Merging...")
merge_video()

print("Done!")