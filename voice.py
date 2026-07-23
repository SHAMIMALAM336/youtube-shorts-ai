import asyncio
import edge_tts

VOICE = "en-US-AndrewNeural"

async def generate(text):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save("voice.mp3")


def create_voice(text):
    print("Generating Professional AI Voice...")

    asyncio.run(generate(text))

    print("✅ voice.mp3 generated")