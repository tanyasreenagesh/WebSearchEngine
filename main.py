# Builds the inverted index

from processing import *

def main():
    
    tempInvertedIdx = dict()
    invertedIdx = dict()            # {token: {doc_id1: tf_idf1, doc_id2: tf_idf2}}
    validTokensInDoc = dict()       # tracks number of valid tokens in each document
    documentsInIdx = set()          # tracks set of documents containing valid words
    
    for folder in range(75):        # 75 
        for file in range(500):     # 500
            currentIdx = str(folder) + "/" + str(file)
            
            tokens, titleTokens, bTokens, h1Tokens, h2Tokens, h3Tokens = getTokens(currentIdx)
            numOfTokens = 0    # tracks the number of valid tokens in each doc_id
            
            for token in tokens:
                # check for alphanumeric tokens and remove stop words
                currentToken = validToken(token)
                
                if currentToken:
                    numOfTokens += 1

                    # insert in temp inverted index with doc_id
                    if currentToken not in tempInvertedIdx:
                        tempInvertedIdx[currentToken] = {currentIdx: [1,1]} 
                    elif currentIdx not in tempInvertedIdx[currentToken]:
                        tempInvertedIdx[currentToken][currentIdx] = [1,1]
                    else:
                        tempInvertedIdx[currentToken][currentIdx][0] += 1
                    
                    documentsInIdx.add(currentIdx)

            # store the number of valid tokens
            validTokensInDoc[currentIdx] = numOfTokens

            # assign weights to tokens in important HTML tags
            assignWeights(tempInvertedIdx, currentIdx,
                          [(titleTokens,3),(h1Tokens,2),(h2Tokens,1.5),(h3Tokens,1),(bTokens,0.5)])

            if currentIdx == "74/496":
                break

    # store the tf-idf score (rounded to nearest 7 digits)
    numOfDocs = len(documentsInIdx)
    for term in tempInvertedIdx:
        invertedIdx[term] = {}
        idf = math.log(numOfDocs/(len(tempInvertedIdx[term])+1))
        for doc in tempInvertedIdx[term]:
            tf = tempInvertedIdx[term][doc][0]/validTokensInDoc[doc]
            invertedIdx[term][doc] = round(tf*idf*tempInvertedIdx[term][doc][1],7)

    invertedIdx['numOfDocs'] = numOfDocs

    # create the docIdx
    docIdx = dict()     # {doc_id: {token: tf-idf}}
    for token,docs in invertedIdx.items():
        if token == "numOfDocs":
            continue
        for doc,score in docs.items():
            if doc not in docIdx:
                docIdx[doc] = dict()
            docIdx[doc][token] = invertedIdx[token][doc]

    # compress and save to pickle files
    compressPickle('invertedIdx', invertedIdx)
    compressPickle('docIdx', docIdx)

if __name__ == "__main__":
    main()
