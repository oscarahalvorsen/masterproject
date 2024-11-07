import json

# Funksjon for å filtrere og lagre unike rader
def filter_unique_sentences(input_path, output_path):
    seen_entries = set()  # Sett for å lagre unike par
    i = 0
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Les hver rad som et JSON-objekt
            entry = json.loads(line)
            # Lag en tuple av nb og nn som kan brukes som nøkkel for å sjekke duplikater
            entry_tuple = (entry["nb"], entry["nn"])
            
            # Sjekk om entry allerede er sett
            if entry_tuple not in seen_entries:
                # Legg entry til settet og skriv til output-fil hvis den er unik
                seen_entries.add(entry_tuple)
                json.dump(entry, outfile, ensure_ascii=False)  # Bruk ensure_ascii=False
                outfile.write('\n')
                
            # Status-oppdatering for hver 500. rad
            if i % 500 == 0:
                print(f"{input_path}: {i} linjer behandlet")
            i += 1

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
