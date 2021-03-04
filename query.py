# Queries the inverted index

from processing import *

# Returns the top 20 ranked results for given raw query
def getResults(rawQuery, invertedIdx, data, resultsText):

    numOfDocs = invertedIdx['numOfDocs']

    noResultsMsg = "Sorry, we couldn't find anything related to your search!"

    # Calculate query tf-idf scores
    query_wt = computeQueryScores(rawQuery,invertedIdx,numOfDocs)

    # Check if there are no valid tokens
    if len(query_wt) == 0:
        resultsText.configure(state='normal')
        resultsText.insert(INSERT, noResultsMsg+"\n")
        resultsText.configure(state='disabled')
        return
    
    # Query normalization
    normalizeQueryScores(query_wt)

    # Compute cosine similarities between query and docs that contain tokens in the query
    scores = getCosineSimilarity(query_wt, invertedIdx)
    
    # Display the top 20 results by score (rank)
    resultsText.configure(state='normal')
    resultsText.insert(END,"We found " + str(len(scores)) + " result(s) for your search.\n\n", 'url_count')
    for title,url,desc in rankResults(scores, data):
        if len(title) > 2:
            resultsText.insert(END, title+"\n", 'title')
        resultsText.insert(END, url+"\n", 'url')
        if len(desc) > 2:
            resultsText.insert(END, desc+"\n", 'desc')
        resultsText.insert(END, "\n")
    resultsText.configure(state='disabled')

