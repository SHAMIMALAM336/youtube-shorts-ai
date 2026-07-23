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

    # ===============================
    # Delete old files
    # ===============================
    for f in ["voice.mp3", "video.mp4", "final.mp4"]:
        if os.path.exists(f):
            os.remove(f)

    data = request.get_json(force=True)

    title = data.get("title", "")
    script = data.get("script", "")

    print("===================================")
    print("Title:", title)
    print("Generating Professional Video")
    print("===================================")

    try:

        # ===============================
        # Generate Voice
        # ===============================
        create_voice(script)

        if not os.path.exists("voice.mp3"):
            raise Exception("voice.mp3 not generated")

        print("✅ Voice Generated")
        print("Voice Size:", os.path.getsize("voice.mp3"), "bytes")

        # ===============================
        # Download Pexels Video
        # ===============================
        print("===================================")
        print("Downloading HD Video...")
        print("===================================")

        download_pexels(title)

        if not os.path.exists("video.mp4"):
            raise Exception("video.mp4 not found")

        print("✅ Video Downloaded")
        print("Video Size:", os.path.getsize("video.mp4"), "bytes")

        # ===============================
        # Merge
        # ===============================
        print("===================================")
        print("Creating Final Video...")
        print("===================================")

        merge_video()

        if not os.path.exists("final.mp4"):
            raise Exception("final.mp4 not generated")

        final_size = os.path.getsize("final.mp4")

        print("✅ Final Video Generated")
        print("Final Size:", final_size, "bytes")

        if final_size < 500000:
            raise Exception("final.mp4 corrupted")

        return jsonify({
            "success": True,
            "title": title,
            "status": "Professional Video Ready",
            "download_url": request.host_url.rstrip("/") + "/download/final"
        })

    except Exception as e:

        print("===================================")
        print("ERROR")
        print(str(e))
        print("===================================")

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)