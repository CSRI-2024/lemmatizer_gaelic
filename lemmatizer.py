# -*- coding: utf-8 -*-
"""
Created on Tue June 20, 2025

Author: Oskar Diyali
"""

# Import spaCy to build the NLP pipeline
import spacy
from spacy.language import Language
import json
import re


# PREPROCESSING FUNCTION
def preprocess_gaelic_word(word):
    """
    Applies preprocessing to a Scottish Gaelic word:
    - Replace acute accents with grave ones.
    - Remove emphatic suffixes (-sa, -se, -san, -ne).
    - Remove prosthetic consonants (t-, h-, n-).
    - Remove lenition marker (initial 'h' after the first consonant).
    """
    # 1. Replace acute accents (´) with grave accents (`)
    acute_to_grave = {
        'á': 'à', 'é': 'è', 'í': 'ì', 'ó': 'ò', 'ú': 'ù',
        'Á': 'À', 'É': 'È', 'Í': 'Ì', 'Ó': 'Ò', 'Ú': 'Ù'
    }
    word = ''.join(acute_to_grave.get(c, c) for c in word)

    # 2. Remove emphatic suffixes
    emphatic_suffixes = ['-sa', '-se', '-san', '-ne', 'sa', 'se', 'san', 'ne']
    for suffix in emphatic_suffixes:
        if word.endswith(suffix):
            word = re.sub(f"{suffix}$", "", word)
            break

    # 3. Remove prosthetic consonants
    if word.startswith(('t-', 'h-', 'n-')):
        word = word[2:]
    elif re.match(r'^[tnh][aeiouàèìòù]', word):
        word = word[1:]

    # 4. Remove lenition marker (second letter 'h')
    if len(word) > 2 and word[1] == 'h':
        word = word[0] + word[2:]

    return word


# LOAD IRREGULAR LEMMA DICTIONARY
with open("irregular_dict.json", "r", encoding="utf-8") as f:
    irregulars = json.load(f)

# DEFINE SUFFIX-BASED RULES
suffix_rules = [
    ("in", lambda w: w[:-2] + "an"),
    ("anan", lambda w: w[:-5]),
    ("ean", lambda w: w[:-3]),
]


# CREATE NLP PIPELINE
nlp = spacy.blank("xx")
nlp.max_length = 20_000_000


# DEFINE CUSTOM RULE-BASED LEMMATIZER
@Language.component("gaelic_lemmatizer")
def gaelic_lemmatizer(doc):
    for token in doc:
        raw_text = token.text.lower()
        text = preprocess_gaelic_word(raw_text)

        # Step 1: Irregular dictionary lookup
        if text in irregulars:
            token.lemma_ = irregulars[text]
            continue

        # Step 2: Suffix rule application
        for suffix, func in suffix_rules:
            if text.endswith(suffix):
                token.lemma_ = func(text)
                break
        else:
            token.lemma_ = text  # Keep as-is if no rules apply

    return doc


# REGISTER IN NLP PIPELINE
nlp.add_pipe("gaelic_lemmatizer", name="lemmatizer", last=True)


# LOAD INPUT DATA
input_file = "Latest_Corpus.txt"  # Format: "word source"
tokens = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        word = line.split(" ", 1)[0]  # Extract only the first word per line
        tokens.append(word.lower())


# PROCESS AND OUTPUT
text = " ".join(tokens)
doc = nlp(text)

# Print results to console
print("Token → Lemma")
print("-" * 20)
for token in doc:
    print(f"{token.text} → {token.lemma_}")

# Save to output file
with open("lemmatized_output.txt", "w", encoding="utf-8") as out:
    for token in doc:
        out.write(f"{token.text} -> {token.lemma_}\n")
