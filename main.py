# Builds the inverted index

from processing import *

def main():
    
    tempInvertedIdx = dict()
    numOfValidDocs = 0

    # parse files in webpages folders
    for folder in range(75):
        for file in range(500):
            currentIdx = str(folder) + "/" + str(file)
            isValidDoc = False
            
            tokens, titleTokens, bTokens, h1Tokens, h2Tokens, h3Tokens = getTokens(currentIdx)
            
            for token in tokens:
                # check for alphanumeric tokens and remove stop words
                currentToken = validToken(token)

                # insert token into tempInvertedIdx
                if currentToken:
                    isValidDoc = True
                    insertToken(currentToken, currentIdx, tempInvertedIdx)
                    
            if isValidDoc: 
                numOfValidDocs += 1
                
            # assign weights to tokens in important HTML tags
            assignWeights(tempInvertedIdx, currentIdx,
                          [(titleTokens,3),(h1Tokens,2),(h2Tokens,1.5),(h3Tokens,1),(bTokens,0.5)])

            if currentIdx == "74/496":
                break

    # store the tf-idf score
    invertedIdx, docIdx = computeIndexScores(tempInvertedIdx, numOfValidDocs)

    # normalization
    normalizeIndexScores(invertedIdx, docIdx)
    
    # save numOfValidDocs for use in querying
    invertedIdx['numOfDocs'] = numOfValidDocs

    # compress and save to pickle file
    compressPickle('invertedIdx', invertedIdx)

if __name__ == "__main__":
    main()
