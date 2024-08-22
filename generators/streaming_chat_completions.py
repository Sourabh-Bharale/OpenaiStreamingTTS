from typing import Callable, Generator
import openai
import threading
from functools import reduce
from config.openai_client import OPENAI_CLIENT

from constants import (
    DEFAULT_RESPONSE_MODEL,
    DELIMITERS,
    MINIMUM_PHRASE_LENGTH,
)

def stream_delimited_completion(
    stop_event: threading.Event,
    messages: list[dict],
    client: openai.OpenAI = OPENAI_CLIENT,
    model: str = DEFAULT_RESPONSE_MODEL,
    content_transformers: list[Callable[[str], str]] = [],
    phrase_transformers: list[Callable[[str], str]] = [],
    delimiters: list[str] = DELIMITERS,
) -> Generator[str, None, None]:
    """Generates delimited phrases from OpenAI's chat completions."""

    def apply_transformers(s: str, transformers: list[Callable[[str], str]]) -> str:
        return reduce(lambda c, transformer: transformer(c), transformers, s)

    working_string = ""
    for chunk in client.chat.completions.create(
        messages=messages, model=model, stream=True
    ):
        # if the global "all stop" happens, then send the sential value downstream
        # to help cease operations and exit this function right away
        if stop_event.is_set():
            yield None
            return

        content = chunk.choices[0].delta.content or ""

        if content:
            # Apply all transformers to the content before adding it to the working_string
            working_string += apply_transformers(content, content_transformers)
            while len(working_string) >= MINIMUM_PHRASE_LENGTH:
                delimiter_index = -1
                for delimiter in delimiters:
                    index = working_string.find(delimiter, MINIMUM_PHRASE_LENGTH)
                    if index != -1 and (
                        delimiter_index == -1 or index < delimiter_index
                    ):
                        delimiter_index = index

                if delimiter_index == -1:
                    break

                phrase, working_string = (
                    working_string[: delimiter_index + len(delimiter)],
                    working_string[delimiter_index + len(delimiter) :],
                )
                yield apply_transformers(phrase, content_transformers)

    # Yield any remaining content that didn't end with the delimiter
    if working_string.strip():
        yield working_string.strip()

    yield None  # Sentinel value to signal "no more coming"
