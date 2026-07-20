import requests

def download_video(url, output="demo.mp4"):
    r = requests.get(url)

    with open(output, "wb") as f:
        f.write(r.content)

    print("✅ demo.mp4 downloaded")