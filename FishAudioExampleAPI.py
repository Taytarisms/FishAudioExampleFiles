import os
import wave
from pathlib import Path
import httpx
import pyaudio
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("FISH_API_KEY") # Ensure you have an appropriate file made in your directory
VOICE_ID = "b347db033a6549378b48d00acb0d06cd"

OUTPUT_DEVICE_ID = None # None = System Default
OUTPUT_FILE = Path(r"Enter your path here.") / "fish_api_output.wav"

if not API_KEY:
    raise RuntimeError(
        "FISH_API_KEY was not found. Add it to your .env file."
    )

def play_audio(audio_path: Path) -> None:
    with wave.open(str(audio_path), "rb") as wav_file:
        player = pyaudio.PyAudio()
        stream = None

        try:
            stream_options = {
                "format": player.get_format_from_width(
                    wav_file.getsampwidth()
                ),
                "channels": wav_file.getnchannels(),
                "rate": wav_file.getframerate(),
                "output": True,
            }

            if OUTPUT_DEVICE_ID is not None:
                stream_options["output_device_index"] = OUTPUT_DEVICE_ID

            stream = player.open(**stream_options)
            chunk_size = 1024
            data = wav_file.readframes(chunk_size)
            while data:
                stream.write(data)
                data = wav_file.readframes(chunk_size)
        finally:
            if stream is not None:
                stream.stop_stream()
                stream.close()
            player.terminate()

payload = {
    "text": """[excited] Hello from the direct Fish Audio API! 
    [giggle] We hope you enjoy our product and follow FellStarTay on Twitch!""",
    "reference_id": VOICE_ID,
    "format": "wav",
    "sample_rate": 44100,
}

response = httpx.post(
    "https://api.fish.audio/v1/tts",
    json=payload,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "model": "s2.1-pro-free",
    },
    timeout=120.0,
)

response.raise_for_status()
OUTPUT_FILE.write_bytes(response.content)
print(f"Audio saved to: {OUTPUT_FILE}")
play_audio(OUTPUT_FILE)