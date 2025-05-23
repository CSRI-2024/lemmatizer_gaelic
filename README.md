# Scottish Gaelic Lemmatizer – CSRI Research Project

This project is part of an ongoing collaborative research initiative between the Cornell College Computer Science Department and Napier University in Edinburgh, Scotland. The goal is to build tools that enable deeper text analysis for the Scottish Gaelic language — a low-resource language with limited computational tools.

---

## Project Context

- **Year 1**: A team of students created a cleaned corpus of Scottish Gaelic text and a tokenizer.
- **Year 2 (Current)**: Our focus is on developing a rule-based lemmatizer and generating linguistic statistics to support broader Gaelic text analysis.

---

## What This Tool Does

This lemmatizer reduces inflected Scottish Gaelic word forms to their base forms (**lemmas**) using:

- A **manually curated irregular dictionary** for unpredictable wordforms (e.g., `chunnaic → faic`)
- A set of **carefully tested suffix rules** for regular morphological patterns (e.g., `taighean → taigh`)
- Frequency-guided refinement: all rules and dictionary entries are based on analysis of the most common words in the corpus
- Output in a simple, editable format for future researchers to reuse or expand

---

## Project Structure

lemmatizer_gaelic/
├── lemmatizer.py # Main lemmatization script using spaCy
├── irregular_dict.json # Irregular word → lemma mappings
├── CleanedCorpus.txt # Cleaned and tokenized Gaelic corpus
├── word_frequency.py # Tool to generate word frequency statistics
├── stopWords.txt # List of Gaelic stop words (excluded from stats)
├── lemmatized_output.txt # Final lemma output (token → lemma)
├── word_frequencies.txt # Top 100 frequent tokens for refinement
└── README.md # Project documentation


---

##  How It Works

1. **Word Frequency Analysis**  
   Use `word_frequency.py` to generate a ranked list of tokens (excluding stop words).

2. **Manual Review & Rule Creation**  
   Identify the most common irregular and regular word patterns.

3. **Lemmatization Process (`lemmatizer.py`)**
   - Matches known irregular forms from `irregular_dict.json`
   - Applies safe suffix rules to common word endings (e.g., `-ean`, `-anan`, `-in`)
   - Leaves unmatched tokens unchanged

4. **Output**  
   Results are saved to `lemmatized_output.txt` in the format:  

**Work on Progress**
