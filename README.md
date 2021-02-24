# web-search-engine
Search engine that maintains an inverted index of webpages and allows users to query ranked results.

Creating the inverted index:
~~~
python main.py
~~~
You may have to change variables *path* and *pathToWebpages* in main.py before running the file, depending on your file structure.

Unless any changes have been made to the way we create our inverted index, there is no need to run this file. Simply download the pickle file (invertedIdx.pkl from invertedIdx.zip), extract the pickle file, and run the search engine to query the webpages.

To run the search engine: 
~~~
python query.py
~~~
Type 'q' in the query to end the program.


### TO-DO:
1. Extra credit (GUI, indexing anchor words, etc.)
2. Modify file directory tree (as specified in project description)


### Instructions for TA/Grading Team:

Install the following (using pip/conda):
1. bs4
2. pandas

Run main.py to create the inverted index (the index will be saved as a feather file).

Run query.py to input search queries and get results.
