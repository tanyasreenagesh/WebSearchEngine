import json
import pickle

path = "webpages/WEBPAGES_RAW/bookkeeping.json"
with open(path) as file:
    data = json.load(file)
        
# load from pickle
file = open("invertedIdx.pkl",'rb')
invertedIdx = pickle.load(file)

print("Number of unique words: ", len(invertedIdx))

# User query
query = input("Enter your search query: \n")
while(query != 'q'):
    query = query.lower()
    if query not in invertedIdx:
        print("\nSorry, we couldn't find anything related to your search.")
    else:
        print("\nHere's what we found:")
        resultCount = 0
        resultList = invertedIdx[query]
        print("Number of URLs retrieved = ", len(resultList))
        for result in resultList:
            resultCount += 1
            if resultCount > 20:
                break
            print(str(resultCount) + ". ", data[result])
    query = input("\n\nEnter your search query: \n")
