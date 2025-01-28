import json
import re
import transformers
transformers.logging.set_verbosity_error()

def is_few_tokens(string):
    tokens = [token for token in re.findall(r'\b\w+\b', string) if token.isalpha()]
    return len(tokens) <= 2

def is_too_many_nonletters(string):
    num_letters = len(re.findall(r'[a-zA-ZÆØÅæøå]', string))
    num_non_letters = len(string) - num_letters
    return num_non_letters >= num_letters

def should_filter(entry, seen_entries):
    entry_tuple = (entry["nb"], entry["nn"])
    if entry_tuple in seen_entries:
        return "duplicate"
    seen_entries.add(entry_tuple)
    if "<INAUDIBLE>" in entry["nb"] or "<INAUDIBLE>" in entry["nn"]:
        return "inaudible"
    if is_few_tokens(entry["nb"]) or is_few_tokens(entry["nn"]):
        return "few_tokens"
    if is_too_many_nonletters(entry["nb"]) or is_too_many_nonletters(entry["nn"]):
        return "too_many_nonletters"
    return None

def dataset_filter(input_path, output_path):
    seen_entries = set() 
    stats = {
        "total_lines": 0,
        "duplicate_count": 0,
        "inaudible_count": 0,
        "few_tokens_count": 0,
        "too_many_nonletters_count": 0,
        "written_count": 0
    }

    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            stats["total_lines"] += 1
            entry = json.loads(line)

            reason = should_filter(entry, seen_entries)
            if reason:
                stats[f"{reason}_count"] += 1
                continue

            outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")
            stats["written_count"] += 1

    print(f"Fil: {input_path}")
    print(f"Totalt antall linjer: {stats['total_lines']}")
    print(f"Antall duplikater fjernet: {stats['duplicate_count']}")
    print(f"Antall linjer fjernet pga. '<INAUDIBLE>': {stats['inaudible_count']}")
    print(f"Antall linjer fjernet pga. få tokens: {stats['few_tokens_count']}")
    print(f"Antall linjer fjernet pga. for mange ikke-bokstavtegn: {stats['too_many_nonletters_count']}")
    print(f"Antall linjer skrevet til output: {stats['written_count']}\n")

filenames = ["NTB-NPK.jsonl", "NNNB.jsonl", "NPSC.jsonl", "NBS2023.jsonl"]

input_dir = "C:/Users/oscar/oscar/myProjects/masterproject/dataprocessing"
output_dir = "C:/Users/oscar/oscar/myProjects/masterproject/dataset"

for filename in filenames:
    input_file = f"{input_dir}/{filename}"
    output_file = f"{output_dir}/{filename}"
    dataset_filter(input_file, output_file)

print("Filtrering fullført og unike rader lagret i mappen:", output_dir)
