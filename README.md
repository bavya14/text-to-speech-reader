# Text-to-Speech Reader

A Python text-to-speech application that reads typed text aloud or extracts text from uploaded `.txt` files. It includes a Streamlit web interface, adjustable speech speed, and voice selection where supported by the installed speech engine.

## Features

- Enter text or upload a UTF-8 `.txt` file.
- Convert text to speech using `pyttsx3` (offline, when a supported system speech engine is installed).
- Adjust speaking rate.
- Select an available system voice.
- Download generated speech as a WAV file where supported.
- Automated tests and GitHub Actions workflow.

## Technology stack

- Python 3.10 or 3.11
- pyttsx3 — offline text-to-speech interface
- Streamlit — web interface
- pytest — tests

## Installation

Create and activate a virtual environment.

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### System speech engine notes

`pyttsx3` uses speech engines available on your operating system. Windows commonly uses SAPI5; macOS uses NSSpeechSynthesizer; Linux typically uses eSpeak. On Linux, you may need to install `espeak-ng` (or `espeak`) using your distribution's package manager. System voice availability varies by computer.

## Run the web app

```bash
streamlit run app.py
```

Type text or upload a `.txt` file, select a voice and rate, then click **Generate speech**. The app attempts to create a WAV download. Some operating systems or speech drivers may not support saving audio in the same way; see troubleshooting below.

## Run from the command line

Speak text aloud:

```bash
python -m src.tts_reader --text "Hello! Welcome to the text to speech reader."
```

Read text from a file:

```bash
python -m src.tts_reader --file sample_texts/example.txt
```

Save speech to a file (driver support varies):

```bash
python -m src.tts_reader --text "This is a speech sample." --output speech.wav
```

## Project structure

```text
text_to_speech_reader/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   ├── __init__.py
│   └── tts_reader.py
├── tests/
│   └── test_tts_reader.py
├── sample_texts/
│   └── example.txt
└── .github/
    └── workflows/
        └── tests.yml
```

## How it works

1. The user enters text or uploads a text file.
2. The app validates that the text is not empty.
3. `pyttsx3` sends the text to the computer's installed speech engine.
4. The selected voice and speaking rate are applied.
5. The app plays or saves the generated speech, depending on platform support.

## Troubleshooting

- **No voices available:** Install or enable a system speech engine and restart the app.
- **Linux audio engine error:** Install eSpeak NG and required audio packages using your Linux distribution's package manager.
- **WAV download fails:** The speech driver may not support file output in the current environment. Try the command-line mode or another system voice.
- **Text file looks incorrect:** Save it as UTF-8.
- **The app is silent:** Check system volume, output device, and the operating system's speech engine.

## Limitations

- Voice options depend on the operating system; this project does not bundle voices.
- Speech quality and supported languages vary by installed voice.
- Audio export is dependent on the speech driver.
- The app processes text locally through the system speech engine; avoid entering sensitive text on shared devices.

## GitHub upload

Create a repository named `text-to-speech-reader`, extract this ZIP, and upload the extracted files and folders.

Or use Git in the extracted project folder:

```bash
git init
git add .
git commit -m "Add text to speech reader"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/text-to-speech-reader.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.
