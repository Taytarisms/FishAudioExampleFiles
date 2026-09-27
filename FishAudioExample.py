from pathlib import Path
from fishaudio import FishAudio
from fishaudio.types import TTSConfig
from dotenv import load_dotenv
import pyaudio
import wave

load_dotenv()
OUTPUT_DEVICE_ID = None # None = System Default
OUTPUT_FILE = Path(r"Enter Path here.") / "fish_audio_output.wav"
client = FishAudio()  # Reads FISH_API_KEY from the environment
text_to_be_inferenced = "Hello from Fish Audio!" # You can edit this text to your liking.
config = TTSConfig(
    reference_id="b347db033a6549378b48d00acb0d06cd", # Enter your copied ID into here.
    format="wav",
)

audio = client.tts.convert(
    text=text_to_be_inferenced,
    model="s2.1-pro-free",
    config=config,
)

print(f"Text inferenced: {text_to_be_inferenced}")

OUTPUT_FILE.write_bytes(audio)
print(f"Audio saved to: {OUTPUT_FILE}")


def play_audio(audio_path: Path) -> None:
    with wave.open(str(audio_path), "rb") as wav_file:
        player = pyaudio.PyAudio()

        try:
            stream = player.open(
                format=player.get_format_from_width(
                    wav_file.getsampwidth()
                ),
                channels=wav_file.getnchannels(),
                rate=wav_file.getframerate(),
                output=True,
                output_device_index=OUTPUT_DEVICE_ID,
            )

            try:
                chunk_size = 1024
                data = wav_file.readframes(chunk_size)

                while data:
                    stream.write(data)
                    data = wav_file.readframes(chunk_size)
            finally:
                stream.stop_stream()
                stream.close()
        finally:
            player.terminate()

play_audio(OUTPUT_FILE)