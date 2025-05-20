from collections import Counter

# LOAD STOP WORDS
with open("stopWords.txt", "r", encoding="utf-8") as f:
    stop_words = set()
    for line in f:
        stop_words.update(word.strip().lower() for word in line.split() if word.strip())

# LOAD TOKENS
tokens = []
with open("mock_tokens.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            tokens.extend(
                word.lower() for word in line.split()
                if word.lower() not in stop_words
            )

# COUNT FREQUENCIES
word_counts = Counter(tokens)

# DISPLAY RESULTS
print("Word → Frequency (excluding stop words)")
print("-" * 40)
for word, freq in word_counts.most_common():
    print(f"{word} → {freq}")
