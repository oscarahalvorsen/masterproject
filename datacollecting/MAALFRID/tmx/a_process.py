import os
import json
import xml.etree.ElementTree as ET

def process_tmx_files():
    # Get the current working directory
    current_dir = os.getcwd()

    # Initialize a list to store all segments across files
    all_segments = []

    # Iterate through all files in the directory
    for file_name in os.listdir(current_dir):
        # Check if the file has a .tmx extension
        if file_name.endswith('.tmx'):
            file_path = os.path.join(current_dir, file_name)

            try:
                # Parse the TMX file
                tree = ET.parse(file_path)
                root = tree.getroot()

                print(f"Processing file: {file_name}")

                # Extract data from <tu> elements
                for tu in root.findall(".//tu"):
                    nb_seg = None
                    nn_seg = None

                    # Find the <tuv> elements
                    for tuv in tu.findall('tuv'):
                        lang = tuv.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
                        seg = tuv.find('seg')
                        if seg is not None:
                            if lang == 'nb':
                                nb_seg = seg.text
                            elif lang == 'nn':
                                nn_seg = seg.text

                    # Append to the result if both segments are found
                    if nb_seg and nn_seg:
                        all_segments.append({'nb': nb_seg, 'nn': nn_seg})

            except ET.ParseError as e:
                print(f"Error parsing {file_name}: {e}")
            except Exception as e:
                print(f"Unexpected error with {file_name}: {e}")

    # Write all extracted segments to a single file
    output_file_path = os.path.join(current_dir, "all_segments.jsonl")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for segment in all_segments:
            json.dump(segment, output_file, ensure_ascii=False)
            output_file.write('\n')

    print(f"All extracted segments written to {output_file_path}")

if __name__ == "__main__":
    process_tmx_files()
