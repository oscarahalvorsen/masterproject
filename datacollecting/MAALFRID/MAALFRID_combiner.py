import json
import xml.etree.ElementTree as ET
from pathlib import Path

def process_tmx_files():
    """Process all TMX files in the current directory and save extracted segments."""
    current_dir = Path(__file__).resolve().parent / "tmx"
    output_file_path = Path("dataprocessing/MAALFRID.jsonl")

    all_segments = []
    for file_path in current_dir.glob("*.tmx"):
        print(f"Processing file: {file_path.name}")
        all_segments.extend(extract_segments_from_tmx(file_path))

    # Write all extracted segments to a JSONL file
    output_file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    with output_file_path.open('w', encoding='utf-8') as output_file:
        for segment in all_segments:
            json.dump(segment, output_file, ensure_ascii=False)
            output_file.write('\n')

    print(f"All extracted segments written to {output_file_path}")

def extract_segments_from_tmx(file_path):
    """Extract translation segments from a TMX file."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        segments = []
        for tu in root.findall(".//tu"):
            nb_seg, nn_seg = None, None

            for tuv in tu.findall('tuv'):
                lang = tuv.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
                seg = tuv.find('seg')
                if seg is not None:
                    if lang == 'nb':
                        nb_seg = seg.text
                    elif lang == 'nn':
                        nn_seg = seg.text

            if nb_seg and nn_seg:
                segments.append({'nb': nb_seg, 'nn': nn_seg})

        return segments

    except ET.ParseError as e:
        print(f"Error parsing {file_path.name}: {e}")
    except Exception as e:
        print(f"Unexpected error with {file_path.name}: {e}")
    return []

if __name__ == "__main__":
    process_tmx_files()
