import json
import re

def clean_punctuation(text):
    new_text = re.sub(r'\s+', ' ', text).strip()  # fix double spaces
    return new_text, new_text != text

def remove_metadata(text):
    new_text = re.sub(r'^(?:[\w\s]+ )?\([^)]*\): ?', '', text).strip()
    return new_text, new_text != text

def remove_special_tokens(text):
    new_text = re.sub(r'<\*?ee>', '', text).strip()
    new_text = re.sub(r'<\*?mm>', '', new_text).strip()
    new_text = re.sub(r'<\*?qq>', '', new_text).strip()
    new_text = re.sub(r'\s+', ' ', new_text).strip()  # fix double spaces that have arosen
    return new_text, new_text != text

def sanitize_text(entry, stats, filename):
    metadata_changed = punctuation_changed = special_tokens_changed = False
    changed_pair = False
    
    for key in ["nb", "nn"]:
        # Apply remove_metadata only if filename is "NTB-NPK.jsonl"
        
        new_text, changed = clean_punctuation(entry[key])
        entry[key] = new_text
        punctuation_changed |= changed
        changed_pair |= changed

        if filename == "NTB-NPK.jsonl":
            new_text, changed = remove_metadata(entry[key])
            entry[key] = new_text
            metadata_changed |= changed
            changed_pair |= changed
        
        new_text, changed = remove_special_tokens(entry[key])
        entry[key] = new_text
        special_tokens_changed |= changed
        changed_pair |= changed

    # Update stats, counting only once per sentence pair
    stats["metadata_count"] += metadata_changed
    stats["punctuation_count"] += punctuation_changed
    stats["special_tokens_count"] += special_tokens_changed
    stats["changed_count"] += changed_pair

    return entry

def dataset_sanitize(input_path, output_path, filename):
    stats = {
        "total_lines": 0,   
        "metadata_count": 0,
        "punctuation_count": 0,
        "special_tokens_count": 0,
        "changed_count": 0
    }
    
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            stats["total_lines"] += 1
            entry = json.loads(line)
            entry = sanitize_text(entry, stats, filename)
            
            outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"File: {input_path}")
    print(f"Total lines: {stats['total_lines']}")
    print(f"Punctuation cleanup: {stats['punctuation_count']}")
    print(f"Metadata removals: {stats['metadata_count']}")  # This should be 0 for file!=NTB-NPK.jsonl
    print(f"Special token removals: {stats['special_tokens_count']}")
    print(f"Sentence pairs changed: {stats['changed_count']}\n")

filenames = ["NTB-NPK.jsonl", "NNNB.jsonl", "NPSC.jsonl", "NBS2023.jsonl"]

input_dir = "C:/Users/oscar/oscar/myProjects/masterproject/dataprocessing"
output_dir = "C:/Users/oscar/oscar/myProjects/masterproject/datasanitization"

for filename in filenames:
    input_file = f"{input_dir}/{filename}"
    output_file = f"{output_dir}/{filename}"
    dataset_sanitize(input_file, output_file, filename)

print("Sanitization completed. Processed files saved to:", output_dir)
