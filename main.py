import queue
import threading
from audio_player import audio_player
from processors.tts import text_to_speech_processor
from generators.phrase_generator import phrase_generator
from config.global_stop import stop_event, wait_for_enter


def main():
    phrase_queue = queue.Queue()
    audio_queue = queue.Queue()

    phrase_generation_thread = threading.Thread(
        target=phrase_generator, args=(phrase_queue,stop_event)
    )
    tts_thread = threading.Thread(
        target=text_to_speech_processor, args=(stop_event,phrase_queue, audio_queue)
    )
    audio_player_thread = threading.Thread(target=audio_player, args=(audio_queue,stop_event))

    phrase_generation_thread.start()
    tts_thread.start()
    audio_player_thread.start()

    # Create and start the "enter to stop" thread. Daemon means it will not block
    # exiting the script when all the other (non doemon) threads have completed.
    threading.Thread(target=wait_for_enter, daemon=True).start()

    phrase_generation_thread.join()
    print("## all phrases enqueued. phrase generation thread terminated.")
    tts_thread.join()
    print("## all tts complete and enqueued. tts thread terminated.")
    audio_player_thread.join()
    print("## audio output complete. audio player thread terminated.")


if __name__ == "__main__":
    main()