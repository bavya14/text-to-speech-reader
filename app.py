"""Streamlit web interface for the Text-to-Speech Reader."""
import tempfile
from pathlib import Path
import streamlit as st
from src.tts_reader import get_voices, save_speech, speak_text

st.set_page_config(page_title="Text-to-Speech Reader", page_icon="🔊")
st.title("🔊 Text-to-Speech Reader")
st.write("Convert typed text or a text file into spoken audio using your system's speech engine.")
st.info("Available voices and audio export depend on your computer's installed speech engine.")

uploaded = st.file_uploader("Upload a UTF-8 text file (optional)", type=["txt"])
default_text = ""
if uploaded is not None:
    try:
        default_text = uploaded.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        st.error("Please upload a text file encoded as UTF-8.")
        default_text = ""

text = st.text_area("Enter or edit text to read aloud", value=default_text, height=220)
rate = st.slider("Speech rate (words per minute)", min_value=80, max_value=300, value=175, step=5)

try:
    voices = get_voices()
except Exception as exc:
    voices = []
    st.warning(f"Could not load system voices: {exc}")

voice_options = {"Default system voice": None}
for voice in voices:
    voice_options[f"{voice['name']}"] = voice["id"]
selected_label = st.selectbox("Voice", list(voice_options.keys()))
selected_voice = voice_options[selected_label]

col1, col2 = st.columns(2)
with col1:
    if st.button("Speak now", type="primary", use_container_width=True):
        if not text.strip():
            st.error("Enter some text first.")
        else:
            try:
                speak_text(text, rate=rate, voice_id=selected_voice)
                st.success("Speech playback finished on the computer running this app.")
            except Exception as exc:
                st.error(f"Speech playback failed: {exc}")
with col2:
    if st.button("Generate audio file", use_container_width=True):
        if not text.strip():
            st.error("Enter some text first.")
        else:
            output_path = None
            try:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    output_path = Path(tmp.name)
                output_path.unlink(missing_ok=True)
                save_speech(text, output_path, rate=rate, voice_id=selected_voice)
                audio_bytes = output_path.read_bytes()
                st.audio(audio_bytes, format="audio/wav")
                st.download_button(
                    "Download speech WAV",
                    data=audio_bytes,
                    file_name="speech.wav",
                    mime="audio/wav",
                    use_container_width=True,
                )
            except Exception as exc:
                st.error(f"Could not export audio with this speech driver: {exc}")
            finally:
                if output_path is not None:
                    output_path.unlink(missing_ok=True)
