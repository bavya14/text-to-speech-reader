"""Text-to-speech functions and command-line interface."""
from __future__ import annotations
import argparse
from pathlib import Path
import pyttsx3


def get_voices() -> list[dict[str, str]]:
    """Return voice IDs and display names from the installed speech engine."""
    engine = pyttsx3.init()
    try:
        voices = engine.getProperty("voices")
        return [
            {"id": str(voice.id), "name": str(getattr(voice, "name", voice.id))}
            for voice in voices
        ]
    finally:
        engine.stop()


def speak_text(text: str, rate: int = 175, voice_id: str | None = None) -> None:
    """Speak text aloud using the system speech engine."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must not be empty.")
    if rate < 80 or rate > 300:
        raise ValueError("Rate must be between 80 and 300 words per minute.")

    engine = pyttsx3.init()
    try:
        engine.setProperty("rate", rate)
        if voice_id:
            engine.setProperty("voice", voice_id)
        engine.say(text)
        engine.runAndWait()
    finally:
        engine.stop()


def save_speech(text: str, output_path: str | Path, rate: int = 175,
                voice_id: str | None = None) -> Path:
    """Ask the installed driver to save speech to an audio file."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must not be empty.")
    if rate < 80 or rate > 300:
        raise ValueError("Rate must be between 80 and 300 words per minute.")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    engine = pyttsx3.init()
    try:
        engine.setProperty("rate", rate)
        if voice_id:
            engine.setProperty("voice", voice_id)
        engine.save_to_file(text, str(output))
        engine.runAndWait()
    finally:
        engine.stop()

    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError(
            "The speech engine did not create an output file. "
            "Check whether your system speech driver supports audio export."
        )
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Text to speak")
    source.add_argument("--file", help="UTF-8 text file to read")
    parser.add_argument("--rate", type=int, default=175, help="Speech rate (80–300)")
    parser.add_argument("--voice", help="Optional system voice ID")
    parser.add_argument("--output", help="Optional output audio file, usually WAV")
    args = parser.parse_args()

    text = args.text if args.text is not None else Path(args.file).read_text(encoding="utf-8")
    if args.output:
        output = save_speech(text, args.output, args.rate, args.voice)
        print(f"Saved speech to {output}")
    else:
        speak_text(text, args.rate, args.voice)
        print("Speech playback finished.")


if __name__ == "__main__":
    main()
