from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube Shorts AI Backend is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    print("Received:", data)

    return jsonify({
        "success": True,
        "title": data.get("title"),
        "status": "Webhook Working"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)