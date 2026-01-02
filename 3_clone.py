import os
import json
import torch
from TTS.api import TTS

# CONFIG
TRANSCRIPT_FILE = "transcript_es_llm.json"
REFERENCE_AUDIO = "temp_audio.wav"
OUTPUT_FOLDER = "dubbed_segments"

def clone_voice():
    # 1. Setup
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    # Load transcript
    with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
        segments = json.load(f)

    # 2. Initialize Model (Force CPU)
    print("--- Loading XTTS Model (This may take a moment) ---")
    # We explicitly accept the license terms here to avoid the prompt
    device = "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    print(f"--- Cloning voice from {REFERENCE_AUDIO} ---")
    
    # 3. Generate Audio
    for i, segment in enumerate(segments):
        text = segment['text']
        start_time = segment['start']
        
        # Skip empty text or failed translations
        if not text or len(text) < 2:
            continue
            
        filename = f"{OUTPUT_FOLDER}/seq_{i:03d}.wav"
        
        print(f"[{i+1}/{len(segments)}] Generating: '{text[:30]}...'")
        
        try:
            # The Magic Line: Generates speech using the reference audio
            tts.tts_to_file(
                text=text,
                speaker_wav=REFERENCE_AUDIO, # Uses original audio to clone voice
                language="es",               # Spanish
                file_path=filename
            )
        except Exception as e:
            print(f"Failed to generate segment {i}: {e}")

    print(f"\nDone! All audio segments saved in '{OUTPUT_FOLDER}/'")

if __name__ == "__main__":
    clone_voice()