# Import spaCy and required classes
import spacy
from spacy.language import Language
import json

# LOAD IRREGULAR DICTIONARY
# Dictionary of known exceptions (irregular forms): word → lemma
with open("irregular_dict.json", "r", encoding="utf-8") as f:
    irregulars = json.load(f)

# DEFINE SUFFIX RULES (REFINED)
# More cautious rules focused on validated morphological patterns
suffix_rules = [
    # Genitive singular: "eilein" → "eilean"
    ("in", lambda w: w[:-2] + "an"),

    # Plural form: "eileanan" → "eilean"
    ("anan", lambda w: w[:-5]),

    # General plural: "ean" → remove (only if not caught above)
    ("ean", lambda w: w[:-3]),
]

# CREATE BLANK NLP PIPELINE
nlp = spacy.blank("xx")
nlp.max_length = 10_000_000  # Allow large input

# CUSTOM LEMMATIZER
@Language.component("gaelic_lemmatizer")
def gaelic_lemmatizer(doc):
    for token in doc:
        text = token.text.lower()

        # Step 1: Check against irregulars
        if text in irregulars:
            token.lemma_ = irregulars[text]
            continue

        # Step 2: Apply suffix rules (first match wins)
        for suffix, func in suffix_rules:
            if text.endswith(suffix):
                token.lemma_ = func(text)
                break
        else:
            # Step 3: No rule applies → return original
            token.lemma_ = text

    return doc

# REGISTER CUSTOM LEMMATIZER
nlp.add_pipe("gaelic_lemmatizer", name="lemmatizer", last=True)

# LOAD AND PROCESS INPUT FILE
input_file = "CleanedCorpus.txt"
tokens = [line.strip().lower() for line in open(input_file, "r", encoding="utf-8") if line.strip()]
text = " ".join(tokens)
doc = nlp(text)

# DISPLAY OUTPUT
print("Token → Lemma")
print("-" * 20)
for token in doc:
    print(f"{token.text} → {token.lemma_}")

# SAVE OUTPUT TO FILE
with open("lemmatized_output.txt", "w", encoding="utf-8") as out:
    for token in doc:
        out.write(f"{token.text} -> {token.lemma_}\n")
