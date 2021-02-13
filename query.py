# Queries the inverted index

import json
import pickle
import operator

path = "webpages/WEBPAGES_RAW/bookkeeping.json"
with open(path) as file:
    data = json.load(file)
        
# load from pickle
file = open("invertedIdx.pkl",'rb')
invertedIdx = pickle.load(file)

print("Number of unique words: ", len(invertedIdx))

#print("Inverted Index: \n", invertedIdx)

# User query
query = input("\n\n\nEnter your search query: \n")
while(query != 'q'):
    query = query.lower().split()        

    # rank the results and store in query_result
    query_result = dict()
    for q in query:
        if q in invertedIdx:
            for doc in invertedIdx[q]:
                if doc not in query_result:
                    query_result[doc] = invertedIdx[q][doc]
                else:
                    query_result[doc] += invertedIdx[q][doc]

    # display the top 20 results by rank
    if len(query_result) == 0:
        print("\nSorry, we couldn't find anything related to your search.")
    else:
        resultCount = 0
        print("Number of URLs retrieved = ", len(query_result))
        for k,v in sorted(query_result.items(), key=operator.itemgetter(1), reverse=True):
            resultCount += 1
            if resultCount > 20:
                break
            print(str(resultCount) + ". ", data[k])
            #print(k,v)
        
    query = input("\n\nEnter your search query: \n")
