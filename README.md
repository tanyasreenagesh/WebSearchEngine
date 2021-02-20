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

TO-DO:
1. Change tf formula to log
2. Complete weighing for important html tags
3. Indices of occurrence within the document
4. Extra credit (GUI, indexing anchor words, etc.)
