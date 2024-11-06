import json

# Funksjon for å filtrere og lagre en fil
def filter_identical_sentences(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        i=0
        for line in infile:
            # Les hver rad som et JSON-objekt
            entry = json.loads(line)
            # Sjekk om nb og nn er identiske
            if entry["nb"] != entry["nn"]:
                # Skriv til output-fil hvis de ikke er identiske
                json.dump(entry, outfile)
                outfile.write('\n')
            if (i%500==0):
                print(f"{input_path}: {i}")
            i+=1

# Filstier for input og output
filenames = ["NNNB.jsonl","NPSC.jsonl","NTB-NPK.jsonl"]

input_dir = "C:/Users/Bruker/myProjects/masterproject/dataprocessing"
output_dir = "C:/Users/Bruker/myProjects/masterproject/dataset"

# Filtrer hver fil og lagre resultatet
for filename in filenames:
    input_file = f"{input_dir}/{filename.split('/')[-1]}"
    output_file = f"{output_dir}/{filename.split('/')[-1]}"
    filter_identical_sentences(input_file, output_file)

print("Filtrering fullført og lagret i mappen:", output_dir)
