# Builds the inverted index

from processing import *


# Creates the inverted index
def createIndex():
    
    tempInvertedIdx = dict()
    numOfValidDocs = 0

    # Parse files in webpages folders
    for folder in range(75):
        for file in range(500):
            currentIdx = str(folder) + "/" + str(file)
            isValidDoc = False
            
            tokens, titleTokens, bTokens, h1Tokens, h2Tokens, h3Tokens = getTokens(currentIdx)
            
            for token in tokens:
                # Check for alphanumeric tokens and remove stop words
                currentToken = validToken(token)

                # Insert token into tempInvertedIdx
                if currentToken:
                    isValidDoc = True
                    insertToken(currentToken, currentIdx, tempInvertedIdx)
                    
            if isValidDoc: 
                numOfValidDocs += 1
                
            # Assign weights to tokens in important HTML tags
            assignWeights(tempInvertedIdx, currentIdx,
                          [(titleTokens,3),(h1Tokens,2),(h2Tokens,1.5),(h3Tokens,1),(bTokens,0.5)])

            if currentIdx == "74/496":
                break

    # Store the tf-idf score
    invertedIdx, docIdx = computeIndexScores(tempInvertedIdx, numOfValidDocs)

    # Normalization
    normalizeIndexScores(invertedIdx, docIdx)
    
    # Save numOfValidDocs for use in querying
    invertedIdx['numOfDocs'] = numOfValidDocs

    # Compress and save to pickle file
    compressPickle('invertedIdx', invertedIdx)

createIndex()
