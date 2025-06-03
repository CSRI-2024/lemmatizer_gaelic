from collections import Counter

# LOAD STOP WORDS
# Read stop words from file and store in a set for fast lookup
with open("stopWords.txt", "r", encoding="utf-8") as f:
    stop_words = set()
    for line in f:
        # Assumes words are space-separated in each line
        stop_words.update(word.strip().lower() for word in line.split() if word.strip())

# LOAD AND PROCESS TOKENS FROM CLEANED CORPUS
tokens = []
with open("OneLineFile.txt", "r", encoding="utf-8") as f:
    for line in f:
        word = line.strip().lower()
        if word and word not in stop_words:
            tokens.append(word)

# COUNT WORD FREQUENCIES
word_counts = Counter(tokens)

# DISPLAY TOP 100 FREQUENT WORDS
print("TOP 100 FREQUENT WORDS")
print("Word → Frequency (excluding stop words)")
print("-" * 40)
for word, freq in word_counts.most_common(500):  # Adjust number as needed
    print(f"{word} → {freq}")
