import os
import git
from bs4 import BeautifulSoup

# SETTINGS
REPO_URL = "https://github.com/CSRI-2024/Gaelic-Corpus.git"  # Replace with the actual repo
CLONE_DIR = "gaelic_corpus_repo"
OUTPUT_DIR = "separated_sources"
SOURCES = ["BBC Alba News", "Gutenberg Texts", "Letters to Learners", "Little Letters", "Wikipedia Dump"]
ATTRIBUTES = ["title", "content"]
INCLUDE_ENG = False

# CLONE REPO SAFELY (READ-ONLY)
if not os.path.exists(CLONE_DIR):
    print(f"Cloning repo into '{CLONE_DIR}'...")
    git.Repo.clone_from(REPO_URL, CLONE_DIR)
else:
    print(f"Repository already cloned at '{CLONE_DIR}'")

# FILE EXCLUSION LIST
EXCLUDED_FILES = {
    'ALBA_titles.txt',
    'requirements.txt',
    'corpus.txt',
    'failed.txt',
    'Coinneach Odhar, Am Fiosaiche.txt',
    'Gearr-sgeoil air Sir Seoras Uilleam Ros.txt',
    'transcribers_notes.txt',
    'gdwiki-20240620-pages-articles-multistream-index.txt'
}

# UTILITY: CHECK IF FILE IS ELIGIBLE
def is_valid_file(file, include_eng):
    if file in EXCLUDED_FILES:
        return False
    if not file.endswith('.txt'):
        return False
    if 'eng_' in file and not include_eng:
        return False
    return True

# CREATE OUTPUT DIRECTORY
os.makedirs(OUTPUT_DIR, exist_ok=True)

# PROCESS EACH SOURCE
for source in SOURCES:
    print(f"\nProcessing source: {source}")
    source_path = os.path.join(CLONE_DIR, source)
    output_path = os.path.join(OUTPUT_DIR, source.replace(" ", "_").lower() + ".txt")

    with open(output_path, "w", encoding="utf-8") as out_file:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                if is_valid_file(file, INCLUDE_ENG):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        content = []
                        if "url" in ATTRIBUTES and len(lines) > 0:
                            content.append(lines[0])
                        if "date" in ATTRIBUTES and len(lines) > 1:
                            content.append(lines[1])
                        if "title" in ATTRIBUTES and len(lines) > 2:
                            content.append(lines[2])
                        if "content" in ATTRIBUTES and len(lines) > 3:
                            content.extend(lines[3:])
                        raw_text = "\n".join(content)
                        clean_text = BeautifulSoup(raw_text, "html.parser").text.strip()
                        out_file.write(clean_text + "\n\n")

    print(f"Saved: {output_path}")

print("\n One file per source saved in:", OUTPUT_DIR)


