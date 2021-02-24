# Queries the inverted index

from processing import *

path = "webpages/WEBPAGES_RAW/bookkeeping.json"
with open(path) as file:
    data = json.load(file)
        
# load and decompress invertedIdx from pickle file
invertedIdx = decompressPickle('invertedIdx.pbz2')

numOfDocs = invertedIdx['numOfDocs']
print("Number of docs = ", numOfDocs)
print("Number of tokens = ",len(invertedIdx))

# User query
rawQuery = input("\n\n\nEnter your search query (or 'q' to quit): \n")
while(rawQuery != 'q'):

    # calculate query tf-idf scores
    query_wt = computeQueryScores(rawQuery,invertedIdx,numOfDocs)

    # check if there are no valid tokens
    if len(query_wt) == 0:
        print("\nSorry, we couldn't find anything related to your search.")
        rawQuery = input("\n\nEnter your search query: \n")
        continue
    
    # query normalization
    normalizeQueryScores(query_wt)

    # compute cosine similarities between query and docs that contain tokens in the query
    scores = getCosineSimilarity(query_wt, invertedIdx)
    
    # display the top 20 results by score
    showResults(scores)

    # get user input until 'q' is entered
    rawQuery = input("\n\nEnter your search query (or 'q' to quit): \n")
