# Scottish Gaelic Lemmatizer – CSRI Research Project

This project is part of an ongoing collaborative research initiative between the Cornell College Computer Science Department and Napier University in Edinburgh, Scotland. The goal is to build tools that enable deeper text analysis for the Scottish Gaelic language — a low-resource language with limited computational tools.

---

## Project Context

- **Year 1**: A team of students created a cleaned corpus of Scottish Gaelic text and a tokenizer.
- **Year 2 (Current)**: Our focus is on developing a rule-based lemmatizer, generating word frequency statistics, and implementing preprocessing techniques specific to Scottish Gaelic grammar and spelling.

---

## What This Tool Does

This lemmatizer reduces inflected Scottish Gaelic word forms to their base forms (**lemmas**) using:

- A **manually curated irregular dictionary** for unpredictable wordforms (e.g., `chunnaic → faic`)
- A set of **carefully tested suffix rules** for regular morphological patterns (e.g., `taighean → taigh`)
- Preprocessing steps that handle **accents**, **emphatic suffixes**, **prosthetic consonants**, and **lenition** based on expert Gaelic linguistic guidelines
- Frequency-guided refinement: all rules and dictionary entries are based on analysis of the most common words in the corpus
- Output in a simple, editable format for future researchers to reuse or expand

---

# Tree-like Folder Structure

```text
lemmatizer_gaelic/
├── lemmatizer.py           # Main lemmatization script using spaCy
├── irregular_dict.json     # Irregular word → lemma mappings
├── Latest_Corpus.txt       # Cleaned corpus with "word source" format
├── lemmatized_output.txt   # Final lemma output (token → lemma)
├── word_frequency.py       # Word frequency analysis script (by source)
├── stopWords.txt           # List of Gaelic stop words (excluded from stats)
├── CorpusBySource.py       # Exports per-source texts from the raw corpus
└── README.md               # Project documentation
```
---

## How It Works

### 1. **Corpus Preparation**
   - The input corpus (`Latest_Corpus.txt`) contains lines in the format `word "source"`
   - Only the first word of each line is used for lemmatization

### 2. **Preprocessing Steps**
   - Replace **acute accents** with **grave accents** to match modern Gaelic orthography
   - Remove **emphatic suffixes** (`-sa`, `-se`, `-san`, `-ne`)
   - Strip **prosthetic consonants** (`t-`, `h-`, `n-`) from the start of words
   - Remove **lenition** markers (i.e., `h` as second letter)

### 3. **Lemmatization (lemmatizer.py)**
   - Apply preprocessing to each word
   - Match irregular forms from `irregular_dict.json`
   - Apply known suffix rules (`-ean`, `-anan`, `-in`) to transform regular words
   - Save results in `lemmatized_output.txt`

## Code Flowchart

```text
Load input corpus file 
  ↓
Extract tokens (words) → store in list
  ↓
For each token in list:
  ↓
Preprocess token:
  ├─ Replace acute accents with grave accents
  ├─ Remove emphatic suffixes (e.g., -sa, -se)
  ├─ Remove prosthetic consonants (e.g., t-, h-, n-)
  └─ Remove lenition marker (initial 'h' after first consonant)
  ↓
Check if token is in irregular lemma dictionary
  ├─ Yes → Assign irregular lemma
  └─ No → Apply suffix rules:
          ├─ If suffix matches, transform token to lemma
          └─ Else → lemma = preprocessed token
  ↓
Assign lemma to token in spaCy Doc object
  ↓
Repeat for all tokens
  ↓
Output results:
  ├─ Print token → lemma pairs to console
  └─ Write token → lemma pairs to output file (lemmatized_output.txt)
```

### 4. **Word Frequency Analysis (word_frequency.py)**
   - Computes the top 100 most frequent words from each source (excluding stop words)
   - Used to guide dictionary updates and new rule creation

---

## Future Work

- Expand suffix rules and irregular dictionary based on linguistic patterns shared by Napier University
- Group frequent words by part-of-speech (nouns, verbs, adjectives)
- Generate statistics on morphological patterns by frequency
- Evaluate lemmatizer accuracy with a human-validated reference set

---

## Status
**Work in Progress – May 2025**
