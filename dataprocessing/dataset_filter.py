import json
import transformers
transformers.logging.set_verbosity_error()

def is_wrong_word_length(string):
    return len(string.split()) < 4 or len(string.split()) > 128

def is_too_many_nonletters(string):
    cleaned_string = string.replace(" ", "")
    num_letters = sum(1 for char in cleaned_string if char.isalpha())
    if len(cleaned_string) == 0:
        return True
    return num_letters / len(cleaned_string) < 0.6

def is_unbalanced_length(nb, nn):
    nb_length = len(nb.split())
    nn_length = len(nn.split())
    return nb_length >= 2 * nn_length or nn_length >= 2 * nb_length

def should_filter(entry, seen_entries):
    entry_tuple = (entry["nb"], entry["nn"])
    if entry_tuple in seen_entries:
        return "duplicate"
    seen_entries.add(entry_tuple)
    if is_wrong_word_length(entry["nb"]) or is_wrong_word_length(entry["nn"]):
        return "few_tokens"
    if is_too_many_nonletters(entry["nb"]) or is_too_many_nonletters(entry["nn"]):
        return "too_many_nonletters"
    if is_unbalanced_length(entry["nb"], entry["nn"]):
        return "unbalanced_length"
    if "<INAUDIBLE>" in entry["nb"] or "<INAUDIBLE>" in entry["nn"]:
        return "inaudible"
    return None

def dataset_filter(input_path, output_path):
    seen_entries = set() 
    stats = {
        "total_lines": 0,
        "duplicate_count": 0,
        "inaudible_count": 0,
        "few_tokens_count": 0,
        "too_many_nonletters_count": 0,
        "unbalanced_length_count": 0,
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

    print(f"File: {input_path}")
    print(f"Total lines: {stats['total_lines']}")
    print(f"Duplicates removed: {stats['duplicate_count']}")
    print(f"Lines removed for because of word count: {stats['few_tokens_count']}")
    print(f"Lines removed for too many non-letter characters: {stats['too_many_nonletters_count']}")
    print(f"Lines removed for unbalanced length: {stats['unbalanced_length_count']}")
    print(f"Lines removed for '<INAUDIBLE>': {stats['inaudible_count']}")
    print(f"Lines written to output: {stats['written_count']}\n")

filenames = ["NTB-NPK.jsonl", "NNNB.jsonl", "NPSC.jsonl", "NBS2023.jsonl"]

input_dir = "C:/Users/oscar/oscar/myProjects/masterproject/datasanitization"
output_dir = "C:/Users/oscar/oscar/myProjects/masterproject/dataset"

for filename in filenames:
    input_file = f"{input_dir}/{filename}"
    output_file = f"{output_dir}/{filename}"
    dataset_filter(input_file, output_file)

print("Filtering completed. Unique rows saved to:", output_dir)
