
import json

# Load irregular dictionary
with open("irregular_dict.json", "r") as f:
    irregulars = json.load(f)

def lemmatize(word):
    if word in irregulars:
        return irregulars[word]
    elif word.endswith("ean"):
        return word[:-3]
    elif word.endswith("an"):
        return word[:-2]
    elif word.endswith("achan"):
        return word[:-5] + "ach"
    else:
        return word

# Test it with the mock tokens
with open("mock_tokens.txt", "r") as f:
    tokens = [line.strip() for line in f.readlines()]

for token in tokens:
    print(f"{token} → {lemmatize(token)}")
