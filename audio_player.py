import queue
import pyaudio
import threading

def audio_player(audio_queue: queue.Queue, stop_event: threading.Event):
    """Plays audio from the audio queue."""
    p = pyaudio.PyAudio()
    player_stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    try:
        while not stop_event.is_set():
            audio_data = audio_queue.get()
            # got the sentinel value that there's nothing more coming, so exit
            if audio_data is None:
                break
            player_stream.write(audio_data)
    except Exception as e:
        print(f"Error in audio_player: {e}")
    finally:
        player_stream.stop_stream()
        player_stream.close()
        p.terminate()
