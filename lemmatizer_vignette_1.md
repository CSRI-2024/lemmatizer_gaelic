---
title: "Scottish Gaelic Lemmatizer — POS-Aware Rule-Based System"
author: "Oskar Diyali"
format:
  html:
    toc: true
    toc-location: right
    code-fold: true
    code-tools: true
    number-sections: true
---

# Understanding Scottish Gaelic Lemmatizer

Lemmatization is the process of reducing inflected word forms to their base (dictionary) form — or *lemma*. In highly inflected and morphologically rich languages like **Scottish Gaelic**, building an effective lemmatizer requires both linguistic insight and computational precision. This document explains how a **POS-aware rule-based lemmatizer** was developed as part of the **CSRI Gaelic NLP project** in collaboration with **Cornell College** and **Napier University**.

---
# Project Objectives

- Handle both **regular** and **irregular** morphological variants.
- Respect grammatical structures via **part-of-speech (POS)** awareness.
- Preprocess Scottish Gaelic orthographic idiosyncrasies: **lenition**, **prosthetics**, **emphatics**, and **accent normalization**.
- Use **frequency-ranked corpora** to prioritize rule generalization and dictionary entries.
- Produce **clean, interpretable output** for further NLP tasks.

---

# Inputs Required

| Filename                  | Description |
|---------------------------|-------------|
| `gaelic_words.txt`        | Corpus list (one word per line, ordered by frequency) |
| `irregular_dict.json`     | Dictionary of irregular forms (e.g., `bha → bi`) |
| `gaelic_pos.json` | POS-tagged version of the 500 most frequent words |

---
# Main Lemmatizer Logic

The lemmatizer is implemented as a **spaCy pipeline component**. For each token:

1. Check against irregular dictionary (highest priority)
2. Preprocess (normalize accents, remove affixes)
3. Re-check for irregulars post-preprocessing
4. Apply suffix-based rules based on POS
5. Fallback: use preprocessed form
6. Filter overly short lemmas (≤ 1 character)

---
# Irregular Dictionary

A JSON file (`irregular_dict.json`) maps irregular inflected forms to their lemma. Examples:

```json
{
  "chunnaic": "faic",
  "fhuair": "faigh",
  "chaidh": "rach",
  "thàinig": "thig",
  "bhiodh": "bi",
  "cait": "cat",
  "mnathan": "bean"
}
```

Irregulars are **checked first** in the pipeline, before preprocessing or suffix rules. If a the Scottish Gaelic word is found in the irregular dictionary, the **assigned lemma** of that word is returned as the **final lemma**.



---

# Preprocessing Logic

The `preprocess_gaelic_word()` function performs normalization specific to Gaelic spelling conventions.

```python
from lemmatizer import preprocess_gaelic_word

print(preprocess_gaelic_word("t-each"))   # → each
print(preprocess_gaelic_word("agam-sa"))  # → agam
print(preprocess_gaelic_word("mór"))      # → mòr
print(preprocess_gaelic_word("dh’òl"))    # → òl
```

The first stage of the lemmatizer is preprocessing, where superficial forms of the word are normalized.
This ensures all variants like emphatic forms or older orthography are transformed to a consistent format before applying further rules.

```python
from lemmatizer import preprocess_gaelic_word

# Normalize prosthetic consonants and accents
examples = ["t-each", "mór", "agam-sa", "dh’òl"]
normalized = [preprocess_gaelic_word(w) for w in examples]
print(normalized)
```

This snippet demonstrates how `preprocess_gaelic_word` cleans and standardizes Gaelic tokens. For example, `"t-each"` becomes `"each"`, and `"agam-sa"` simplifies to `"agam"`. These transformations help the suffix rules and dictionary lookup operate on the core lemma-like form.


- Replace **acute accents** (á, é, í) with **grave accents** (à, è, ì)
- Remove **emphatic suffixes**: `-sa`, `-se`, `-san`, `-ne`
- Strip **prosthetic consonants**: `t-`, `h-`, `n-`
- Remove **lenition marker** if the second letter is `h`
- Remove **`dh’`** or **`dh'`** prosthetic forms


---

## Rule Application with POS Context

Once a token is preprocessed, suffix rules are applied differently depending on the POS tag. This snippet shows how noun plural endings are handled.

```python
def noun_suffix_rule(word):
    if word.endswith("aichean"):
        return word[:-7]
    elif word.endswith("ean"):
        return word[:-3]
    return word

# Apply noun rule
tokens = ["notaichean", "taighean", "lochannan"]
lemmas = [noun_suffix_rule(preprocess_gaelic_word(tok)) for tok in tokens]
print(lemmas)
```

