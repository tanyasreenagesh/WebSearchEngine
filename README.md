# web-search-engine

### Instructions for TA/Grading Team:

### Required Installations:

Install the following (using pip/conda):
1. bs4
2. pandas
3. nltk

### Specify File Paths:

You may have to change the pathToWebpages (file path to webpages folder) and pathToBook (file path to JSON bookkeeping file) variables depending on your directory structure.

To change these variables, go to processing.py and specify your file paths on lines 20-21.

### Running the Code:

Run main.py to create the inverted index (the index will be saved locally as a compressed pickle file - invertedIdk.pbz2).

Run gui.py to start the GUI where you may input search queries and get results.

### Brief Description of the Python Files:

1. indexer.py:     Create the inverted index and save it to the pickle file invertedIdx.pkl
2. processing.py:  Most of the functions for this python project can be found in this file. It provides all the functions that indexer.py calls to create the 
                   inverted index, such as creating a list of tokens from an HTML file, lemmatizing and classifying the tokens as valid or not, assigning specific 
                   weights to tokens in certain HTML tags (such as headers, titles etc.), inserting the (token, doc) pair into the index and computing tf-idf score 
                   for the tokens.  It also computes tf-idf score for tokens in the query, normalizes these scores, and computes and returns co-sine similarity of 
                   the query and all the documents in the index. Additionally, it retrieves tokens from a docID, and compresses and decompresses the pickle file. 
                   Finally, it contains functions whose results are passed to gui.py, such as functions to retrive the title of a doc, a description of a doc, and 
                   the top 20 results of the query.
3. gui.py:         Creates the GUI.
4. query.py:       Ranks the top 20 results of the query by their score after calling the respective functions from processing.py, and passes this to the GUI.
