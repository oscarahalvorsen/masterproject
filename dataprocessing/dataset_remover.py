import json
import re
from bert_score import score
import transformers
transformers.logging.set_verbosity_error()


# Funksjon for å sjekke om en streng har to eller færre bokstavkarakterer
def is_non_alpha(string):
    return len(re.findall(r'[a-zA-ZÆØÅæøå]', string)) <= 2

def is_non_alpha0(string):
    return len(re.findall(r'[a-zA-ZÆØÅæøå]', string)) <= 0

def is_non_alpha3(string):
    tokens = re.findall(r'\S+', string)
    return len(tokens) == 3

# Funksjon for å beregne BERTScore i batcher
def calculate_bertscore_batch(references, candidates):
    _, _, F1 = score(candidates, references, model_type="roberta-base", lang="en", rescale_with_baseline=False, batch_size=8)
    return F1.tolist()  # Returner F1-scorene som en liste

# Funksjon for å filtrere og lagre unike rader
def filter_unique_sentences(input_path, output_path):
    seen_entries = set()  # Sett for å lagre unike par
    total_lines = 0
    duplicate_count = 0
    inaudible_count = 0
    non_alpha_count = 0
    low_bertscore_count = 0
    
    references = []
    candidates = []
    batch_entries = []
    batch_size = 64  # Juster batch-størrelsen etter tilgjengelig minne

    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            total_lines += 1
            entry = json.loads(line)
            entry_tuple = (entry["nb"], entry["nn"])
            
            if entry_tuple in seen_entries:
                duplicate_count += 1
                continue

            seen_entries.add(entry_tuple)

            if "<INAUDIBLE>" in entry["nb"] or "<INAUDIBLE>" in entry["nn"]:
                inaudible_count += 1
                continue
            
            if is_non_alpha(entry["nb"]) or is_non_alpha(entry["nn"]):
                # if not is_non_alpha0(entry["nb"]) and not is_non_alpha0(entry["nn"]):
                #     print(f'{entry["nb"]}  |  {entry["nn"]}')
                non_alpha_count += 1
                continue
            
            if is_non_alpha3(entry["nb"]) or is_non_alpha3(entry["nn"]):
                print(f'{entry["nb"]}  |  {entry["nn"]}')

            # Legg til i batch
            references.append(entry["nb"])
            candidates.append(entry["nn"])
            batch_entries.append(entry)

            # # Beregn BERTScore når batchen er full
            # if len(references) >= batch_size:
            #     F1_scores = calculate_bertscore_batch(references, candidates)
            #     for i, F1_score in enumerate(F1_scores):
            #         if F1_score < 0.7:
            #             low_bertscore_count += 1
            #             continue
            #         json.dump(batch_entries[i], outfile, ensure_ascii=False)
            #         outfile.write('\n')
                
            #     # Nullstill batchen
            #     references.clear()
            #     candidates.clear()
            #     batch_entries.clear()

            if total_lines % 10000000 == 0:
                print(f"{input_path}: {total_lines} linjer behandlet")
        
        # # Beregn BERTScore for eventuell gjenværende data i batchen
        # if references:
        #     F1_scores = calculate_bertscore_batch(references, candidates)
        #     for i, F1_score in enumerate(F1_scores):
        #         if F1_score < 0.7:
        #             low_bertscore_count += 1
        #             continue
        #         json.dump(batch_entries[i], outfile, ensure_ascii=False)
        #         outfile.write('\n')

    # Print ut statistikk etter at filen er ferdig prosessert
    print(f"Fil: {input_path}")
    print(f"Totalt antall linjer: {total_lines}")
    print(f"Antall duplikater fjernet: {duplicate_count}")
    print(f"Antall linjer fjernet pga. '<INAUDIBLE>': {inaudible_count}")
    print(f"Antall linjer fjernet pga. 2 eller færre bokstavtegn: {non_alpha_count}")
    print(f"Antall linjer fjernet pga. lav BERTScore: {low_bertscore_count}")
    print(f"Antall linjer skrevet til output: {total_lines - duplicate_count - inaudible_count - non_alpha_count - low_bertscore_count}\n")

# Filstier for input og output
filenames = ["NNNB.jsonl", "NPSC.jsonl", "NTB-NPK.jsonl", "NBS2023.jsonl"]

input_dir = "C:/Users/oscar/oscar/myProjects/masterproject/dataprocessing"
output_dir = "C:/Users/oscar/oscar/myProjects/masterproject/dataset"

# Filtrer hver fil og lagre resultatet
for filename in filenames:
    input_file = f"{input_dir}/{filename}"
    output_file = f"{output_dir}/{filename}"
    filter_unique_sentences(input_file, output_file)

print("Filtrering fullført og unike rader lagret i mappen:", output_dir)
