# Scottish Gaelic Lemmatizer – CSRI Research Project

This project is part of an ongoing collaborative research initiative between the **Cornell College Computer Science Department** and **Napier University** in Edinburgh, Scotland. The goal is to build tools that enable deeper text analysis for the **Scottish Gaelic language** — a low-resource language with limited computational tools.


It integrates directly with **spaCy**, making Scottish Gaelic NLP processing accessible to researchers, educators, and developers anywhere in the world.

---

## Project Overview

This work is part of a multi-year research collaboration between:

- **Cornell College – Computer Science & Data Science**
- **Edinburgh Napier University – Languages & NLP**

**Year 1 (2023–2024):**
- Built a cleaned corpus  
- Created a Gaelic tokenizer  
- Developed preprocessing tools and scraping pipelines  

**Year 2 (2024–2025):**
- Built a rule-based + POS-aware lemmatizer  
- Published the pipeline to **PyPI**  
- Added accent normalization, lenition handling, prosthetic removal, suffix rules  
- Integrated a lightweight POS tagger  
- Created evaluation + benchmarking scripts  
- Constructed irregular dictionaries and frequency-driven refinement methods  

This project supports **low-resource language revitalization** by providing tools normally unavailable for Gaelic.

---


## What This Tool Does

This lemmatizer reduces inflected Scottish Gaelic word forms to their base forms (**lemmas**) using:

- A **manually curated irregular dictionary** for unpredictable wordforms (e.g., `chunnaic → faic`)
- A set of **carefully tested suffix rules** for regular morphological patterns (e.g., `taighean → taigh`)
- **Preprocessing steps** that handle accents, emphatic suffixes, prosthetic consonants, and lenition
- **Frequency-guided refinement**: rules and dictionary are informed by analysis of the most common words
- Output in a simple, editable format for future researchers to reuse or expand

---

## Tree-like Folder Structure

```
gd_core_web_sm/
├── config.cfg                # spaCy pipeline config
├── meta.json                 # spaCy model metadata
├── lookups/                  # irregular dict & rulesets
├── models/                   # tagger model + vectors
├── tokenizer/                # tokenizer data
├── pos_aware_lemmatizer.py   # main rule-based lemmatizer

```


---

##  How It Works

### 1. **Corpus Preparation**
- The input corpus (`Latest_Corpus.txt`) contains lines in the format:
- Only the first word of each line is used for lemmatization.

---

### 2. **Preprocessing Steps**
- Replace **acute accents** with **grave accents**
- Remove **emphatic suffixes**: `-sa`, `-se`, `-san`, `-ne`
- Strip **prosthetic consonants**: `t-`, `h-`, `n-` (at beginning)
- Remove **lenition marker**: `h` as second letter (e.g., `bhean → bean`)

---

### 3. **Lemmatization Logic **

- Apply preprocessing to each token
- If token exists in irregular dictionary → use its mapped lemma
- If not, apply suffix rules (`-ean`, `-an`, `-achadh`, etc.)
- If no rules match, return preprocessed token (unless it's too short)

---

## Code Flowchart

```
Load input corpus file
  ↓
Process text with spaCy pipeline (Tokenizer -> POS Tagger -> Custom Lemmatizer)
  ↓                                  (This step assigns POS tags to tokens)
For each token in the spaCy `Doc` object:
  ↓
  Get lowercased raw text
  Initialize lemma with raw text
  ↓
  1. Check if raw token text exists in irregular dictionary
  ├─ Yes → Use lemma from irregulars (e.g., "deach" → "rach") and SKIP further steps for this token
  └─ No → Proceed to preprocessing
             ↓
      2. Preprocess token text (e.g., "chuala" → "cuala", "bhean" → "bean"):
        ├─ Replace acute accents with grave accents
        ├─ Remove emphatic suffixes
        ├─ Remove prosthetic consonants
        └─ Remove lenition marker
             ↓
      3. Check if preprocessed token text exists in irregular dictionary
      ├─ Yes → Use lemma from irregulars (e.g., "cuala" → "cluinn") and SKIP further steps
      └─ No → Proceed to POS-informed suffix rules
                  ↓
          4. Apply POS-informed suffix rules (based on `token.pos_`):
            ├─ If `token.pos_ == "NOUN"`:
            │  ├─ Apply longest noun suffixes first (e.g., "-aichean" -> "", "-annan" -> "", "-ean" -> "", "-an" -> "")
            │  └─ Examples: "eileanan" → "eilean", "stàitean" → "stàit", "lochan" → "loch"
            ├─ If `token.pos_ == "VERB"`:
            │  ├─ Apply longest verb suffixes first (e.g., "-eachadh" -> "-ich", "-eadh" -> "", "-te" -> "", "-ta" -> "")
            │  └─ Examples: "atharrachadh" → "atharraich", "stèidheachadh" → "stèidhich", "aonaichte" → "aonaich", "sònraichte" → "sònraich"
            ├─ If `token.pos_ == "ADJ"`:
            │  ├─ Apply adjective-specific rules
            │  └─ Examples: (comparatives, superlatives, ensuring base forms like "cumanta" remain unchanged)
            └─ If no POS-specific rule matched:
                   ↓
                  5. Fallback: If preprocessing changed the word and no rule applied, use preprocessed word as lemma.
                      If lemma length is 1 or less (and not an irregular), revert to original raw text.
  ↓
Assign final lemma to token in spaCy `Doc` object
  ↓
Repeat for all tokens
  ↓
Output results:
  ├─ Print token → lemma to console
  └─ Save results to `lemmatized_output_pos_aware_example.txt`
  ↓
Print summary:
  ├─ Changed by irregulars
  ├─ Changed by preprocessing
  ├─ Changed by suffix
  ├─ Total changed / unchanged words
  └─ Total operations applied
```

---

## Quickstart: Using the Scottish Gaelic Lemmatizer (`gd_core_web_sm`)

The `gd_core_web_sm` package provides a fully integrated Scottish Gaelic NLP pipeline, including a rule-based lemmatizer, lightweight POS tagger, and Gaelic-specific preprocessing (lenition, accents, emphatics, prosthetics). This Quickstart shows how to install, load, and use the model effectively. Note: `gd_core_web_sm` is an independently developed model and is not an official spaCy model.

---

### Installation

```bash
pip install spacy
pip install gd-core-web-sm
```
A successful load means the model is ready for lemmatization and POS tagging.

### Token-Level Lemmatization

Example Code:
```
import spacy
nlp = spacy.load("gd_core_web_sm")

text = "Chunnaic mi e agus chuala mi i."
doc = nlp(text)

for token in doc:
    print(f"{token.text:<12} → {token.lemma_:<12} ")

```

Output:
```
Chunnaic     → faic
mi           → mi
e            → e
agus         → agus
chuala       → cluinn
mi           → mi
i            → i
.            → .            

```


---

## Future Work

- Improve Gaelic POS tagger lemmatization accuracy
- Expand suffix rules and irregulars using linguistic input from Napier University
- Group frequent words by part of speech (noun, verb, adj) for better rule targeting
- Evaluate lemmatizer accuracy using a manually verified gold standard

---

## Status
Active Development - Dec 2025


