import asyncio
import edge_tts

VOICE = "en-US-AndrewNeural"

async def generate(text):
    print("Starting Edge TTS...")

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await asyncio.wait_for(
        communicate.save("voice.mp3"),
        timeout=60
    )

    print("Voice saved.")


def create_voice(text):
    print("Generating AI Voice...")

    asyncio.run(generate(text))

    print("✅ voice.mp3 generated")