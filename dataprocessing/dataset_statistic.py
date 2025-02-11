import json
import statistics
from collections import Counter

def calculate_statistics(input_path, combined_stats=None):
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

            # Update combined statistics if provided
            if combined_stats is not None:
                combined_stats['total_lines'] += 1
                combined_stats['word_counts'].append(word_count)
                combined_stats['char_counts'].append(char_count)
                combined_stats['word_count_distribution'][word_count] += 1

    # Calculate statistics
    avg_words = sum(word_counts) / total_lines
    median_words = statistics.median(word_counts)
    std_dev_words = statistics.stdev(word_counts)
    
    avg_chars = sum(char_counts) / total_lines
    median_chars = statistics.median(char_counts)
    std_dev_chars = statistics.stdev(char_counts)

    # Aggregate counts for word ranges
    distribution = {
        "0-5_words": sum(word_count_distribution[i] for i in range(0, 6)),
        "6-10_words": sum(word_count_distribution[i] for i in range(6, 11)),
        "11-15_words": sum(word_count_distribution[i] for i in range(11, 16)),
        "16-20_words": sum(word_count_distribution[i] for i in range(16, 21)),
        "21_or_more_words": sum(count for word, count in word_count_distribution.items() if word >= 21),
    }

    # distribution = [
    #     word_count_distribution.get(i, 0)
    #     for i in range(max(word_count_distribution.keys()) + 1)
    # ]

    # Print statistics for this dataset
    print(f"Statistics for {input_path}:")
    print(f"Total lines: {total_lines}")
    print(f"Average number of words: {avg_words:.2f}")
    print(f"Median number of words: {median_words}")
    print(f"Standard deviation of word count: {std_dev_words:.2f}")
    print(f"Average number of characters: {avg_chars:.2f}")
    print(f"Median number of characters: {median_chars}")
    print(f"Standard deviation of char count: {std_dev_chars:.2f}")
    print(f"Word count distribution: {distribution}\n")

# Initialize combined statistics
combined_stats = {
    'total_lines': 0,
    'word_counts': [],
    'char_counts': [],
    'word_count_distribution': Counter()
}

# File paths for input
filenames = ["NTB-NPK.jsonl", "NNNB.jsonl", "NPSC.jsonl", "NBS2023.jsonl"]

input_dir = "C:/Users/oscar/oscar/myProjects/masterproject/dataset"

# Process each file and calculate statistics
for filename in filenames:
    input_file = f"{input_dir}/{filename}"
    calculate_statistics(input_file, combined_stats)

# Calculate overall combined statistics
total_lines = combined_stats['total_lines']
avg_words = sum(combined_stats['word_counts']) / total_lines
median_words = statistics.median(combined_stats['word_counts'])
std_dev_words = statistics.stdev(combined_stats['word_counts'])

avg_chars = sum(combined_stats['char_counts']) / total_lines
median_chars = statistics.median(combined_stats['char_counts'])
std_dev_chars = statistics.stdev(combined_stats['char_counts'])

combined_distribution = {
    "0-5_words": sum(combined_stats['word_count_distribution'][i] for i in range(0, 6)),
    "6-10_words": sum(combined_stats['word_count_distribution'][i] for i in range(6, 11)),
    "11-15_words": sum(combined_stats['word_count_distribution'][i] for i in range(11, 16)),
    "16-20_words": sum(combined_stats['word_count_distribution'][i] for i in range(16, 21)),
    "21_or_more_words": sum(count for word, count in combined_stats['word_count_distribution'].items() if word >= 21),
}

# combined_distribution = [
#     combined_stats['word_count_distribution'].get(i, 0)
#     for i in range(max(combined_stats['word_count_distribution'].keys()) + 1)
# ]

# Print overall combined statistics
print("Combined Statistics for All Datasets:")
print(f"Total lines: {total_lines}")
print(f"Average number of words: {avg_words:.2f}")
print(f"Median number of words: {median_words}")
print(f"Standard deviation of word count: {std_dev_words:.2f}")
print(f"Average number of characters: {avg_chars:.2f}")
print(f"Median number of characters: {median_chars}")
print(f"Standard deviation of char count: {std_dev_chars:.2f}")
print(f"Word count distribution: {combined_distribution}\n")

print("Statistics calculation completed.")
