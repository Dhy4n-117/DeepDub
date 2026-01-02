import ffmpeg
import json
from faster_whisper import WhisperModel
import os

# CONFIG
VIDEO_PATH = "input_video.mp4" # Put a short video file in your folder named this
MODEL_SIZE = "small" # options: tiny, base, small, medium, large-v2
DEVICE = "cpu" # Change to "cpu" if you don't have an NVIDIA GPU

def extract_audio(video_path, audio_output="temp_audio.wav"):
    print(f"--- Extracting audio from {video_path} ---")
    if os.path.exists(audio_output):
        os.remove(audio_output)
        
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_output, ac=1, ar=16000) # Mono, 16kHz for Whisper
            .run(quiet=True, overwrite_output=True)
        )
        print("Audio extracted successfully.")
        return audio_output
    except ffmpeg.Error as e:
        print("FFmpeg Error! Make sure FFmpeg is installed and in your PATH.")
        return None

def transcribe_audio(audio_path):
    print(f"--- Transcribing with Whisper ({MODEL_SIZE}) ---")
    
    # Run on GPU with FP16
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type="int8")
    
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    print(f"Detected language: '{info.language}' with probability {info.language_probability}")
    
    transcript_data = []
    
    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        transcript_data.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })
        
    return transcript_data

if __name__ == "__main__":
    if not os.path.exists(VIDEO_PATH):
        print(f"Error: Please place a video file named '{VIDEO_PATH}' in this folder.")
    else:
        audio_file = extract_audio(VIDEO_PATH)
        if audio_file:
            data = transcribe_audio(audio_file)
            
            # --- NEW CODE STARTS HERE ---
            with open("transcript.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print("Saved transcript to 'transcript.json'")