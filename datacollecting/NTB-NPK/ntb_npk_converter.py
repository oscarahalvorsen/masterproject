import csv
import json

# Filstier
input_file = r"C:\Users\Bruker\myProjects\masterproject\datacollecting\NTB-NPK\npk_2011_2022.tsv"
output_file = r"C:\Users\Bruker\myProjects\masterproject\dataprocessing\ntb-npk.jsonl"

# Les TSV-filen og lagre som JSONL
with open(input_file, "r", encoding="utf-8") as file, open(output_file, "w", encoding="utf-8") as output:
    reader = csv.reader(file, delimiter="\t")
    i=0
    for row in reader:
        # Hopp over linjer som ikke har riktig antall kolonner
        if len(row) < 3:
            continue
        # Opprett JSON-objekt og skriv det til filen som en linje
        json_obj = {"nb": row[1], "nn": row[2]}
        output.write(json.dumps(json_obj, ensure_ascii=False) + "\n")
        if (i%1000==0):
            print(i)
        i+=1

print(f"Lagring ferdig! Data lagret i {output_file}.")
