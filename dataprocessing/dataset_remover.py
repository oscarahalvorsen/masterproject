import json
import re

# Funksjon for å sjekke om en streng kun inneholder ikke-bokstavtegn
def is_non_alpha(string):
    return not re.search(r'[a-zA-ZÆØÅæøå]', string)

# Funksjon for å filtrere og lagre unike rader
def filter_unique_sentences(input_path, output_path):
    seen_entries = set()  # Sett for å lagre unike par
    total_lines = 0
    duplicate_count = 0
    inaudible_count = 0
    non_alpha_count = 0
    
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            total_lines += 1
            
            # Les hver rad som et JSON-objekt
            entry = json.loads(line)
            entry_tuple = (entry["nb"], entry["nn"])
            
            # Sjekk om entry allerede er sett (duplikat)
            if entry_tuple in seen_entries:
                duplicate_count += 1
                continue
            
            # Legg entry til settet hvis det er unikt
            seen_entries.add(entry_tuple)
            
            # Sjekk etter "<INAUDIBLE>"-taggen i både 'nb' og 'nn'
            if "<INAUDIBLE>" in entry["nb"] or "<INAUDIBLE>" in entry["nn"]:
                inaudible_count += 1
                continue
            
            # Sjekk om enten 'nb' eller 'nn' kun inneholder ikke-bokstavtegn
            if is_non_alpha(entry["nb"]) or is_non_alpha(entry["nn"]):
                non_alpha_count += 1
                continue
            
            # Skriv til output-fil hvis linjen er unik, ikke inneholder "<INAUDIBLE>", og har bokstavtegn
            json.dump(entry, outfile, ensure_ascii=False)
            outfile.write('\n')

            # Status-oppdatering for hver 10 000. rad
            if total_lines % 10000 == 0:
                print(f"{input_path}: {total_lines} linjer behandlet")

    # Print ut statistikk etter at filen er ferdig prosessert
    print(f"Fil: {input_path}")
    print(f"Totalt antall linjer: {total_lines}")
    print(f"Antall duplikater fjernet: {duplicate_count}")
    print(f"Antall linjer fjernet pga. '<INAUDIBLE>': {inaudible_count}")
    print(f"Antall linjer fjernet pga. ikke-bokstavtegn: {non_alpha_count}")
    print(f"Antall linjer skrevet til output: {total_lines - duplicate_count - inaudible_count - non_alpha_count}\n")

# Filstier for input og output
filenames = ["NNNB.jsonl", "NPSC.jsonl", "NTB-NPK.jsonl"]

input_dir = "C:/Users/Bruker/myProjects/masterproject/dataprocessing"
output_dir = "C:/Users/Bruker/myProjects/masterproject/dataset"

# Filtrer hver fil og lagre resultatet
for filename in filenames:
    input_file = f"{input_dir}/{filename}"
    output_file = f"{output_dir}/{filename}"
    filter_unique_sentences(input_file, output_file)

print("Filtrering fullført og unike rader lagret i mappen:", output_dir)
