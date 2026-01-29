import json

def save_to_file(results, filename="ai_responses.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✓ Results saved to {filename}")
    except Exception as e:
        print(f"✗ Failed to save: {e}")