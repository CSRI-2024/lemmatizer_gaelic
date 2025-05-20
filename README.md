# Scottish Gaelic Lemmatizer

This is a custom, rule-based lemmatizer for Scottish Gaelic, built as part of a collaborative text analysis project with Napier University. It uses the spaCy NLP framework and is designed to work with a cleaned Gaelic corpus and tokenized text.

Since Scottish Gaelic is a low-resource language with no official spaCy language model, this lemmatizer is implemented as a **custom pipeline component** using a combination of:

-  Simple suffix-stripping rules (e.g., for plural and diminutive endings)
-  A manually curated dictionary of irregular word forms
-  spaCy's lightweight `blank("xx")` pipeline for token handling

---

##  What This Project Does

- Loads a list of Gaelic word tokens from a file
- Applies custom lemmatization rules and dictionary mappings
- Prints each word alongside its identified lemma (base form)

---

##  Project Structure
lemmatizer_gaelic/ \n
├── lemmatizer.py # Main script with spaCy pipeline and rules \n
├── irregular_dict.json # Dictionary of irregular Gaelic word forms \n
├── mock_tokens.txt # Sample word list for testing \n
├── README.md # Project documentation \n

