import json
import os

# Dictionary to hold configurations for each dataset
configurations = {
    "eval": {
        "base_path": r"C:\Users\Bruker\myProjects\masterproject\datacollecting\NPSC\eval",
        "input_files": [
            "20170209.json", "20180109.json", "20180201.json", "20180307.json", "20180611.json"
        ],
        "output_file": r"C:\Users\Bruker\myProjects\masterproject\datacollecting\NPSC\NPSC-eval.json"
    },
    "test": {
        "base_path": r"C:\Users\Bruker\myProjects\masterproject\datacollecting\NPSC\test",
        "input_files": [
            "20170207.json", "20171122.json", "20171219.json", "20180530.json"
        ],
        "output_file": r"C:\Users\Bruker\myProjects\masterproject\datacollecting\NPSC\NPSC-test.json"
    },
    "train": {
        "base_path": r"C:\Users\Bruker\myProjects\masterproject\datacollecting\NPSC\train",
        "input_files": [
            "20170110.json", "20170208.json", "20170215.json", "20170216.json", "20170222.json",
            "20170314.json", "20170322.json", "20170323.json", "20170403.json", "20170405.json",
            "20170419.json", "20170426.json", "20170503.json", "20170510.json", "20170516.json",
            "20170613.json", "20170615.json", "20171007.json", "20171012.json", "20171018.json",
            "20171024.json", "20171122.json", "20171208.json", "20171211.json", "20171213.json",
            "20171219.json", "20180316.json", "20180321.json", "20180404.json", "20180410.json",
            "20180411.json", "20180530.json", "20180601.json", "20180613.json", "20180615.json"
        ],
        "output_file": r"C:\Users\Bruker\myProjects\masterproject\datacollecting\NPSC\NPSC-train.json"
    }
}

# Function to process a configuration
def process_configuration(config_name, config):
    base_path = config["base_path"]
    input_files = [os.path.join(base_path, file) for file in config["input_files"]]
    output_file = config["output_file"]

    print(f"Processing configuration: {config_name}")
    
    # Open the output file for writing
    with open(output_file, "w", encoding="utf-8") as outfile:
        # Process each input file
        for input_file in input_files:
            with open(input_file, "r", encoding="utf-8") as infile:
                for line in infile:
                    # Parse each JSON line
                    data = json.loads(line.strip())
                    
                    # Check and map based on the sentence_language_code
                    if data["sentence_language_code"] == "nb-NO":
                        output_data = {"nb": data["sentence_text"], "nn": data["transsentence_text"]}
                    elif data["sentence_language_code"] == "nn-NO":
                        output_data = {"nb": data["transsentence_text"], "nn": data["sentence_text"]}
                    else:
                        # Print error and skip this line
                        print(f"Error: Unrecognized language code '{data['sentence_language_code']}' in sentence ID {data['sentence_id']}. Line skipped.")
                        continue
                    
                    # Write the processed line to the output file
                    outfile.write(json.dumps(output_data, ensure_ascii=False) + "\n")

    print(f"Processing complete! Data saved in {output_file}.\n")

# Run the script for each configuration
for config_name, config in configurations.items():
    process_configuration(config_name, config)
