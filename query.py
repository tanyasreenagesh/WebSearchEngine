# Queries the inverted index

from processing import *

path = "webpages/WEBPAGES_RAW/bookkeeping.json"
with open(path) as file:
    data = json.load(file)
        
# load and decompress invertedIdx and docIdx from pickle files
invertedIdx = decompressPickle('invertedIdx.pbz2')
docIdx = decompressPickle('docIdx.pbz2')

numOfDocs = invertedIdx['numOfDocs']
print("Number of docs = ", numOfDocs)
print("Number of tokens = ",len(invertedIdx))

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

    # calculate query tf-idf scores
    query_wt = dict()
    for q in query:
        if q in invertedIdx:      
            tf = query.count(q)/len(query)     
            idf = math.log(numOfDocs/(len(invertedIdx[q])+1)) 
            query_wt[q] = round(tf*idf,7)


    # compute cosine similarities
    scores = dict()         # {doc_id: cosine_score}
    
    for q in query_wt:
        for doc in invertedIdx[q]:
            if doc in scores:
                scores[doc] += invertedIdx[q][doc] * query_wt[q]
            else:
                scores[doc] = invertedIdx[q][doc] * query_wt[q]

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

    # get user input until 'q' is entered
    rawQuery = input("\n\nEnter your search query: \n")
