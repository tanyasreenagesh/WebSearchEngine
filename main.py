# Builds the inverted index

import json
import pickle
import re
import codecs
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import math

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

    tempInvertedIdx = dict()
    invertedIdx = dict()            # {token: {doc_id1: tf_idf1, doc_id2: tf_idf2}}
    validTokensInDoc = dict()       # tracks number of valid tokens in each document
    documentsInIdx = set()          # tracks set of documents containing valid words
    pathToWebpages = "webpages/WEBPAGES_RAW/"
    
    for folder in range(75):        # 75 
        for file in range(500):     # 500
            currentIdx = str(folder) + "/" + str(file)
            fileName = pathToWebpages + currentIdx
            url = data[currentIdx]
            print(str(currentIdx), " : ", url)

            file = codecs.open(fileName, "r", "utf-8")
    
            content = BeautifulSoup(file.read(), features="lxml").get_text()
            tokens = word_tokenize(content)
            
            numOfTokens = 0    # tracks the number of valid tokens in each doc_id
            
            for token in tokens:
                # check for alphanumeric tokens and remove stop words
                if len(token) > 1 and re.match("^[A-Za-z]*$", token) and token.lower() not in stopWords:
                    currentToken = lemmatizer.lemmatize(token.lower())      # lemmatize and lower
                    numOfTokens += 1

                    # insert in temp inverted index with doc_id
                    if currentToken not in tempInvertedIdx:
                        tempInvertedIdx[currentToken] = {currentIdx: 1} 
                    elif currentIdx not in tempInvertedIdx[currentToken]:
                        tempInvertedIdx[currentToken][currentIdx] = 1
                    else:
                        tempInvertedIdx[currentToken][currentIdx] += 1
                    
                    documentsInIdx.add(currentIdx)

            # store the number of valid tokens
            validTokensInDoc[currentIdx] = numOfTokens

            file.close()

            if currentIdx == "74/496":
                break

    # store the tf-idf score (rounded to nearest 7 digits)
    numOfDocs = len(documentsInIdx)
    for term in tempInvertedIdx:
        invertedIdx[term] = {}
        idf = math.log(numOfDocs/(len(tempInvertedIdx[term])+1))
        for doc in tempInvertedIdx[term]:
            tf = tempInvertedIdx[term][doc]/validTokensInDoc[doc]
            invertedIdx[term][doc] = round(tf*idf,7)      # store it in the final invertedIdx
        

    # store invertedIdx to invertedIdx.pkl
    f = open("tempInvertedIdx.pkl","wb")
    pickle.dump(invertedIdx, f)
    f.close()

if __name__ == "__main__":
    main()
