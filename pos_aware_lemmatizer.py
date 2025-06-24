# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24, 2025
Author: Oskar Diyali (based on your original lemmatizer and refined suffix rules)

This file contains the POS-aware lemmatizer component for Scottish Gaelic,
and includes example usage to demonstrate its functionality and output format,
processing words according to an external frequency list.
"""

import spacy
from spacy.language import Language
import json
import re # Import regex for more robust preprocessing


# --- PREPROCESSING FUNCTION ---
def preprocess_gaelic_word(word):
    """
    Applies preprocessing to a Scottish Gaelic word.

    Steps:
    1. Convert to lowercase and replace acute accents with grave ones.
    2. Remove hyphenated emphatic suffixes (-sa, -se, -san, -ne).
    3. Remove hyphenated prosthetic consonants (t-, h-, n-).

    Args:
        word (str): The input Scottish Gaelic word.

    Returns:
        str: The preprocessed word.
    """
    # 1. Convert to lowercase and replace acute accents with grave accents
    acute_to_grave = {
        'á': 'à', 'é': 'è', 'í': 'ì', 'ó': 'ò', 'ú': 'ù',
        'Á': 'À', 'É': 'È', 'Í': 'Ì', 'Ó': 'Ò', 'Ú': 'Ù',
        'ʼ': '`'
    }
    word = ''.join(acute_to_grave.get(c, c) for c in word.lower())

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

    # 4. Remove dh’ at the beginning
    if re.match(r"^dh[’']", word):
        word = word[3:]

    # 5. Remove lenition (second letter 'h')
    # This is a broad rule and might affect words where 'h' is not lenition
    # (e.g., 'thig' becomes 'tig').
    if len(word) > 2 and word[1] == 'h':
        word = word[0] + word[2:]


    return word


# --- LOAD IRREGULAR DICTIONARY ---
irregulars = {}
try:
    with open("irregular_dict.json", "r", encoding="utf-8") as f:
        irregulars = json.load(f)
except FileNotFoundError:
    print("Warning: irregular_dict.json not found. Lemmatizer will not use irregular forms.")
    irregulars = {}
except json.JSONDecodeError:
    print("Warning: Could not decode irregular_dict.json. Check its format.")
    irregulars = {}


# --- DEFINE SUFFIX RULE FUNCTIONS ---
def remove_suffix(word, suffix_len):
    """Helper to remove a suffix if word is long enough."""
    if len(word) > suffix_len:
        return word[:-suffix_len]
    return word

def change_in_to_an(word):
    """Specific rule for 'in' to 'an' transformation."""
    if len(word) > 2:
        return word[:-2] + "an"
    return word


# --- INITIALIZE A NEW NLP PIPELINE ---
nlp = spacy.blank("gd") # "gd" for Scottish Gaelic
nlp.max_length = 20_000_000


# --- CUSTOM POS-AWARE RULE-BASED LEMMATIZER COMPONENT ---
@Language.component("gaelic_lemmatizer_pos_aware")
def gaelic_lemmatizer_pos_aware(doc):
    """
    Custom rule-based lemmatizer for Scottish Gaelic, leveraging POS tags.

    Processing Order:
    1. Irregular dictionary lookup (highest priority).
    2. General preprocessing (accents, hyphenated affixes).
    3. POS-specific suffix rules.
    4. Fallback to preprocessed or original if no rule applies.
    5. Final length check.
    """
    for token in doc:
        raw_text = token.text.lower() # Start with lowercased raw text
        token.lemma_ = raw_text       # Initialize lemma with original text

        # Retrieve POS tags from the token
        # These are expected to be set by the calling script (e.g., test_lemmatizer_pos_aware.py)
        upos = token.pos_ # Universal POS tag (e.g., "NOUN", "VERB", "ADJ")
        xpos = token.tag_ # Fine-grained POS tag (e.g., "Nouns", "Verbs")

        # 1. Irregular dictionary lookup (HIGHEST PRIORITY)
        if raw_text in irregulars:
            token.lemma_ = irregulars[raw_text]
            continue # Skip all other rules for irregulars

        # 2. General Preprocessing
        preprocessed = preprocess_gaelic_word(raw_text)
        # If preprocessing makes it identical to an irregular form, use that
        if preprocessed in irregulars and irregulars[preprocessed] == preprocessed:
             token.lemma_ = preprocessed
             continue # Stop here if it became an irregular base form

        # 3. Irregular dictionary lookup (SECOND PRIORITY - after preprocessing)
        # If the word *becomes* an irregular after preprocessing, use its lemma and stop.
        if preprocessed in irregulars:
            token.lemma_ = irregulars[preprocessed]
            continue  # Skip remaining rules for this token

        # 4. POS-INFORMED SUFFIX-BASED LEMMATIZATION
        lemma_applied_by_rule = False # Flag to track if a specific rule was applied

        if upos == "NOUN":
            # Noun-specific rules (longest suffixes first)
            # Advisor Note: "sporan" example. If "sporan" should NOT be changed,
            # it must be added to irregular_dict.json like {"sporan": "sporan"}.
            if preprocessed.endswith("aichean"):
                token.lemma_ = remove_suffix(preprocessed, 7)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("annan"):
                token.lemma_ = remove_suffix(preprocessed, 5)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("ean"):
                token.lemma_ = remove_suffix(preprocessed, 3)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("in"): # Genitive singular (Advisor Note: change "in" to "an")
                token.lemma_ = change_in_to_an(preprocessed)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("an"): # Broad plural (Advisor Note: may conflict with base forms like "sporan")
                token.lemma_ = remove_suffix(preprocessed, 2)
                lemma_applied_by_rule = True
            # Add other noun rules here



        elif upos == "VERB":
            # Verb-specific rules (tenses, moods, verbal nouns, imperatives, passives)
            # Longest suffixes first

            if preprocessed.endswith("eachadh"):  # For verbs like stèidhich (often from -ich verbs)
                # Remove 'eachadh' and append 'ich' to get the base verb
                token.lemma_ = remove_suffix(preprocessed, 7) + "ich"
                lemma_applied_by_rule = True
            elif preprocessed.endswith("achadh"):  # For verbs like stèidhich (often from -ich verbs)
                # Remove 'eachadh' and append 'aich' to get the base verb
                token.lemma_ = remove_suffix(preprocessed, 6) + "aich"
                lemma_applied_by_rule = True
            elif preprocessed.endswith("eamaid"):  # Correctly indented to align with the 'if'
                token.lemma_ = remove_suffix(preprocessed, 6)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("teadh"):
                token.lemma_ = remove_suffix(preprocessed, 5)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("tadh"):
                token.lemma_ = remove_suffix(preprocessed, 4)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("eadh"):
                token.lemma_ = remove_suffix(preprocessed, 4)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("aidh"):
                token.lemma_ = remove_suffix(preprocessed, 4)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("aibh"):
                token.lemma_ = remove_suffix(preprocessed, 4)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("ainn"):
                token.lemma_ = remove_suffix(preprocessed, 4)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("eas"):
                token.lemma_ = remove_suffix(preprocessed, 3)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("ear"):
                token.lemma_ = remove_suffix(preprocessed, 3)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("tar"):
                token.lemma_ = remove_suffix(preprocessed, 3)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("idh"):
                token.lemma_ = remove_suffix(preprocessed, 3)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("ibh"):
                token.lemma_ = remove_suffix(preprocessed, 3)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("inn"):
                token.lemma_ = remove_suffix(preprocessed, 3)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("eam"):
                token.lemma_ = remove_suffix(preprocessed, 3)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("adh"):
                token.lemma_ = remove_suffix(preprocessed, 3)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("as"):
                token.lemma_ = remove_suffix(preprocessed, 2)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("ar"):
                token.lemma_ = remove_suffix(preprocessed, 2)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("am"):
                token.lemma_ = remove_suffix(preprocessed, 2)
                lemma_applied_by_rule = True
            # Past Participle (often adjective-like, but derived from verbs) (Advisor Note: covered)
            elif preprocessed.endswith("te"):
                token.lemma_ = remove_suffix(preprocessed, 2)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("ta"):
                token.lemma_ = remove_suffix(preprocessed, 2)
                lemma_applied_by_rule = True



        elif upos == "ADJ":
            # Adjective-specific rules
            # 'ach' suffix for adjectives: typically indicates a base adjective, so keep it.
            # (Advisor Note: Albannach -> Albannach correctly handled here)
            if preprocessed.endswith("ach") and not lemma_applied_by_rule:
                token.lemma_ = raw_text # Keep original as it's likely the base form
                lemma_applied_by_rule = True
            # Example: Slenderization (bige -> beag) - if not in irregulars (Advisor Note: specific example covered)
            elif raw_text == "bige":
                token.lemma_ = "beag"
                lemma_applied_by_rule = True
            # Add other adjective rules (e.g., comparative/superlative forms)
            elif preprocessed.endswith("ta"):
                token.lemma_ = remove_suffix(preprocessed, 2)
                lemma_applied_by_rule = True
            elif preprocessed.endswith("te"):
                token.lemma_ = remove_suffix(preprocessed, 2)
                lemma_applied_by_rule = True

        # 4. Fallback Logic: If no specific POS rule applied, and preprocessing changed the word, use preprocessed.
        # (Advisor Note: "if you already have a lemma, just stop" is effectively handled by this logic
        # and the lemma_applied_by_rule flag, ensuring specific rules take precedence.)
        if not lemma_applied_by_rule and preprocessed != raw_text:
            token.lemma_ = preprocessed

        # 5. Final Lemma Length Check: Revert if lemma is too short (1 char or less)
        # AND it's not an irregular form (which might be intentionally short).
        if len(token.lemma_) <= 1 and token.lemma_ != irregulars.get(raw_text):
            token.lemma_ = raw_text

    return doc


# --- REGISTER THE POS-AWARE LEMMATIZER COMPONENT ---
nlp.add_pipe("gaelic_lemmatizer_pos_aware", name="gaelic_lemmatizer_pos_aware", last=True)


# --- EXAMPLE USAGE AND OUTPUT GENERATION (Similar to old code, but frequency-aware) ---
if __name__ == "__main__":
    # This block runs only when pos_aware_lemmatizer.py is executed directly.
    # When imported by test_lemmatizer_pos_aware.py, this block is skipped.

    print("Running pos_aware_lemmatizer.py directly (example usage, frequency-aware).")

    # --- CONFIGURATION FOR DIRECT RUN ---
    pos_data_json_path = "top_500_gaelic_pos.json" # POS classified data
    frequency_list_path = "Top500Words.txt" # Words ordered by frequency
    output_file_name = "lemmatized_output_pos_aware_example.txt"

    # --- LOAD POS DATA INTO A LOOKUP DICTIONARY ---
    pos_lookup = {} # {word: {'upos': 'NOUN', 'xpos': 'Nouns'}, ...}
    try:
        with open(pos_data_json_path, "r", encoding="utf-8") as f:
            pos_data_list = json.load(f)
            for entry in pos_data_list:
                pos_lookup[entry['word'].lower()] = {'upos': entry['upos'], 'xpos': entry['xpos']}
    except FileNotFoundError:
        print(f"Error: POS data file '{pos_data_json_path}' not found. Please ensure it exists.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: Could not decode {pos_data_json_path}. Check its JSON format.")
        exit()

    # --- LOAD WORDS IN FREQUENCY ORDER ---
    words_to_process_ordered = []
    try:
        with open(frequency_list_path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower() # Read word, strip whitespace, convert to lower
                if word and word in pos_lookup: # Only process if it has POS data
                    words_to_process_ordered.append(word)
                elif word:
                    print(f"Warning: Word '{word}' from frequency list not found in POS data. Skipping.")
    except FileNotFoundError:
        print(f"Error: Frequency list file '{frequency_list_path}' not found. Please create it.")
        exit()

    # Initialize counters for different types of changes
    changed_by_irregular = 0
    changed_by_preprocessing = 0
    changed_by_suffix = 0
    unchanged = 0
    total_processed_count = 0 # To accurately count words actually processed

    print("Token  ->  Lemma   | POS ")
    print("-" * 40)

    with open(output_file_name, "w", encoding="utf-8") as out:
        for original_word in words_to_process_ordered:
            total_processed_count += 1
            pos_info = pos_lookup.get(original_word) # Get POS info

            if not pos_info: # Should not happen if filtered above, but for safety
                print(f"Error: No POS information for '{original_word}'. Skipping.")
                continue

            assigned_upos = pos_info['upos']
            assigned_xpos = pos_info['xpos']

            # Create a simple Doc object for the single word
            doc = nlp.make_doc(original_word)

            # Manually assign POS tags to the token in this Doc
            if doc:
                token = doc[0]
                token.pos_ = assigned_upos
                token.tag_ = assigned_xpos
            else:
                print(f"Warning: Could not create Doc for '{original_word}'. Skipping.")
                continue

            # Process the Doc through the pipeline
            # Passing the `doc` object (where POS is already set) ensures the custom
            # lemmatizer component has access to the POS information.
            processed_doc = nlp(doc)
            current_lemma = processed_doc[0].lemma_


            # Track changes for summary (similar to your original code's logic)
            if current_lemma == original_word.lower():
                unchanged += 1
            else:
                # Try to deduce the change source
                if original_word.lower() in irregulars and current_lemma == irregulars[original_word.lower()]:
                    changed_by_irregular += 1
                else:
                    preprocessed_val = preprocess_gaelic_word(original_word)
                    if current_lemma == preprocessed_val and preprocessed_val != original_word.lower():
                        changed_by_preprocessing += 1
                    else:
                        changed_by_suffix += 1

            print(f"{original_word:<6} ->  {current_lemma:<7} | {assigned_upos:<7} ")
            out.write(f"{original_word} -> {current_lemma}\n")

    # --- SUMMARY OUTPUT ---
    print("\nSummary of Lemmatization Changes (POS-Aware, Frequency-Ordered):")
    print("-" * 55)
    print(f"Words changed by irregular dictionary: {changed_by_irregular}")
    print(f"Words changed primarily by preprocessing: {changed_by_preprocessing}")
    print(f"Words changed primarily by suffix rules (POS-aware): {changed_by_suffix}")
    print(f"-------------------------------------------------------")
    print(f"Total words changed: {changed_by_irregular + changed_by_preprocessing + changed_by_suffix}")
    print(f"Total words unchanged: {unchanged}")
    print(f"Total words processed: {total_processed_count}")
    print(f"\nResults saved to: {output_file_name}")