import os
import json

base_path = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(os.path.dirname(os.path.dirname(base_path)), "dataprocessing")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

input_files = [
    "NPSC-eval.json",
    "NPSC-train.json",
    "NPSC-test.json",
]
output_file = os.path.join(output_dir, "NPSC.jsonl")

# Open the output file in write mode
with open(output_file, "w", encoding="utf-8") as outfile:
    for filename in input_files:
        file_path = os.path.join(base_path, filename)
        
        # Handle JSONL files directly
        if filename.endswith(".jsonl"):
            with open(file_path, "r", encoding="utf-8") as infile:
                for line in infile:
                    outfile.write(line)
        else:
            # Attempt to read JSON files either as a list or line by line
            try:
                with open(file_path, "r", encoding="utf-8") as infile:
                    data = json.load(infile)  # Attempt to load as a JSON list
                    for entry in data:
                        outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")
            except json.JSONDecodeError:
                # If the JSON load fails, fall back to line-by-line reading
                with open(file_path, "r", encoding="utf-8") as infile:
                    for line in infile:
                        try:
                            entry = json.loads(line.strip())
                            outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")
                        except json.JSONDecodeError:
                            print(f"Warning: Skipping invalid JSON line in {filename}: {line.strip()}")

print(f"All files have been combined and saved to {output_file}.")
