import queue
import threading
from constants import PROMPT_TO_USE
from . import streaming_chat_completions

def phrase_generator(phrase_queue: queue.Queue, stop_event: threading.Event):
    """Generates phrases and puts them in the phrase queue."""
    print(f"sending prompt:\n{PROMPT_TO_USE}\n- - - - - - - - - -")

    for phrase in streaming_chat_completions.stream_delimited_completion(
        stop_event=stop_event,
        messages=[{"role": "user", "content": PROMPT_TO_USE}],
        content_transformers=[
            lambda c: c.replace("\n", " ")
        ],  # If a line ends with a period, this helps it be recognized as a phrase.
        phrase_transformers=[
            lambda p: p.strip()
        ],  # Since each phrase is being used for audio, we don't need white-space
    ):
        # Sentinel (nothing more coming) signal received, so pass it downstream and exit
        if phrase is None:
            phrase_queue.put(None)
            return

        print(f"> {phrase}")
        phrase_queue.put(phrase)

