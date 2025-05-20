import spacy
from spacy.language import Language
import json

# Load irregular dictionary from JSON
with open("irregular_dict.json", "r", encoding="utf-8") as f:
    irregulars = json.load(f)

# Create a blank spaCy pipeline (no pretrained language model)
nlp = spacy.blank("xx")  # "xx" = multilingual placeholder

# Define custom rule-based lemmatizer component
@Language.component("gaelic_lemmatizer")
def gaelic_lemmatizer(doc):
    for token in doc:
        text = token.text

        # Irregular words
        if text in irregulars:
            token.lemma_ = irregulars[text]
        # Rule-based suffix stripping
        elif text.endswith("ean"):
            token.lemma_ = text[:-3]
        elif text.endswith("an"):
            token.lemma_ = text[:-2]
        elif text.endswith("achan"):
            token.lemma_ = text[:-5] + "ach"
        else:
            token.lemma_ = text  # No rule match — return word as-is

    return doc

# Add lemmatizer to spaCy pipeline
nlp.add_pipe("gaelic_lemmatizer", name="lemmatizer", last=True)

# Load test tokens from file
with open("mock_tokens.txt", "r", encoding="utf-8") as f:
    token_list = [line.strip() for line in f.readlines()]

# Join tokens into a fake sentence (spaCy needs text input, not a token list)
text = " ".join(token_list)
doc = nlp(text)

# Print token and lemma pairs
print("Token → Lemma")
print("-" * 20)
for token in doc:
    print(f"{token.text} → {token.lemma_}")
