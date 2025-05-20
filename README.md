# Scottish Gaelic Lemmatizer

This is a custom, rule-based lemmatizer for Scottish Gaelic, developed as part of a collaborative text analysis project with Napier University in Edinburgh. The tool is implemented using the [spaCy](https://spacy.io/) NLP framework and is designed to process a cleaned and tokenized Gaelic corpus.

Because Scottish Gaelic is a low-resource language without an official spaCy model, we use a lightweight custom NLP pipeline (`spacy.blank("xx")`) and integrate:

- A curated dictionary of **irregular word → lemma** mappings
- A flexible set of **rule-based suffix stripping functions**
- spaCy's custom pipeline API for efficient lemmatization

---

## What This Project Does

- Loads **tokenized Gaelic words** from a file (e.g. `mock_tokens.txt`)
- Applies a **custom lemmatizer** that:
  - Matches irregular forms using `irregular_dict.json`
  - Applies common suffix-stripping rules (e.g., `"ean" → ""`, `"achan" → "ach"`)
- Outputs each word and its **lemma** to:
  - The console
  - A tab-separated file: `lemmatized_output.txt`

---

## Project Structure `
text lemmatizer_gaelic/
├── lemmatizer.py # Main script: spaCy pipeline, suffix rules, and output 
├── irregular_dict.json # Dictionary of irregular Gaelic word → lemma mappings 
├── mock_tokens.txt # Sample tokenized input (one word per line) 
├── lemmatized_output.txt # Output: token → lemma (generated after running script) 
├── word_frequency.py # Counting word frequencies 
└── README.md # This documentation 

