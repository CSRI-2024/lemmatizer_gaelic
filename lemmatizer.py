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
nlp.max_length = 10_000_000  # Allow large inputs

# DEFINE CUSTOM RULE-BASED LEMMATIZER
# This component replaces spaCy’s default lemmatizer.
# It follows a two-step process:
# (1) If the word is in the irregular dictionary, use that mapping.
# (2) If not, try to apply one of the suffix rules.
@Language.component("gaelic_lemmatizer")
def gaelic_lemmatizer(doc):
    for token in doc:
        text = token.text.lower()  # Normalize token to lowercase

        # Step 1: Check irregular dictionary
        if text in irregulars:
            token.lemma_ = irregulars[text]
            continue  # Skip to next token

        # Step 2: Apply the first matching suffix rule
        for suffix, func in suffix_rules:
            if text.endswith(suffix):
                token.lemma_ = func(text)
                break  # Stop checking rules after first match
        else:
            # Step 3: If no rule applies, keep the word as its own lemma
            token.lemma_ = text

    return doc  # Return the processed document

# REGISTER CUSTOM LEMMATIZER IN PIPELINE
# Add the custom lemmatizer to the end of the spaCy pipeline.
# It will run after tokenization.
nlp.add_pipe("gaelic_lemmatizer", name="lemmatizer", last=True)

# LOAD TOKENS FROM FILE
# Read from your cleaned corpus (one token per line).
# This ensures consistency with your frequency analysis step.
input_file = "CleanedCorpus.txt"
tokens = [line.strip().lower() for line in open(input_file, "r", encoding="utf-8") if line.strip()]

# CONVERT TOKEN LIST TO TEXT FOR spaCy PROCESSING
# spaCy expects a single string as input.
# We join the tokens into a space-separated string so spaCy can tokenize and lemmatize it.
text = " ".join(tokens)
doc = nlp(text)  # Run the NLP pipeline

# PRINT LEMMATIZATION RESULTS TO CONSOLE
print("Token → Lemma")
print("-" * 20)
for token in doc:
    print(f"{token.text} → {token.lemma_}")

# SAVE RESULTS TO FILE
# This creates a text file with each token and its lemma on a separate line.
with open("lemmatized_output.txt", "w", encoding="utf-8") as out:
    for token in doc:
        out.write(f"{token.text} -> {token.lemma_}\n")
