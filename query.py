# Queries the inverted index

from processing import *
from tkinter import *


def getResults(rawQuery, invertedIdx, data, resultsText):

    numOfDocs = invertedIdx['numOfDocs']
    print("Number of docs = ", numOfDocs)
    print("Number of tokens = ", len(invertedIdx))

    noResultsMsg = "Sorry, we couldn't find anything related to your search!"

    # calculate query tf-idf scores
    query_wt = computeQueryScores(rawQuery,invertedIdx,numOfDocs)

    # check if there are no valid tokens
    if len(query_wt) == 0:
        resultsText.configure(state='normal', fg="black")
        resultsText.insert(INSERT, noResultsMsg+"\n")
        resultsText.configure(state='disabled')
        return
    
    # query normalization
    normalizeQueryScores(query_wt)

    # compute cosine similarities between query and docs that contain tokens in the query
    scores = getCosineSimilarity(query_wt, invertedIdx)

    resultsText.tag_config('url', foreground="blue")
    
    # display the top 20 results by score
    resultsText.configure(state='normal')
    for title,url,desc in formatResults(scores, data):
        resultsText.insert(END, title+"\n")
        resultsText.insert(END, url+"\n", 'url')
        resultsText.insert(END, desc+"\n\n")
    resultsText.configure(state='disabled')

