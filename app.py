from flask import Flask, request, jsonify
from voice import create_voice
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube Shorts AI Backend is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True)

    title = data.get("title", "")
    script = data.get("script", "")

    print("Title:", title)
    print("Generating voice...")

    try:
        create_voice(script)

        return jsonify({
            "success": True,
            "title": title,
            "status": "Voice Generated",
            "audio_file": "voice.mp3"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)