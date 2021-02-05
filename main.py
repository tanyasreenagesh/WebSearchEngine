# Search Engine
# Milestone 1: Build an index and query the index for links

import json
import re
import codecs
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer 

stopWords = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out',
             'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into',
             'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the',
             'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were',
             'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while','above', 'both', 'up', 'to',
             'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have',
             'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can',
             'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
             'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
             'doing', 'it', 'how', 'further', 'was', 'here', 'than'}

def main():
    lemmatizer = WordNetLemmatizer()
    
    path = "webpages/WEBPAGES_RAW/bookkeeping.json"
    with open(path) as file:
        data = json.load(file)

    final_tokens = []   # put inside double for loop
    invertedIdx = dict()        # token: [doc_id1, doc_id2]   # change value to linked list?
    pathToWebpages = "webpages/WEBPAGES_RAW/"
    
    for folder in range(75):     # 75
        for file in range(500):  # 500
            currentIdx = str(folder) + "/" + str(file)
            fileName = pathToWebpages + currentIdx
            url = data[currentIdx]
            print(str(currentIdx), " : ", url)

            file = codecs.open(fileName, "r", "utf-8")
    
            content = BeautifulSoup(file.read(), features="lxml").get_text()
            tokens = word_tokenize(content)
            
            for token in tokens:
                # check for alphanumeric tokens and remove stop words
                if len(token) > 1 and re.match("^[A-Za-z]*$", token) and token not in stopWords:
                    currentToken = lemmatizer.lemmatize(token.lower())
                    final_tokens.append(currentToken)    # lemmatize and lower

                    # insert in inverted index with doc_id
                    if currentToken not in invertedIdx:
                        invertedIdx[currentToken] = []
                    # check if doc_id already stored for token
                    if currentIdx not in invertedIdx[currentToken]:
                        invertedIdx[currentToken].append(currentIdx)

            file.close()

            if currentIdx == "74/496":
                break

    print("\n\n\n", invertedIdx, "\n\n\n")

    # User query
    query = input("Enter your search query: \n")
    while(query != 'q'):
        if query not in invertedIdx:
            print("\nSorry, we couldn't find anything related to your search.")
        else:
            print("\nHere's what we found:")
            resultCount = 0
            for result in invertedIdx[query]:
                resultCount += 1
                print(str(resultCount) + ". ", data[result])
        query = input("\n\nEnter your search query: \n")
    

if __name__ == "__main__":
    main()
