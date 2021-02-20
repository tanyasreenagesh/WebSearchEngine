# Queries the inverted index

from processing import *
import pickle
import operator
import math

path = "webpages/WEBPAGES_RAW/bookkeeping.json"
with open(path) as file:
    data = json.load(file)
        
# load from pickle
file = open("tempInvertedIdx.pkl",'rb')
invertedIdx = pickle.load(file)

print("Number of unique words: ", len(invertedIdx))

print("Inverted Index: \n", invertedIdx)

# User query
rawQuery = input("\n\n\nEnter your search query: \n")
while(rawQuery != 'q'):
    rawQuery = rawQuery.split()

    # remove stop words, non-alpha words, etc.
    query = []
    for q in rawQuery:
        token = validToken(q)
        if token:
            query.append(token)

    # compute cosine similarities
    scores = dict()         # {doc_id: cosine_score}

    # calculate query tf-idf scores
    query_wt = dict()
    for q in query:
        if q in invertedIdx:
            tf = query.count(q)/len(q)
            idf = math.log(invertedIdx['numOfDocs']/(len(invertedIdx[q])+1)) 
            query_wt[q] = round(tf*idf,7)

    # calculate document tf-idf scores
    for q in query_wt:
        doc_wt = dict()

        for doc in invertedIdx[q]:
            tokens = getTokens(doc, False)
            for token in tokens:
                currentToken = validToken(token)
                if currentToken:
                    doc_wt[currentToken] = invertedIdx[currentToken][doc]

            # calculate cosine similarity between doc and query
            scores[doc] = 0
            for q in query_wt:
                if q in doc_wt:
                    scores[doc] += doc_wt[q] * query_wt[q]
            
    #print(scores)

    # display the top 20 results by scores rank
    if len(scores) == 0:
        print("\nSorry, we couldn't find anything related to your search.")
    else:
        resultCount = 0
        print("Number of URLs retrieved = ", len(scores))
        for k,v in sorted(scores.items(), key=operator.itemgetter(1), reverse=True):
            resultCount += 1
            if resultCount > 20:
                break
            print(str(resultCount) + ". ", data[k])
            #print(k,v)

    # get user input until 'q' is entered
    rawQuery = input("\n\nEnter your search query: \n")
