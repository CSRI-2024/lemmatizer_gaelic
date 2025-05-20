from collections import Counter
import spacy

# Load a blank spaCy pipeline (for basic tokenization)
nlp = spacy.blank("xx")

# Read the cleaned corpus text file
with open("mock_tokens.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Process the text with spaCy to split it into tokens
doc = nlp(text)

# Count word frequencies (skip punctuation/numbers, lowercase for consistency)
word_counts = Counter(token.text.lower() for token in doc if token.is_alpha)

# Print the 20 most frequent words
print("Word → Frequency")
print("-" * 20)
for word, freq in word_counts.most_common(20):
    print(f"{word} → {freq}")


