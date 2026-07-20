from gtts import gTTS

def create_voice(text):
    print("Generating voice using gTTS...")

    tts = gTTS(
        text=text,
        lang="en",
        slow=False
    )

    tts.save("voice.mp3")

    print("✅ voice.mp3 generated successfully")