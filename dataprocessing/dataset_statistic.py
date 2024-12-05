import json
import re
import statistics
from collections import Counter

def calculate_statistics(input_path):
    total_lines = 0
    word_counts = []
    char_counts = []
    word_count_distribution = Counter()

    with open(input_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            total_lines += 1
            entry = json.loads(line)

            # Calculate word and character counts
            nb_text = entry["nb"]
            word_count = len(nb_text.split())
            char_count = len(nb_text)

            word_counts.append(word_count)
            char_counts.append(char_count)

            # Update word count distribution
            word_count_distribution[word_count] += 1

            # Print progress for every 10,000 lines
            if total_lines % 10_000 == 0:
                print(f"{input_path}: {total_lines} lines processed")

    # Calculate statistics
    avg_words = sum(word_counts) / total_lines
    median_words = statistics.median(word_counts)
    avg_chars = sum(char_counts) / total_lines
    median_chars = statistics.median(char_counts)

    # Aggregate counts for word ranges
    distribution = {
        "1_word": word_count_distribution[1],
        "2_words": word_count_distribution[2],
        "3_words": word_count_distribution[3],
        "4_words": word_count_distribution[4],
        "5_words": word_count_distribution[5],
        "6-9_words": sum(word_count_distribution[i] for i in range(6, 10)),
        "10-14_words": sum(word_count_distribution[i] for i in range(10, 15)),
        "15-19_words": sum(word_count_distribution[i] for i in range(15, 20)),
        "20_or_more_words": sum(count for word, count in word_count_distribution.items() if word >= 20),
    }

    # Print statistics for this dataset
    print(f"\nStatistics for {input_path}:")
    print(f"Total lines: {total_lines}")
    print(f"Average number of words: {avg_words:.2f}")
    print(f"Median number of words: {median_words}")
    print(f"Average number of characters: {avg_chars:.2f}")
    print(f"Median number of characters: {median_chars}")
    print(f"Word count distribution: {distribution}\n")

# File paths for input
filenames = ["NNNB.jsonl", "NPSC.jsonl", "NTB-NPK.jsonl", "NBS2023.jsonl"]

input_dir = "C:/Users/oscar/oscar/myProjects/masterproject/dataprocessing"

# Process each file and calculate statistics
for filename in filenames:
    input_file = f"{input_dir}/{filename}"
    calculate_statistics(input_file)

print("Statistics calculation completed.")