This rule-based strategy strips common noun suffixes like `-aichean`, `-ean`, and `-annan`. It uses preprocessing first, ensuring that words are in their most analyzable form before suffix handling occurs. This reduces false matches and improves lemma precision.


### Some POS-Specific Examples

| POS   | Rule Example | Result      |
|-------|--------------|-------------|
| NOUN  | `aichean` → remove → `notaichean` → `not` |
| VERB  | `eachadh` → `ich` → `stèidheachadh` → `stèidhich` |
| ADJ   | `ach`, `ta`, `te` → remove selectively |

---


## Code Snippet

```python
from lemmatizer import nlp

doc = nlp("bha daoine a’ fuireach anns na taighean")
for token in doc:
    print(token.text, "→", token.lemma_, "|", token.pos_)
```

This code snippet showcases how to run the custom Scottish Gaelic lemmatizer on a full sentence and retrieve both the lemmas and part-of-speech (POS) tags for each token. By passing a Gaelic sentence into the (`nlp`) pipeline, spaCy tokenizes it and runs each word through your preprocessing rules, irregular dictionary, and POS-aware suffix logic. The output reveals how the lemmatizer reduces inflected forms like “taighean”_ to their base forms (e.g., _“taigh”_) and correctly tags POS such as _VERB, NOUN, or ADP_. This is a compact demonstration of the lemmatizer's full functionality on real input.

---
## Output:

```
bha → bi | VERB
daoine → duine | NOUN
fuireach → fuirich | VERB
taighean → taigh | NOUN
```


Each line shows an original word mapped to its _lemma_. Alongside this, its part of speech is identified.

---
# Example Corpus Chart

Below is a sample from the Top500Words.txt frequency list used:

| Word      | Frequency |
|-----------|-----------|
| ann       | 77031     |
| tha       | 56620     |
| bha       | 40729     |
| airson    | 12383     |
| taighean  | 3306      |

---
# Result Summary

```text
Summary of Lemmatization Changes (POS-Aware):
-------------------------------------------------------
Words changed by irregular dictionary: 61
Words changed by preprocessing: 79
Words changed by suffix rules: 35
-------------------------------------------------------
Total words changed: 175
Total words unchanged: 324
Total processed: 499
```
This summarizes how words were transformed into their base forms. It breaks down the changes by the method used (_irregular dictionary, preprocessing, suffix rules_) and shows the total words changed versus those that remained the same.

---
# Flowchart Summary

```text
Load input file
  ↓
If in irregulars → return final lemma
  ↓
Preprocess (accents, emphatics, prosthetics, lenition)
  ↓
Check again in irregulars
  ↓
Apply POS-based suffix rules
  ↓
If no rules match → use preprocessed form
  ↓
If lemma too short → use original
  ↓
Save result + print summary
```

---

## Optional: Word Frequency Chart Example (using matplotlib)

You can visualize the top 20 frequent lemmatized words using `matplotlib` for a quick understanding of common lemma distributions in the corpus.

```python
import matplotlib.pyplot as plt
from collections import Counter

# Dummy frequency list of lemmatized tokens
lemmas = ["bi", "duine", "taigh", "bi", "bi", "duine", "alba", "alba", "eilean"]
lemma_counts = Counter(lemmas)

# Plotting
top = lemma_counts.most_common(5)
words, freqs = zip(*top)
plt.figure(figsize=(8,4))
plt.bar(words, freqs)
plt.title("Top 5 Most Frequent Lemmas")
plt.xlabel("Lemma")
plt.ylabel("Frequency")
plt.show()
```

This bar chart gives a high-level overview of lemma frequency, which helps determine which lemmas are dominant and whether any preprocessing or rule-related errors skew the data. This is crucial for iteratively refining the lemmatizer’s accuracy.

---

# Future Improvements

- Integrate full **automatic POS tagging** before lemmatization
- Improve **handling of ambiguous forms** (e.g., `fir` → `fear`, `fir` plural or genitive?)
- Compile **statistical patterns** of inflections for verbs/nouns/adjectives
- Improve **visualization and accuracy testing** with labeled test corpus

---

# Credits

This work is part of the CSRI research collaboration between Cornell College and Edinburgh Napier University.  
Special thanks to **Dr. Barclay**, **Dr. George**, **Dr. Chavan**, and **Dr. Lawson** for their support.


---
