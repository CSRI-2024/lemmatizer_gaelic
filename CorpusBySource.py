import os
from bs4 import BeautifulSoup
from Corpus import Corpus  # Make sure Corpus.py is in the same directory or a module

def download_by_source(self, output_dir="by_source_corpus"):
    """
    Saves separate corpus files for each source, preserving all original rules and filtering logic.
    Each file contains only the texts from that source, cleaned and structured based on the specified attributes.
    """
    os.makedirs(output_dir, exist_ok=True)

    for source in self.sources:
        output_path = os.path.join(output_dir, source.lower().replace(" ", "_") + ".txt")

        if os.path.exists(output_path):
            os.remove(output_path)

        with open(output_path, 'a', encoding='utf-8') as corpus_file:
            for root, dirs, files in os.walk(source):
                for file in files:
                    if not self.__text_meets_conditions(file):
                        continue

                    file_path = os.path.join(root, file)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                    except Exception as e:
                        print(f"⚠️ Failed to read {file_path}: {e}")
                        continue

                    useful_content = []

                    if "url" in self.attributes and len(lines) > 0:
                        useful_content.append(lines[0])
                    if "date" in self.attributes and len(lines) > 1:
                        useful_content.append(lines[1])
                    if "title" in self.attributes and len(lines) > 2:
                        useful_content.append(lines[2])
                    if "content" in self.attributes and len(lines) > 3:
                        useful_content.extend(lines[3:])

                    cleaned = BeautifulSoup("\n".join(useful_content), 'html.parser').get_text()
                    corpus_file.write(cleaned + "\n\n")

#  Monkey-patch the method into the class (quick way to extend a class externally)
Corpus.download_by_source = download_by_source

#  Use the method
corpus5 = Corpus(
    sources=["BBC Alba News", "Gutenberg Texts", "Letters to Learners", "Little Letters", "Wikipedia Dump"],
    include_eng=False
)

corpus5.download_by_source()
