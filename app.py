from flask import Flask, request, jsonify
from voice import create_voice
import os
from search_video import search_video

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube Shorts AI Backend is Running!"

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

        create_voice(script)

        # Check if voice.mp3 was created
        if os.path.exists("voice.mp3"):
            print("✅ voice.mp3 generated successfully")
            print("File Size:", os.path.getsize("voice.mp3"), "bytes")
        else:
            print("❌ voice.mp3 NOT generated")

        return jsonify({
            "success": True,
            "title": title,
            "status": "Voice Generated",
            "audio_file": "voice.mp3"
        })

    except Exception as e:

        print("❌ ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)