# python test.py ..\data\consultation1.json

import os
import json
import sys
import openai

openai.api_key = ""

def generate_discharge_note(input_json_path):
    with open(input_json_path, 'r') as file:
        data = json.load(file)
    
    prompt = ("You are a veterinary assistant. "
              "Given this consultation JSON, produce one concise paragraph summary "
              "of the entire visit and discharge with no bullets or markdown - just plain text.\n\n"
              f"{json.dumps(data)}")

    response = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}]
    )

    note = response.choices[0].message.content.strip()

    output_json = {
        "discharge_note": note
    }
    
    return output_json

if __name__ == "__main__":
    input_path = sys.argv[1]
    note = generate_discharge_note(input_path)
    print(json.dumps(note, indent=2))
