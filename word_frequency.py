from collections import defaultdict, Counter

# CONFIG
corpus_file = "New_Cleaned_Corpus2.txt"
stop_words_file = "stopWords.txt"
top_n = 50

# LOAD STOP WORDS
with open(stop_words_file, "r", encoding="utf-8") as f:
    stop_words = set()
    for line in f:
        stop_words.update(word.strip().lower() for word in line.split() if word.strip())

# LOAD AND COUNT TOKENS BY SOURCE
# Format: word "source name"
source_word_freq = defaultdict(Counter)

with open(corpus_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue  # Skip blank lines

        tokens = line.split()
        if len(tokens) < 2:
            continue  # Skip malformed lines

        word = tokens[0].lower()  # only the first word
        source = " ".join(tokens[1:]).strip('"').lower()  # rest is the source

        if word and word not in stop_words:
            source_word_freq[source][word] += 1

# DISPLAY TOP N WORDS PER SOURCE
print(f"\nTop {top_n} most frequent words in each source (excluding stop words):")
print("-" * 50)
for source, counter in source_word_freq.items():
    print(f"\n{source}:")
    for word, freq in counter.most_common(top_n):
        print(f"  {word} → {freq}")
