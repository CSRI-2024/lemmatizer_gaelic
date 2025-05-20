# Import spaCy and required classes for building custom NLP components
import spacy
from spacy.language import Language

# Import JSON module to read the irregular lemma dictionary
import json

# LOAD IRREGULAR DICTIONARY
# This JSON file contains a dictionary of irregular Gaelic words mapped to their lemmas (base forms).
# These are exceptions that cannot be handled using simple suffix-stripping rules.
with open("irregular_dict.json", "r", encoding="utf-8") as f:
    irregulars = json.load(f)

# CREATE NLP PIPELINE
# Create a blank spaCy NLP pipeline.
# 'xx' is a multilingual placeholder used when no built-in language model is available (Scottish Gaelic is unsupported).
nlp = spacy.blank("xx")

# DEFINE CUSTOM RULE-BASED LEMMATIZER
# This is a custom component that replaces spaCy’s default lemmatizer.
# It applies a two-step approach:
# (1) Check for irregular forms in the dictionary,
# (2) Apply rule-based suffix stripping for common endings.
@Language.component("gaelic_lemmatizer")
def gaelic_lemmatizer(doc):
    for token in doc:
        text = token.text.lower()  # Lowercasing ensures consistency

        # Step 1: Handle known irregular words
        if text in irregulars:
            token.lemma_ = irregulars[text]
            continue  # Skip to next token

        # Step 2: Apply custom suffix-stripping rules in order
        for suffix, rule in suffix_rules:
            if text.endswith(suffix):
                token.lemma_ = rule(text)
                break  # Stop at the first matching rule
        else:
            # If no rule matches, return the word as-is
            token.lemma_ = text

    return doc  # Return the processed document with updated lemmas

# DEFINE SUFFIX RULES=
# This list defines common morphological patterns in Scottish Gaelic.
# Each rule removes or modifies a known suffix to approximate the word's base form.
# Ordered from longest to shortest to prevent partial matches
suffix_rules = [
    ("adaireachd", lambda w: w[:-10]),      # Agentive abstract
    ("adairean",   lambda w: w[:-8]),       # Agentive plural
    ("airean",     lambda w: w[:-7]),       # Alternative plural
    ("idhean",     lambda w: w[:-6]),       # Long plural
    ("eanach",     lambda w: w[:-6]),       # Terrain/collective
    ("rachaidh",   lambda w: w[:-7]),       # Verb future
    ("achan",      lambda w: w[:-5] + "ach"),# Diminutive
    ("adaire",     lambda w: w[:-6]),       # Agent noun
    ("aiche",      lambda w: w[:-5]),       # Abstract adjective
    ("eachd",      lambda w: w[:-5]),       # Abstract noun
    ("ean",        lambda w: w[:-3]),       # Regular plural
    ("achd",       lambda w: w[:-4]),       # Abstract noun
    ("an",         lambda w: w[:-2]),       # Short plural
]

# REGISTER CUSTOM LEMMATIZER
# Add the custom component to the end of the NLP pipeline
# so it's applied after tokenization.
nlp.add_pipe("gaelic_lemmatizer", name="lemmatizer", last=True)

# SET INPUT FILE
# This file contains tokenized words (one per line).
# Currently using mock data; will switch to a real tokenized corpus later.
input_file = "mock_tokens.txt"

# LOAD TOKENS FROM FILE
# Read each line (one token per line), strip whitespace, and convert to lowercase.
token_list = [line.strip().lower() for line in open(input_file, "r", encoding="utf-8") if line.strip()]

# PROCESS TOKENS
# spaCy expects a full text string, so we join tokens into one space-separated string.
# This triggers tokenization + custom lemmatization via the NLP pipeline.
text = " ".join(token_list)
doc = nlp(text)

# PRINT RESULTS
# Output each original token with its computed lemma
print("Token → Lemma")
print("-" * 20)
for token in doc:
    print(f"{token.text} → {token.lemma_}")


# SAVE OUTPUT TO FILE
with open("lemmatized_output.txt", "w", encoding="utf-8") as out:
    for token in doc:
        out.write(f"{token.text} -> {token.lemma_}\n")