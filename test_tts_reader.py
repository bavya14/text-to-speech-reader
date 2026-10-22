import pytest
from src.tts_reader import speak_text, save_speech


def test_empty_text_is_rejected():
    with pytest.raises(ValueError):
        speak_text("   ")


def test_invalid_rate_is_rejected_before_engine_start():
    with pytest.raises(ValueError):
        speak_text("Hello", rate=500)


def test_empty_text_cannot_be_saved(tmp_path):
    with pytest.raises(ValueError):
        save_speech("", tmp_path / "out.wav")
