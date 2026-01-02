# 🎙️ DeepDub: Automated AI Video Dubbing Pipeline

**DeepDub** is an automated pipeline that dubs video content into other languages while preserving the original speaker's voice. It uses a chain of state-of-the-art AI models to transcribe, translate (with cultural nuance), and clone voices locally.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Ollama](https://img.shields.io/badge/AI-Llama%203.2-orange) ![Coqui TTS](https://img.shields.io/badge/TTS-Coqui%20XTTS-green)

## 🧠 The Architecture

The pipeline consists of four distinct modules:

1.  **The Ear (Transcription):** Uses **Faster-Whisper** to extract audio and generate precise timestamps.
2.  **The Brain (Translation):** Uses **Llama 3.2 (via Ollama)** with a custom system prompt to perform context-aware translation (e.g., understanding that "chop" in a kitchen means "cut," not "pork chop").
3.  **The Voice (Cloning):** Uses **Coqui XTTS v2** to clone the original speaker's timbre and generate speech in the target language (Spanish, Hindi, etc.).
4.  **The Editor (Assembly):** Uses **FFmpeg** to surgically insert the new audio segments at the correct timestamps, mixing them with the original background noise.

## 🛠️ Tech Stack

* **Language:** Python
* **Transcription:** `faster-whisper` (OpenAI Whisper optimized)
* **Translation:** `ollama` running `llama3.2` (Local LLM)
* **Voice Cloning:** `TTS` (Coqui XTTS v2)
* **Media Processing:** `ffmpeg-python`

## 🚀 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/DeepDub.git](https://github.com/yourusername/DeepDub.git)
    cd DeepDub
    ```

2.  **Install Dependencies**
    *(Note: Microsoft C++ Build Tools are required for Coqui TTS on Windows)*
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Local LLM**
    Download [Ollama](https://ollama.com) and pull the lightweight model:
    ```bash
    ollama pull llama3.2
    ```

## 🎬 How to Run

1.  Place your video file in the root folder and rename it to `input_video.mp4`.
2.  **Step 1: Extract & Transcribe**
    ```bash
    python 1_transcribe.py
    ```
3.  **Step 2: Smart Translation**
    ```bash
    python 2_translate_llm.py
    ```
4.  **Step 3: Generate Voice Clones**
    ```bash
    python 3_clone.py
    ```
5.  **Step 4: Merge Video**
    ```bash
    python 4_merge.py
    ```
6.  **Done!** Check `final_dubbed_video.mp4` for the result.

## 🔮 Future Roadmap

* [ ] **Lip Sync:** Implement `Wav2Lip` to match mouth movements to the new language.
* [ ] **Background Noise Separation:** Use `Spleeter` to isolate voice from music for cleaner mixing.
* [ ] **GUI:** Build a Streamlit interface for drag-and-drop dubbing.
