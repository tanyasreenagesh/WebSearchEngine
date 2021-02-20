# Builds the inverted index

from processing import *
import pickle
import math

def main():

    tempInvertedIdx = dict()
    invertedIdx = dict()            # {token: {doc_id1: tf_idf1, doc_id2: tf_idf2}}
    validTokensInDoc = dict()       # tracks number of valid tokens in each document
    documentsInIdx = set()          # tracks set of documents containing valid words
    
    for folder in range(5):        # 75 
        for file in range(20):     # 500
            currentIdx = str(folder) + "/" + str(file)
            
            tokens = getTokens(currentIdx)
            numOfTokens = 0    # tracks the number of valid tokens in each doc_id
            
            for token in tokens:
                # check for alphanumeric tokens and remove stop words
                currentToken = validToken(token)
                
                if currentToken:
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

    invertedIdx['numOfDocs'] = numOfDocs
        

    # store invertedIdx to invertedIdx.pkl
    f = open("tempInvertedIdx.pkl","wb")
    pickle.dump(invertedIdx, f)
    f.close()

if __name__ == "__main__":
    main()
