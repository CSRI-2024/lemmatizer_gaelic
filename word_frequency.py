from collections import Counter

tokens = []

with open("mock_tokens.txt", "r", encoding="utf-8") as f:
    for line in f:
        # Strip whitespace, skip if line is empty
        line = line.strip()
        if line:
            # Split into words, lowercase them, and add to tokens list
            tokens.extend(word.lower() for word in line.split() if word)

# COUNT WORD FREQUENCIES
word_counts = Counter(tokens)

# DISPLAY RESULTS
print("Word → Frequency")
print("-" * 20)
for word, freq in word_counts.most_common():
    print(f"{word} → {freq}")




