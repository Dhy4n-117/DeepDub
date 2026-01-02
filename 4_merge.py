import os
import json
import subprocess

# CONFIG
VIDEO_PATH = "input_video.mp4"
OUTPUT_VIDEO = "final_dubbed_video.mp4"
DUB_FOLDER = "dubbed_segments"
TRANSCRIPT_FILE = "transcript_es.json"

def merge_audio_video():
    print("--- 1. Creating Silence/Audio Map ---")
    
    # We need to build a complex FFmpeg filter to place audio at exact timestamps
    with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
        segments = json.load(f)

    filter_complex = ""
    inputs = ""
    
    # Start with a silent base audio track that matches video length
    # (We will handle this by just overlaying clips on top of silence)
    
    inputs += f"-i {VIDEO_PATH} " # Input 0: Video
    
    audio_indices = []
    
    for i, segment in enumerate(segments):
        audio_file = f"{DUB_FOLDER}/seq_{i:03d}.wav"
        
        if os.path.exists(audio_file):
            start_time = segment['start']
            # Multiply start_time by 1000 for ms (if needed) but FFmpeg uses seconds
            start_ms = int(start_time * 1000)
            
            inputs += f"-i {audio_file} "
            # We want to delay this specific audio clip to start at 'start_time'
            # Input index starts at 1 because 0 is the video
            audio_indices.append(f"[{i+1}:a]adelay={start_ms}|{start_ms}[a{i}];")

    # Combine all delays
    filter_complex += "".join(audio_indices)
    
    # Mix all audio streams
    # We have N audio segments. We mix them into one.
    mix_inputs = "".join([f"[a{i}]" for i in range(len(audio_indices))])
    filter_complex += f"{mix_inputs}amix=inputs={len(audio_indices)}:dropout_transition=0[outa]"

    print("--- 2. Running FFmpeg Merger ---")
    
    # Construct the massive command
    cmd = f'ffmpeg -y {inputs} -filter_complex "{filter_complex}" -map 0:v -map "[outa]" -c:v copy {OUTPUT_VIDEO}'
    
    # Run it
    subprocess.run(cmd, shell=True)
    
    print(f"\nDone! Your dubbed video is ready: {OUTPUT_VIDEO}")

if __name__ == "__main__":
    if not os.path.exists(DUB_FOLDER):
        print("Error: Dubbed segments not found. Run 3_clone.py first.")
    else:
        merge_audio_video()