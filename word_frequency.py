from collections import Counter

#LOAD TOKENS FROM FILE
# Currently using mock_tokens.txt (one word per line)
with open("mock_tokens.txt", "r", encoding="utf-8") as f:
    # Strip line breaks and lowercase each word
    tokens = [line.strip().lower() for line in f if line.strip()]

# COUNT WORD FREQUENCIES
word_counts = Counter(tokens)

# PRINT RESULTS
print("Word → Frequency")
print("-" * 20)
for word, freq in word_counts.most_common():
    print(f"{word} → {freq}")




