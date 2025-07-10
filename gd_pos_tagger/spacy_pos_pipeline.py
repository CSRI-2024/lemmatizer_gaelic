import spacy
import csv
from tagger_module import create_tagger_pipe

# Initialize spaCy pipeline
nlp = spacy.blank("gd")
nlp.add_pipe("pos_tagger_pipe")

# Load tag mapping from CSV
tag_to_pos = {}
with open("Tags_Sheet.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tag_to_pos[row["Tag"].strip()] = row["SimplifiedTags"].strip()

# Function to simplify fine-grained tag
def get_simplified_pos(fine_tag):
    base = fine_tag.split("-")[0]
    return tag_to_pos.get(base, "UNKNOWN")

# Load the tokenized corpus (one word per line)
with open("../Top500Words.txt", "r", encoding="utf-8") as f:
    words = [line.strip() for line in f if line.strip()]

# Print header
print("Word".ljust(10) + "POS")

# Process each token individually
for word in words:
    doc = nlp(word)  # Each word is treated as its own Doc
    token = doc[0]   # Single-token doc
    fine_tag = token.tag_
    simplified = get_simplified_pos(fine_tag)
    print(word.ljust(10) + simplified)
