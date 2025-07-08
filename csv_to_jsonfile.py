import csv
import json

# --- CONFIGURATION ---
csv_file_path = 'POS_Gaelic_Test.csv'  # <--- IMPORTANT: UPDATE THIS PATH
json_output_path = 'top_500_gaelic_pos.json'

# Define your exact POS headers. Order matters here if your CSV columns match this order.
POS_HEADERS_IN_CSV = ["Nouns", "Verbs", "Adjectives", "Preposition", "Pronoun", "Others"]

# Mapping your custom headers to Universal POS (UPOS) tags
# These are the standard tags used by spaCy (token.pos_)
# See: https://universaldependencies.org/u/pos/all.html
UPOS_MAPPING = {
    "Nouns": "NOUN",
    "Verbs": "VERB",
    "Adjectives": "ADJ",
    "Preposition": "ADP",  # Adposition (for prepositions/postpositions)
    "Pronoun": "PRON",
    "Others": "X"  # For miscellaneous/unknown
}

# SCRIPT TO PROCESS CSV
processed_words_data = []

try:
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        # Read the header row to confirm column indices
        actual_headers = next(reader)

        # Verify that your expected headers match the actual headers in the CSV
        if not all(h in actual_headers for h in POS_HEADERS_IN_CSV):
            print(f"Warning: CSV headers do not exactly match expected headers. "
                  f"Expected: {POS_HEADERS_IN_CSV}, Found: {actual_headers}")
            print("Please ensure your POS_HEADERS_IN_CSV list matches your CSV's first row exactly.")
            # You might want to exit or adjust POS_HEADERS_IN_CSV here

        # Get the column index for each header
        header_indices = {header: actual_headers.index(header) for header in POS_HEADERS_IN_CSV}

        # Transpose logic is tricky with this format, better to iterate by column.
        # Find the maximum number of rows (words) in any column to ensure we read all data
        f.seek(0)  # Reset file pointer to beginning
        next(reader)  # Skip header again
        num_rows_in_data = sum(1 for row in reader)  # Count data rows

        # Now, re-read the file to process column by column
        f.seek(0)
        reader = csv.reader(f)
        next(reader)  # Skip header

        # Store all data in columns first
        columns_data = {header: [] for header in POS_HEADERS_IN_CSV}
        for row in reader:
            for header_name in POS_HEADERS_IN_CSV:
                idx = header_indices[header_name]
                if idx < len(row):  # Ensure row has this column
                    word = row[idx].strip()
                    if word:  # Only add if the cell is not empty
                        columns_data[header_name].append(word)

        # Now, iterate through the collected column data to build the final list
        for header, words_list in columns_data.items():
            upos = UPOS_MAPPING.get(header, "X")  # Get UPOS from mapping, default to X
            xpos = header  # Use your original header as the fine-grained XPOS

            for word in words_list:
                processed_words_data.append({
                    'word': word,
                    'upos': upos,
                    'xpos': xpos
                })

except FileNotFoundError:
    print(f"Error: The CSV file '{csv_file_path}' was not found.")
    exit()
except Exception as e:
    print(f"An error occurred during CSV processing: {e}")
    exit()

# Save the processed data to a JSON file
with open(json_output_path, 'w', encoding='utf-8') as f:
    json.dump(processed_words_data, f, indent=2, ensure_ascii=False)

print(f"Successfully converted '{csv_file_path}' to '{json_output_path}'.")
print(f"Total words with assigned POS: {len(processed_words_data)}")