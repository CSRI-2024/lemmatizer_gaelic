import os

def parse_mapping_line(line):
    """
    Parses a single line from the mapping file (e.g., "original -> lemma")
    and returns a tuple (original_word, lemma_word).
    Returns None if the line is empty or doesn't match the expected format.
    """
    line = line.strip()
    if not line:
        return None

    parts = line.split('->')
    if len(parts) == 2:
        original = parts[0].strip()
        lemma = parts[1].strip()
        if original and lemma: # Ensure both parts are non-empty
            return (original, lemma)
    return None

def read_mappings_from_file(filepath):
    """
    Reads a file containing word->lemma mappings and returns a dictionary.
    Keys are original words, values are their lemmas.
    """
    mappings = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parsed_entry = parse_mapping_line(line)
                if parsed_entry:
                    original_word, lemma_word = parsed_entry
                    mappings[original_word] = lemma_word
        return mappings
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred while reading {filepath}: {e}")
        return None

def compare_lemmatizer_outputs(file1_path, file2_path):
    """
    Compares word->lemma mappings from two files.
    Prints the number of differences and lists the differing entries.
    """
    print(f"Reading mappings from '{file1_path}'...")
    mappings1 = read_mappings_from_file(file1_path)
    if mappings1 is None:
        return

    print(f"Reading mappings from '{file2_path}'...")
    mappings2 = read_mappings_from_file(file2_path)
    if mappings2 is None:
        return

    differences_count = 0
    different_entries = []

    # Get all unique original words from both sets of mappings
    all_original_words = set(mappings1.keys()).union(set(mappings2.keys()))

    print("\nComparing mappings...")
    for original_word in sorted(list(all_original_words)):
        lemma1 = mappings1.get(original_word, "[NOT_IN_FILE_1]")
        lemma2 = mappings2.get(original_word, "[NOT_IN_FILE_2]")

        if lemma1 != lemma2:
            differences_count += 1
            different_entries.append(
                f"  Original: '{original_word}'\n"
                f"    File 1 Lemma: '{lemma1}'\n"
                f"    File 2 Lemma: '{lemma2}'"
            )

    print("\n--- Comparison Results ---")
    print(f"Total entries compared (unique original words): {len(all_original_words)}")
    print(f"Number of differing mappings: {differences_count}\n")

    if differences_count > 0:
        print("--- Details of Differing Mappings ---")
        for entry in different_entries:
            print(entry)
            print("-" * 30) # Separator for readability
    else:
        print("No differences found between the two mapping files!")

# --- Main execution ---
if __name__ == "__main__":
    # --- Configuration ---
    # IMPORTANT: Replace these with the actual paths to your files
    file1 = 'lemmatized_output.txt' # Updated to user's specified file name
    file2 = 'lemmatized_output_pos_aware_example.txt' # Updated to user's specified file name
    # -------------------

    # Create dummy files for demonstration if they don't exist
    if not os.path.exists(file1):
        print(f"Creating a dummy file for '{file1}'...")
        with open(file1, 'w', encoding='utf-8') as f:
            f.write("atharrachadh -> atharrach\n")
            f.write("daoine -> duine\n")
            f.write("eileanan -> eilean\n")
            f.write("chomharran -> comharradh\n")
            f.write("sgìrean -> sgìre\n")
            f.write("test_word_1 -> lemma_a\n")
            f.write("test_word_2 -> lemma_b\n")
            f.write("only_in_file_1 -> lemma_x\n")
        print(f"Dummy file '{file1}' created.")

    if not os.path.exists(file2):
        print(f"Creating a dummy file for '{file2}'...")
        with open(file2, 'w', encoding='utf-8') as f:
            f.write("atharrachadh -> atharraich\n") # This will differ
            f.write("daoine -> duine\n")
            f.write("eileanan -> eilean\n")
            f.write("chomharran -> comharradh_new\n") # This will differ
            f.write("sgìrean -> sgìre\n")
            f.write("test_word_1 -> lemma_a\n")
            f.write("test_word_3 -> lemma_c\n") # New entry
            f.write("only_in_file_2 -> lemma_y\n")
        print(f"Dummy file '{file2}' created.")

    compare_lemmatizer_outputs(file1, file2)
