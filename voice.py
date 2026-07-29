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

    last_error = None

    for attempt in range(3):

        try:

            asyncio.run(generate(text))

            print("✅ voice.mp3 generated")

            return

        except Exception as e:

            last_error = e

            print(f"Retry {attempt+1}/3 failed")

    raise last_error