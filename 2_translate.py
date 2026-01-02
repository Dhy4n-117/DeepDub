import json
from googletrans import Translator

# CONFIG
INPUT_FILE = "transcript.json"
OUTPUT_FILE = "transcript_es.json"
TARGET_LANG = "es" # Change to 'hi' for Hindi, 'fr' for French, etc.

def translate_transcript():
    print(f"--- Loading {INPUT_FILE} ---")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    translator = Translator()
    translated_data = []

    print(f"--- Translating to {TARGET_LANG} ---")
    
    for segment in data:
        original_text = segment['text']
        
        # Translate the text
        try:
            translation = translator.translate(original_text, dest=TARGET_LANG)
            translated_text = translation.text
            
            print(f"Original: {original_text}")
            print(f"Translated: {translated_text}")
            print("-" * 20)

            # Keep the original timestamps, just swap the text
            translated_data.append({
                "start": segment['start'],
                "end": segment['end'],
                "text": translated_text,
                "original_text": original_text # Keep original for reference
            })
            
        except Exception as e:
            print(f"Error translating segment: {original_text}")
            print(e)
            # If fail, keep original text so pipeline doesn't break
            translated_data.append(segment) 

    # Save the new JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(translated_data, f, indent=4, ensure_ascii=False)
    
    print(f"Done! Saved translated data to {OUTPUT_FILE}")

if __name__ == "__main__":
    translate_transcript()