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
    Applies preprocessing to a Scottish Gaelic word.

    Steps:
    1. Replace acute accents with grave ones.
    2. Remove emphatic suffixes (-sa, -se, -san, -ne) if hyphenated.
    3. Remove prosthetic consonants (t-, h-, n-) if hyphenated.
    4. Remove lenition marker (if second letter is 'h').

    Args:
        word (str): The input Scottish Gaelic word.

    Returns:
        str: The preprocessed word.
    """

    # 1. Replace acute accents with grave accents
    # Also handles a specific apostrophe-like character to grave accent
    acute_to_grave = {
        'á': 'à', 'é': 'è', 'í': 'ì', 'ó': 'ò', 'ú': 'ù',
        'Á': 'À', 'É': 'È', 'Í': 'Ì', 'Ó': 'Ò', 'Ú': 'Ù',
        'ʼ': '`'  # Specific character normalization
    }
    word = ''.join(acute_to_grave.get(c, c) for c in word)

    # 2. Remove hyphenated emphatic suffixes only
    emphatic_suffixes = ['-sa', '-se', '-san', '-ne']
    for suffix in emphatic_suffixes:
        if word.endswith(suffix) and len(word) > len(suffix):
            word = word[:-len(suffix)]
            break  # Assume only one emphatic suffix will be present

    # 3. Remove prosthetic consonants (t-, h-, n-) if followed by a hyphen
    # E.g., t-each -> each, h-uile -> uile, n-adharc -> adharc
    if word.startswith(("t-", "h-", "n-")):
        word = word[2:]

    # 4. Remove lenition (second letter 'h')
    # This is a broad rule and might affect words where 'h' is not lenition
    # (e.g., 'thig' becomes 'tig').
    if len(word) > 2 and word[1] == 'h':
        word = word[0] + word[2:]

    return word


# LOAD IRREGULAR DICTIONARY
# Ensure 'irregular_dict.json' exists in the same directory
try:
    with open("irregular_dict.json", "r", encoding="utf-8") as f:
        irregulars = json.load(f)
except FileNotFoundError:
    print("Error: irregular_dict.json not found. Please create this file.")
    irregulars = {}  # Initialize as empty dict to prevent further errors
except json.JSONDecodeError:
    print("Error: Could not decode irregular_dict.json. Check its format.")
    irregulars = {}

# DEFINE SUFFIX RULES
# Order matters: longer suffixes should come before shorter ones to prevent partial matches.

suffix_rules = [
    ("aichean", lambda w: w[:-7]),  # Class 1a plural (e.g., notaichean → not)
    ("annan", lambda w: w[:-5]),  # Class 1a plural (alt) (e.g., lochannan → loch)
    ("anan", lambda w: w[:-5]),  # Long plural (e.g., taigheanan → taigh)
    ("ean", lambda w: w[:-3]),  # Class 1 plural, slender (e.g., taighean → taigh)
    ("ach", lambda w: w[:-3]),  # Adjectival/Nominal suffix (e.g., bòidheach -> bòidh)
    ("adh", lambda w: w[:-3]),  # Verbal noun or abstract noun suffix (e.g., obair-chòcaireachd -> obair-chòcaireach)
    ("an", lambda w: w[:-2]),  # Class 1 plural, broad (e.g., làmhan → làmh)
    ("in", lambda w: w[:-2] + "an")  # Genitive singular with slenderisation (e.g., eilein → eilean)
]

# INITIALIZE NLP PIPELINE
nlp = spacy.blank("xx")  # "xx" is for a blank multi-language pipeline
nlp.max_length = 20_000_000  # Increase max_length for potentially large inputs


# CUSTOM RULE-BASED LEMMATIZER
@Language.component("gaelic_lemmatizer")
def gaelic_lemmatizer(doc):
    """
    Custom rule-based lemmatizer for Scottish Gaelic.
    Applies irregular dictionary lookup, preprocessing, and suffix-based rules.
    """
    for token in doc:
        raw_text = token.text.lower()
        token.lemma_ = raw_text  # Default lemma is the original token text

        # STEP 1: Irregular dictionary lookup (PRIORITY)
        if raw_text in irregulars:
            token.lemma_ = irregulars[raw_text]
            continue  # Move to the next token, as irregulars take precedence

        # STEP 2: Preprocessing (accents, emphatics, prosthetics, lenition)
        preprocessed = preprocess_gaelic_word(raw_text)

        # STEP 3: Suffix-based lemmatization
        # Only apply suffix rules if preprocessing has not already made it a known irregular or a very short word
        lemma_found_by_suffix = False
        if preprocessed == raw_text or len(
                preprocessed) > 1:  # Only apply if preprocessing had no effect or resulted in a valid length
            for suffix, func in suffix_rules:
                if preprocessed.endswith(suffix):
                    lemma_candidate = func(preprocessed)
                    # Avoid returning single-letter lemmas from suffix rules
                    if len(lemma_candidate) > 1:
                        token.lemma_ = lemma_candidate
                        lemma_found_by_suffix = True
                        break  # Apply the first matching suffix rule and stop

            # If no suffix matched, and preprocessing changed the word, use the preprocessed form
            if not lemma_found_by_suffix and preprocessed != raw_text:
                token.lemma_ = preprocessed
            # If no suffix matched and preprocessing didn't change it, lemma remains raw_text (default)
            # This handles cases where a word doesn't fit any rule and isn't irregular
            # The initial default `token.lemma_ = raw_text` covers this.

        # Final check: if lemma somehow became single char, revert to original unless it's from irregulars
        if len(token.lemma_) <= 1 and token.lemma_ != irregulars.get(raw_text):
            token.lemma_ = raw_text  # Revert to original if lemma is too short and not from irregulars

    return doc


# Register lemmatizer component
# It's set to 'last=True' to ensure it runs after default spaCy components (if any were added)
nlp.add_pipe("gaelic_lemmatizer", name="gaelic_lemmatizer", last=True)

# LOAD INPUT DATA
input_file = "Top500Words.txt"  # Format: "word source"
tokens_to_process = []

try:
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip().split(" ", 1)[0]  # Extract the word before the first space
            if word:
                tokens_to_process.append(word.lower())
except FileNotFoundError:
    print(f"Error: Input file '{input_file}' not found. Please ensure it exists.")
    exit()  # Exit if input file is critical and not found

# Create document from input tokens
# Joining tokens with space to create a single string for spaCy Doc
doc = nlp(" ".join(tokens_to_process))

# PROCESS AND OUTPUT RESULTS
# Initialize counters for different types of changes
changed_by_irregular = 0
changed_by_preprocessing = 0
changed_by_suffix = 0
unchanged = 0
total_changed = 0
total_unchanged = 0

print("Token → Lemma (excluding stop words)")
print("-" * 20)

output_file_name = "lemmatized_output.txt"
with open(output_file_name, "w", encoding="utf-8") as out:
    for token in doc:
        original = token.text
        lemma = token.lemma_

        # Determine the primary reason for change for statistical purposes
        if lemma == original:
            unchanged += 1
        else:
            total_changed += 1  # Count any change as a total_changed
            if original in irregulars and lemma == irregulars[original]:
                changed_by_irregular += 1
            else:
                # Check what preprocessing would have done
                preprocessed_version = preprocess_gaelic_word(original)
                if lemma == preprocessed_version and preprocessed_version != original:
                    changed_by_preprocessing += 1
                elif lemma != preprocessed_version:  # If lemma is different from preprocessed, it's due to suffix or other rule
                    changed_by_suffix += 1
                # Note: A word could be preprocessed AND then a suffix applied.
                # This counting logic prioritizes irregulars, then preprocessing, then suffix.
                # If a word was preprocessed, and THEN a suffix rule changed it further,
                # it's counted under suffix_changed.

        print(f"{original} → {lemma}")
        out.write(f"{original} -> {lemma}\n")

total_unchanged = len(tokens_to_process) - total_changed

# SUMMARY OUTPUT
print("\nSummary of Lemmatization Changes:")
print("-" * 35)
print(f"Words changed by irregular dictionary: {changed_by_irregular}")
print(f"Words changed primarily by preprocessing: {changed_by_preprocessing}")
print(f"Words changed primarily by suffix rules: {changed_by_suffix}")
print(f"-----------------------------------")
print(f"Total words changed: {total_changed}")
print(f"Total words unchanged: {total_unchanged}")
print(f"Total words processed: {len(tokens_to_process)}")

print(f"\nNote: The sum of 'changed by' categories may not equal 'Total words changed'")
print(f"if a single word underwent multiple transformations (e.g., preprocessed then suffixed),")
print(f"as the counters attempt to categorize the primary reason for the *final* lemma change.")