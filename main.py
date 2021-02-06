# Search Engine
# Milestone 1: Build an index and query the index for links

import json
import pickle
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

    invertedIdx = dict()        # token: [doc_id1, doc_id2] 
    pathToWebpages = "webpages/WEBPAGES_RAW/"
    
    for folder in range(75):     
        for file in range(500):  
            currentIdx = str(folder) + "/" + str(file)
            fileName = pathToWebpages + currentIdx
            url = data[currentIdx]
            print(str(currentIdx), " : ", url)

            file = codecs.open(fileName, "r", "utf-8")
    
            content = BeautifulSoup(file.read(), features="lxml").get_text()
            tokens = word_tokenize(content)
            
            for token in tokens:
                # check for alphanumeric tokens and remove stop words
                if len(token) > 1 and re.match("^[A-Za-z]*$", token) and token.lower() not in stopWords:
                    currentToken = lemmatizer.lemmatize(token.lower())      # lemmatize and lower

                    # insert in inverted index with doc_id
                    if currentToken not in invertedIdx:
                        invertedIdx[currentToken] = {currentIdx: 1}
                    else:
                        # check if doc_id already stored for token
                        if currentIdx not in invertedIdx[currentToken]:
                            invertedIdx[currentToken][currentIdx] = 1
                        else:
                            invertedIdx[currentToken][currentIdx] += 1

            file.close()

            if currentIdx == "74/496":
                break

    # store to pickle
    f = open("invertedIdx.pkl","wb")
    pickle.dump(invertedIdx, f)
    f.close()
    

if __name__ == "__main__":
    main()
