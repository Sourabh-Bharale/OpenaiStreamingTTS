import queue
import threading
import openai

from constants import (
    DEFAULT_VOICE,
    DEFAULT_TTS_MODEL,
    TTS_CHUNK_SIZE,
)

from config.openai_client import OPENAI_CLIENT

def text_to_speech_processor(
    stop_event: threading.Event,
    phrase_queue: queue.Queue,
    audio_queue: queue.Queue,
    client: openai.OpenAI = OPENAI_CLIENT,
    model: str = DEFAULT_TTS_MODEL,
    voice: str = DEFAULT_VOICE,
):
    """Processes phrases into speech and puts the audio in the audio queue."""
    while not stop_event.is_set():
        phrase = phrase_queue.get()
        # Got the signal that nothing more is coming, so pass that down and exit
        if phrase is None:
            audio_queue.put(None)
            return

        try:
            with client.audio.speech.with_streaming_response.create(
                model=model, voice=voice, response_format="pcm", input=phrase
            ) as response:
                for chunk in response.iter_bytes(chunk_size=TTS_CHUNK_SIZE):
                    audio_queue.put(chunk)
                    if stop_event.is_set():
                        return
        except Exception as e:
            print(f"Error in text_to_speech_processor: {e}")
            audio_queue.put(None)
            return
