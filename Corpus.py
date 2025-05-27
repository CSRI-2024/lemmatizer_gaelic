# -*- coding: utf-8 -*-
"""
Created on Tue Jul 9, 2024

Author: Mark Liberko
"""

import os
from bs4 import BeautifulSoup


class Corpus:
    """
    This class is used to create and then save (download) a corpus as a single unified document
    
    sources - which sources should the corpus contain. Passed as a list of strings. Possible options are:
        "BBC Alba News"
        "Gutenburg Texts"
        "Letters to Learners"
        "Little Letters"
        "Wikipedia Dump"
        Or any other source added after the writing of this script
    Defaults to these five sources (which was everything we had at the time of writing)
        
    attributes - which sections of the existing files should be taken. Passed as a list of strings. Possible options are:
        "url"
        "date"
        "title"
        "content"
    Defaults to title and content
    
    include_eng - a boolean for whether or not to include texts written in English when compiling the corpus file. Defaults to False
    
    
    The following script would create a text file called "corpus.txt" on your local device containing the date and contents of 
    the letters and the little letters:
    
    ```
    corpus = Corpus(sources = ["Little Letters", "Letters to Learners"], attributes = ["date","content"])
    corpus.download("corpus.txt")
    ```
    """
    
    def __init__(self,sources:list[str] = ["BBC Alba News","Gutenburg Texts","Letters to Learners","Little Letters","Wikipedia Dump"],
                 attributes:list[str] = ["title","content"],
                 include_eng = False):
        
        self.sources = sources
        self.attributes = attributes
        self.include_eng = include_eng
        
        self.excluded_files = [
            'ALBA_titles.txt',
            'requirements.txt',
            'corpus.txt',
            'failed.txt',
            'Coinneach Odhar, Am Fiosaiche.txt',
            'Gearr-sgeoil air Sir Seoras Uilleam Ros.txt',
            'transcribers_notes.txt',
            'gdwiki-20240620-pages-articles-multistream-index.txt',
            ] # These files exist within the corpus but don't contain text meant for analysis
        
        # The following generates a list of all paths where text exists
        
        self.file_paths = []
        self.set_file_paths(self.sources)

            
    def set_file_paths(self,sources):
        """
        Is the setter for `self.file_paths`
        sources - a list of source files with the same restrictions as `self.sources`
        """
        temp_file_paths = []
        
        # I apologize for all the nesting
        # The gist is for every file in our sources if it should be added, add it
        for source in sources:
            for root, dirs, files in os.walk(source): # ASSUMES THE WORKING DIRECTORY IS ~\...\Gaelic-Corpus
                for file in files:
                    if self.__text_meets_conditions(file):
                        temp_file_paths.append(os.path.join(root, file)) # Add the path to that file to the list of paths
        
        self.file_paths = temp_file_paths   

        
    def __text_meets_conditions(self,file):
        """
        This method is called during self.set_file_paths
        Can be updated to include more conditions if necessary
        """
        if file in self.excluded_files: # Shouldn't be in excluded files
            return False
        if not file.endswith('.txt'): # Should be a .txt
            return False
        if ('eng_' in file) & (self.include_eng is False): #If it's English don't add it unless specified
            return False
        return True
        
                        
    def download(self,file_name = "corpus.txt"):
        """
        Downloads all files from all sources with the attributes given. Will include English if specified by self.include_eng
        
        file_name - the name of the new text file being created
        """
                        
        if os.path.exists(file_name):
            os.remove("corpus.txt")
        corpus_file = open(file_name, 'a', encoding = 'utf-8') # Open a file to create one file with all texts gathered in it

        for path in self.file_paths: # For each path in the list: 
            
            file = open(path, 'r', encoding = 'utf-8') # Open the pile at that path
            lines = file.readlines() # Read the file 
            
            useful_content = []
            if "url" in self.attributes: # Appending the wanted material to what we'll write to the file
                useful_content.append(lines[0])
            if "date" in self.attributes:
                useful_content.append(lines[1])
            if "title" in self.attributes:
                useful_content.append(lines[2])
            if "content" in self.attributes:
                useful_content.extend(lines[3:]) # .extend() because slicing gives a list, not just one string, so .append() doesn't work
            useful_content = "\n".join(useful_content)           
            useful_content = BeautifulSoup(useful_content,'html.parser') # Just in case any weird html got through
            
            corpus_file.write(str(useful_content)) # Write that content to the corpus file 
            corpus_file.write('\n')
                        
            file.close() 

        corpus_file.close()
    
                        
    def serialize_to_spacy(self,file_name = "corpus.spacy"):
        """
        A method that should be implemented once our tokenizer is incorporated in spaCy
        
        This will create a DocBin object (see https://spacy.io/api/docbin) that consists of the all of the files in `self.file_paths`.
        It will then save it to disk as a .spacy file
        """
        print("This method still needs implementation")
    