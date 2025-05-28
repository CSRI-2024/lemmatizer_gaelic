# -*- coding: utf-8 -*-
"""
Created on Tue June 20, 2025

Author: Oskar Diyali
"""

# Import spaCy to build the NLP pipeline
import spacy
from spacy.language import Language

# Import JSON to read the dictionary of irregular lemmas
import json

# LOAD IRREGULAR LEMMA DICTIONARY
# This JSON file contains mappings of irregular forms to their lemmas.
# Example: "bha" → "bi", "daoine" → "duine"
with open("irregular_dict.json", "r", encoding="utf-8") as f:
    irregulars = json.load(f)

# DEFINE SUFFIX-BASED RULES
# These rules apply to words that follow regular morphological patterns.
# Each rule checks for a suffix and transforms the word to its likely lemma.
# Only a few carefully tested rules are used to avoid over-stemming.
suffix_rules = [
    # Genitive singular → restore base form
    # e.g., "eilein" → "eilean"
    ("in", lambda w: w[:-2] + "an"),

    # Plural long form → strip to base
    # e.g., "eileanan" → "eilean"
    ("anan", lambda w: w[:-5]),

    # Regular plural suffix
    # e.g., "balg-ean" → "balg"
    ("ean", lambda w: w[:-3]),
]

# CREATE NLP PIPELINE
# Since spaCy does not support Scottish Gaelic directly,
# we use a blank multilingual ("xx") model.
nlp = spacy.blank("xx")
nlp.max_length = 20_000_000  # Allow large inputs


# DEFINE CUSTOM RULE-BASED LEMMATIZER
# This component replaces spaCy’s default lemmatizer.
@Language.component("gaelic_lemmatizer")
def gaelic_lemmatizer(doc):
    for token in doc:
        text = token.text.lower()  # Normalize token to lowercase

        # Step 1: Check irregular dictionary
        if text in irregulars:
            token.lemma_ = irregulars[text]
            continue

        # Step 2: Apply first matching suffix rule
        for suffix, func in suffix_rules:
            if text.endswith(suffix):
                token.lemma_ = func(text)
                break
        else:
            token.lemma_ = text  # Default to unchanged word

    return doc


# REGISTER CUSTOM LEMMATIZER IN PIPELINE
nlp.add_pipe("gaelic_lemmatizer", name="lemmatizer", last=True)

# LOAD TOKENS FROM CORPUS FILE (only first word per line)
input_file = "Latest_Corpus.txt"  # Contains "word source" lines
tokens = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        word = line.split(" ", 1)[0]  # Get only the first word
        tokens.append(word.lower())

# CONVERT TOKEN LIST TO TEXT FOR spaCy
text = " ".join(tokens)
doc = nlp(text)

# PRINT TO CONSOLE
print("Token → Lemma")
print("-" * 20)
for token in doc:
    print(f"{token.text} → {token.lemma_}")

# SAVE TO FILE
with open("lemmatized_output.txt", "w", encoding="utf-8") as out:
    for token in doc:
        out.write(f"{token.text} -> {token.lemma_}\n")
