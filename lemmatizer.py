# -*- coding: utf-8 -*-
"""
Created on Tue May 20, 2025
Author: Oskar Diyali
"""

# Import spaCy to build the NLP pipeline
import spacy
from spacy.language import Language
import json

# PREPROCESSING FUNCTION
def preprocess_gaelic_word(word):
    """
    Applies preprocessing to a Scottish Gaelic word:
    Step 1: Replace acute accents with grave ones.
    Step 2: Remove emphatic suffixes (-sa, -se, -san, -ne).
    Step 3: Remove prosthetic consonants (t-, h-, n-) with caution.
    Step 4: Remove lenition marker (if second letter is 'h').
    """

    # 1. Replace acute accents with grave accents
    acute_to_grave = {
        'á': 'à', 'é': 'è', 'í': 'ì', 'ó': 'ò', 'ú': 'ù',
        'Á': 'À', 'É': 'È', 'Í': 'Ì', 'Ó': 'Ò', 'Ú': 'Ù',
        'ʼ': '`'
    }
    word = ''.join(acute_to_grave.get(c, c) for c in word)

    # 2. Remove hyphenated emphatic suffixes only
    emphatic_suffixes = ['-sa', '-se', '-san', '-ne']
    for suffix in emphatic_suffixes:
        if word.endswith(suffix) and len(word) > len(suffix):
            word = word[:-len(suffix)]
            break

    # 3. Remove prosthetic consonants
    # Only strip prosthetics if in the form of t-, h-, or n- (e.g., t-each → each)
    if word.startswith(("t-", "h-", "n-")):
        word = word[2:]

    # 4. Remove lenition (second letter 'h')
    if len(word) > 2 and word[1] == 'h':
        word = word[0] + word[2:]

    return word


# LOAD IRREGULAR DICTIONARY
with open("irregular_dict.json", "r", encoding="utf-8") as f:
    irregulars = json.load(f)


# DEFINE SUFFIX RULES
suffix_rules = [
    ("aichean", lambda w: w[:-7]),  # Class 1a plural (e.g., notaichean → not)
    ("annan", lambda w: w[:-5]),    # Class 1a plural (alt) (e.g., lochannan → loch)
    ("anan", lambda w: w[:-5]),     # Long plural (e.g., taigheanan → taigh)
    ("ean", lambda w: w[:-3]),      # Class 1 plural, slender (e.g., taighean → taigh)
    ("ach", lambda w: w[:-3]),      # Removes suffix to reveal root noun
    ("adh", lambda w: w[:-3]),      # Forms verbal nouns or abstract nouns
    ("an", lambda w: w[:-2]),       # Class 1 plural, broad (e.g., làmhan → làmh)
    ("in", lambda w: w[:-2] + "an") # Genitive singular with slenderisation (e.g., eilein → eilean)
]


# INITIALIZE NLP PIPELINE
nlp = spacy.blank("xx")
nlp.max_length = 20_000_000


# CUSTOM RULE-BASED LEMMATIZER
@Language.component("gaelic_lemmatizer")
def gaelic_lemmatizer(doc):
    for token in doc:
        raw_text = token.text.lower()

        # STEP 1: Irregular dictionary lookup (PRIORITY)
        if raw_text in irregulars:
            token.lemma_ = irregulars[raw_text]
            continue

        # STEP 2: Preprocessing (accents, emphatics, prosthetics, lenition)
        preprocessed = preprocess_gaelic_word(raw_text)

        # STEP 3: Suffix-based lemmatization
        for suffix, func in suffix_rules:
            if preprocessed.endswith(suffix):
                lemma_candidate = func(preprocessed)
                # Avoid returning single-letter lemmas (unless from irregulars)
                if len(lemma_candidate) > 1:
                    token.lemma_ = lemma_candidate
                else:
                    token.lemma_ = preprocessed
                break
        else:
            # If no suffix matched, assign preprocessed form only if it's more than 1 character
            token.lemma_ = preprocessed if len(preprocessed) > 1 else raw_text

    return doc

# Register lemmatizer component
nlp.add_pipe("gaelic_lemmatizer", name="lemmatizer", last=True)


# LOAD INPUT DATA
input_file = "Top500Words.txt"  # Format: "word source"
tokens = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        word = line.strip().split(" ", 1)[0]
        if word:
            tokens.append(word.lower())

# Create document from input tokens
doc = nlp(" ".join(tokens))


# PROCESS AND OUTPUT RESULTS

changed_by_irregular = 0
changed_by_preprocessing = 0
changed_by_suffix = 0
unchanged = 0
total_changed = 0
total_unchanged = 0

print("Token → Lemma (excluding stop words)")
print("-" * 20)
with open("lemmatized_output.txt", "w", encoding="utf-8") as out:
    for token in doc:
        original = token.text
        lemma = token.lemma_

        if original in irregulars:
            changed_by_irregular += 1
        else:
            preprocessed = preprocess_gaelic_word(original)
            if preprocessed != original:
                changed_by_preprocessing += 1
            if lemma != preprocessed:
                changed_by_suffix += 1
            elif lemma == original:
                unchanged += 1

        if lemma != original:
            total_changed += 1
        else:
            total_unchanged += 1

        print(f"{original} → {lemma}")
        out.write(f"{original} -> {lemma}\n")


# SUMMARY OUTPUT
print("\nSummary of Lemmatization Changes:")
print("-" * 35)
print(f"Changed by irregular dictionary: {changed_by_irregular}")
print(f"Changed by preprocessing: {changed_by_preprocessing}")
print(f"Changed by suffix rules: {changed_by_suffix}")
print(f"Words changed: {total_changed}")
print(f"Words unchanged: {total_unchanged}")
print(f"\nHence, {changed_by_preprocessing+changed_by_irregular+changed_by_suffix} operations occurred, but only {total_changed} final results differed from the original.")

