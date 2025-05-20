import spacy
from spacy.language import Language
import json

# LOAD IRREGULAR DICTIONARY
with open("irregular_dict.json", "r", encoding="utf-8") as f:
    irregulars = json.load(f)

# CREATE NLP PIPELINE
nlp = spacy.blank("xx")  # 'xx' is for unsupported languages like Scottish Gaelic

# DEFINE CUSTOM RULE-BASED LEMMATIZER
@Language.component("gaelic_lemmatizer")
def gaelic_lemmatizer(doc):
    for token in doc:
        text = token.text.lower()

        # Check if it's an irregular form
        if text in irregulars:
            token.lemma_ = irregulars[text]
            continue

        # Apply suffix-stripping rules (in order of specificity)
        for suffix, rule in suffix_rules:
            if text.endswith(suffix):
                token.lemma_ = rule(text)
                break
        else:
            token.lemma_ = text  # Default: return word unchanged

    return doc

# DEFINE SUFFIX RULES
# Ordered from longest to shortest to avoid partial matches
suffix_rules = [
    ("adairean", lambda w: w[:-8]),
    ("idhean",   lambda w: w[:-6]),
    ("achan",    lambda w: w[:-5] + "ach"),
    ("ean",      lambda w: w[:-3]),
    ("achd",     lambda w: w[:-4]),
    ("an",       lambda w: w[:-2]),
]

# REGISTER LEMMATIZER IN PIPELINE
nlp.add_pipe("gaelic_lemmatizer", name="lemmatizer", last=True)

# SET INPUT FILE
input_file = "mock_tokens.txt"  # Switch to "tokenized_corpus.txt" later

# LOAD TOKENS FROM FILE
with open(input_file, "r", encoding="utf-8") as f:
    token_list = [line.strip().lower() for line in f if line.strip()]

# Join tokens into a single string so spaCy can process them
text = " ".join(token_list)
doc = nlp(text)

# PRINT OUTPUT
print("Token → Lemma")
print("-" * 20)
for token in doc:
    print(f"{token.text} → {token.lemma_}")


