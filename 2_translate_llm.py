import json
import ollama
import os

# CONFIG
INPUT_FILE = "transcript.json"
OUTPUT_FILE = "transcript_es_llm.json"
TARGET_LANG = "Spanish" 
MODEL_NAME = "llama3.2"  # Using the model you just pulled

# --- THE PROMPT ENGINEERING ---
# We force the AI to act like a Chef Translator
SYSTEM_PROMPT = f"""
You are a professional subtitle translator for a high-end cooking show.
Your Goal: Translate the input text into natural-sounding {TARGET_LANG}.

Rules:
1. Context is COOKING. Interpret words like "chop", "season", "dash" in culinary terms.
   - Example: "Chop" -> "Picar" or "Cortar" (NOT "Chuleta").
2. Keep the tone casual and instructional.
3. Output ONLY the translation. No explanations.
"""

def translate_with_llm():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run 1_transcribe.py first.")
        return

    print(f"--- Loading {INPUT_FILE} ---")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    translated_data = []
    print(f"--- Starting LLM Translation (Model: {MODEL_NAME}) ---")

    for i, segment in enumerate(data):
        original_text = segment['text']
        
        # Skip empty lines
        if not original_text.strip():
            continue

        print(f"[{i+1}/{len(data)}] Translating: '{original_text[:30]}...'")

        try:
            # Send to Ollama
            response = ollama.chat(model=MODEL_NAME, messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': f"Translate exactly: '{original_text}'"}
            ])
            
            translated_text = response['message']['content'].strip()
            
            # Clean up quotes if the AI added them
            if translated_text.startswith('"') and translated_text.endswith('"'):
                translated_text = translated_text[1:-1]

            print(f"   -> {translated_text}")
            
            translated_data.append({
                "start": segment['start'],
                "end": segment['end'],
                "text": translated_text,
                "original_text": original_text
            })

        except Exception as e:
            print(f"   [ERROR] {e}")
            translated_data.append(segment) 

    # Save to NEW file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(translated_data, f, indent=4, ensure_ascii=False)
    
    print(f"\nDone! Smart translation saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    translate_with_llm()