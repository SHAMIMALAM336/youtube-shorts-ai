from merge_pro import merge_video
import subprocess
from flask import Flask, request, jsonify, send_file
from voice import create_voice
from download_pexels import download_pexels
import os

app = Flask(__name__)


@app.route("/")
def home():
    try:
        version = subprocess.check_output(
            ["ffmpeg", "-version"]
        ).decode().split("\n")[0]

        return version

    except Exception as e:
        return str(e)


@app.route("/download/final")
def download_final():

    if os.path.exists("final.mp4"):
        return send_file(
            "final.mp4",
            mimetype="video/mp4",
            as_attachment=True,
            download_name="final.mp4"
        )

    return jsonify({
        "success": False,
        "message": "final.mp4 not found"
    }), 404


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True)

    title = data.get("title", "")
    script = data.get("script", "")

    print("===================================")
    print("Title:", title)
    print("Generating voice...")
    print("===================================")

    try:

        # Generate Voice
        create_voice(script)

        if os.path.exists("voice.mp3"):
            print("✅ voice.mp3 generated successfully")
            print("File Size:", os.path.getsize("voice.mp3"), "bytes")
        else:
            print("❌ voice.mp3 NOT generated")

        # Download HD Pexels Video
        print("===================================")
        print("Downloading Professional Pexels Video...")
        print("===================================")

        download_pexels(title)

        video = "video.mp4"

        if os.path.exists(video):
            print("✅ Video Downloaded:", video)
            print("File Size:", os.path.getsize(video), "bytes")
        else:
            raise Exception("video.mp4 not found")

        # Merge
        print("===================================")
        print("Creating Professional Video...")
        print("===================================")

        merge_video()

        if os.path.exists("final.mp4"):
            print("✅ final.mp4 generated")
            print("File Size:", os.path.getsize("final.mp4"), "bytes")
        else:
            raise Exception("final.mp4 not generated")

        return jsonify({
            "success": True,
            "title": title,
            "status": "Professional Video Ready",
            "audio_file": "voice.mp3",
            "video_file": video,
            "final_video": "final.mp4",
            "download_url": request.host_url.rstrip("/") + "/download/final"
        })

    except Exception as e:

        print("❌ ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)