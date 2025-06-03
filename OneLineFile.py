# Save this as extract_first_words.py or run directly in your environment

input_file = "Latest_Corpus.txt"
output_file = "OneLineFile.txt"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        line = line.strip()
        if line:
            first_word = line.split()[0]
            outfile.write(first_word + "\n")

print("✅ First words have been written to:", output_file)
