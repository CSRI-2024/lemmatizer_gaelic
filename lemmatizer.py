# Import spaCy's core library and Language class for defining custom components
import spacy
from spacy.language import Language

# Import json for loading the irregular dictionary
import json

# -------- LOAD IRREGULAR DICTIONARY --------
# Open the JSON file containing irregular word → lemma mappings
# "utf-8" encoding is used to handle special Gaelic characters (e.g., à, è, ò)
with open("irregular_dict.json", "r", encoding="utf-8") as f:
    irregulars = json.load(f)  # Load the contents into a Python dictionary

# -------- CREATE NLP PIPELINE --------
# Create a blank spaCy NLP pipeline
# "xx" is a generic language code for unsupported languages (like Scottish Gaelic)
nlp = spacy.blank("xx")

# -------- DEFINE CUSTOM LEMMATIZER COMPONENT --------
# Decorate this function as a spaCy pipeline component named "gaelic_lemmatizer"
@Language.component("gaelic_lemmatizer")
def gaelic_lemmatizer(doc):
    # Loop through each token (word) in the document
    for token in doc:
        text = token.text  # Get the actual word text

        # FIRST: Check if the word is an irregular form
        if text in irregulars:
            token.lemma_ = irregulars[text]  # Use its known lemma from the dictionary

        # SECOND: Apply rule-based suffix stripping if no dictionary match
        # These rules handle common Gaelic endings (plural, diminutive, etc.)

        # Remove "ean" (common plural ending) → e.g., "taighean" → "taigh"
        elif text.endswith("ean"):
            token.lemma_ = text[:-3]

        # Remove "an" (another common plural/inflection ending) → e.g., "leanaban" → "leanab"
        elif text.endswith("an"):
            token.lemma_ = text[:-2]

        # Replace "achan" (diminutive suffix) with "ach" → e.g., "cuimhneachan" → "cuimhneach"
        elif text.endswith("achan"):
            token.lemma_ = text[:-5] + "ach"

        # DEFAULT: If no rule or dictionary match, keep the word as-is
        else:
            token.lemma_ = text

    return doc  # Return the updated document

# -------- ADD LEMMATIZER TO THE PIPELINE --------
# Register the custom component as the last step in the NLP pipeline
nlp.add_pipe("gaelic_lemmatizer", name="lemmatizer", last=True)

# -------- LOAD TOKENS FROM FILE --------
# Open a test file with one word per line
with open("mock_tokens.txt", "r", encoding="utf-8") as f:
    # Strip whitespace and line breaks from each line and store as a list
    token_list = [line.strip() for line in f.readlines()]

# Combine tokens into a space-separated string (spaCy expects full text, not a token list)
text = " ".join(token_list)

# Process the text with the spaCy pipeline (includes your custom lemmatizer)
doc = nlp(text)

# -------- OUTPUT --------
# Print each token and its corresponding lemma
print("Token → Lemma")
print("-" * 20)
for token in doc:
    print(f"{token.text} → {token.lemma_}")
