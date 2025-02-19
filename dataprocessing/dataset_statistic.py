import json
import statistics
from collections import Counter

def compute_distribution(word_count_distribution, use_grouped_distribution):
    """Compute either a numerical or grouped word count distribution."""
    if use_grouped_distribution:
        return {
            "0-5_words": sum(word_count_distribution[i] for i in range(0, 6)),
            "6-10_words": sum(word_count_distribution[i] for i in range(6, 11)),
            "11-15_words": sum(word_count_distribution[i] for i in range(11, 16)),
            "16-20_words": sum(word_count_distribution[i] for i in range(16, 21)),
            "21_or_more_words": sum(count for word, count in word_count_distribution.items() if word >= 21),
        }
    return [
        word_count_distribution.get(i, 0)
        for i in range(max(word_count_distribution.keys(), default=0) + 1)
    ]

def compute_statistics(total_lines, word_counts, char_counts, word_count_distribution, use_grouped_distribution):
    """Compute and return formatted statistics from collected data."""
    if total_lines == 0:
        return None

    return {
        "Total lines": total_lines,
        "Average words": f"{sum(word_counts) / total_lines:.2f}",
        "Median words": f"{statistics.median(word_counts):.2f}",
        "Word count std dev": f"{statistics.stdev(word_counts) if total_lines > 1 else 0:.2f}",
        "Average chars": f"{sum(char_counts) / total_lines:.2f}",
        "Median chars": f"{statistics.median(char_counts):.2f}",
        "Char count std dev": f"{statistics.stdev(char_counts) if total_lines > 1 else 0:.2f}",
        "Word count distribution": compute_distribution(word_count_distribution, use_grouped_distribution)
    }

def print_statistics(name, stats):
    """Print the computed statistics."""
    if stats is None:
        print(f"No data for {name}.")
        return

    print(f"Statistics for {name}:")
    for key, value in stats.items():
        print(f"{key}: {value}")
    print()

def calculate_statistics(input_path, combined_stats=None, use_grouped_distribution=False):
    """Calculate word and character count statistics for a given dataset."""
    total_lines = 0
    word_counts, char_counts = [], []
    word_count_distribution = Counter()

    with open(input_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            total_lines += 1
            entry = json.loads(line)
            nb_text = entry["nb"]

            word_count = len(nb_text.split())
            char_count = len(nb_text)

            word_counts.append(word_count)
            char_counts.append(char_count)
            word_count_distribution[word_count] += 1

            if combined_stats is not None:
                combined_stats["total_lines"] += 1
                combined_stats["word_counts"].append(word_count)
                combined_stats["char_counts"].append(char_count)
                combined_stats["word_count_distribution"][word_count] += 1

    stats = compute_statistics(total_lines, word_counts, char_counts, word_count_distribution, use_grouped_distribution)
    print_statistics(input_path, stats)

def process_files(use_grouped_distribution):
    """Main function to process all datasets and compute statistics."""

    combined_stats = {
        "total_lines": 0,
        "word_counts": [],
        "char_counts": [],
        "word_count_distribution": Counter()
    }

    filenames = ["NTB-NPK.jsonl", "NNNB.jsonl", "NPSC.jsonl", "MAALFRID.jsonl", "NBS2023.jsonl"]
    input_dir = "C:/Users/oscar/oscar/myProjects/masterproject/dataset"

    for filename in filenames:
        input_file = f"{input_dir}/{filename}"
        calculate_statistics(input_file, combined_stats, use_grouped_distribution)

    combined_stats_summary = compute_statistics(
        combined_stats["total_lines"], 
        combined_stats["word_counts"], 
        combined_stats["char_counts"], 
        combined_stats["word_count_distribution"], 
        use_grouped_distribution
    )

    print_statistics("Combined Statistics for All Datasets", combined_stats_summary)
    print("Statistics calculation completed.")

if __name__ == "__main__":
    process_files(use_grouped_distribution = False)
