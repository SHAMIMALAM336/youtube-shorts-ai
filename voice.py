import asyncio
import edge_tts

async def generate_voice(text, output_file="voice.mp3"):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AndrewNeural"
    )
    await communicate.save(output_file)

def create_voice(text):
    asyncio.run(generate_voice(text))