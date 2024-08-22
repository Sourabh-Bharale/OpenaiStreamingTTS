
# Constants
DELIMITERS = [f"{d} " for d in (".", "?", "!")]  # Determine where one phrase ends
MINIMUM_PHRASE_LENGTH = 200  # Minimum length of phrases to minimize audio choppiness
TTS_CHUNK_SIZE = 1024

# Default values
DEFAULT_RESPONSE_MODEL = "gpt-3.5-turbo"
DEFAULT_TTS_MODEL = "tts-1"
DEFAULT_VOICE = "alloy"

# Prompt constants
AUDIO_FRIENDLY_INSTRUCTION = "Make sure your output is formatted in such a way that it can be read out loud (it will be turned into spoken words) from your response directly."
PROMPT_OPTIONS = {
    "story": "write an story about an employee working in MNC it should be minimum 1000 words and end with an happy ending",
    "getty": "explain the gettysburg address to a ten year old. then say the speech in a way they'd understand",
    "toast": "write a sixty sentence story about toast",
    "counter": "Count to 15, with a comma between each number, unless it's a multiple of 3z (including 3), then use only a period (ex. '4, 5, 6. 7,'), and no newlines. E.g., 1, 2, 3, ...",
    "punc": "say five senteces. each one ending with different punctuation. at least one question. each sentence should be at least 50 words long.",
}

PROMPT_TO_USE = f"{PROMPT_OPTIONS['story']}. {AUDIO_FRIENDLY_INSTRUCTION}"
