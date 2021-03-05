import re
import nltk
nltk.download("wordnet")
nltk.download("punkt")
from nltk.stem import WordNetLemmatizer
import json
import codecs
from bs4 import BeautifulSoup
from nltk import word_tokenize
from datetime import datetime
import bz2
import pickle
import _pickle as cPickle
import operator
import math
import pandas as pd
import tkinter as tk
from tkinter import *

pathToWebpages = "webpages/WEBPAGES_RAW/"
pathToBook = "webpages/WEBPAGES_RAW/bookkeeping.json"

with open(pathToBook) as file:
    data = json.load(file)
        
stopWords = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out',
             'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into',
             'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the',
             'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were',
             'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while','above', 'both', 'up', 'to',
             'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have',
             'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can',
             'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
             'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
             'doing', 'it', 'how', 'further', 'was', 'here', 'than'}


# Returns the lemmatized token if token is valid, False otherwise
def validToken(token):
    if type(token) == str and len(token) > 1 and re.match("^[A-Za-z]*$", token) and token.lower() not in stopWords:
        lemmatizer = WordNetLemmatizer()
        return lemmatizer.lemmatize(token.lower())
    else:
        return False


# returns list of valid tokens from HTML content
def getTextFromTags(soup, tag):
    textInTag = list(''.join(s.findAll(text=True)) for s in soup.findAll(tag))
    allTokens = []
    tagTokens = []
    for text in textInTag:
        allTokens += word_tokenize(text)
    for token in allTokens:
        currToken = validToken(token)
        if currToken:
            tagTokens.append(currToken)
    return tagTokens


# Returns tokens from docID including lists of tokens in important HTML tags
def getTokens(docID, output=True):
    fileName = pathToWebpages + docID
    url = data[docID]
    
    if output:
        print(datetime.now().strftime("%H:%M"), str(docID), " : ", url)

    file = codecs.open(fileName, "r", "utf-8")

    soup = BeautifulSoup(file.read(), features="lxml")

    title_tokens = getTextFromTags(soup, 'title')
    b_tokens = getTextFromTags(soup, 'b')
    h1_tokens = getTextFromTags(soup, 'h1')
    h2_tokens = getTextFromTags(soup, 'h2')
    h3_tokens = getTextFromTags(soup, 'h3')
    
    content = soup.get_text()
    
    file.close()
    
    return word_tokenize(content), title_tokens, b_tokens, h1_tokens, h2_tokens, h3_tokens


# Assigns weights to tokens in important HTML tags
def assignWeights(invertedIdx, doc, inputList):
    for tokens,weight in inputList:
        for token in tokens:
            if token in invertedIdx and doc in invertedIdx[token]:
                invertedIdx[token][doc][1] += weight


# Compresses a pickle file
def compressPickle(fName, data):
    with bz2.BZ2File(fName + '.pbz2', 'w') as f: 
        cPickle.dump(data, f)


# Decompresses a pickle file
def decompressPickle(fName):
    data = bz2.BZ2File(fName, 'rb')
    data = cPickle.load(data)
    return data


# Inserts the (token,doc) pair into the index
def insertToken(token, doc, idx):
    if token not in idx:
        idx[token] = {doc: [1,1]} 
    elif doc not in idx[token]:
        idx[token][doc] = [1,1]
    else:
        idx[token][doc][0] += 1


# Returns tf-idf scores for tokens in index
def computeIndexScores(tempInvertedIdx, numOfValidDocs):
    invertedIdx = dict()            # {token:   {doc_id1:   tf_idf1}}
    docIdx = dict()                 # {doc_id:  {token:     tf-idf}}

    # store the tf-idf score (rounded to nearest 7 digits)
    for term in tempInvertedIdx:
        invertedIdx[term] = {}
        idf = math.log(numOfValidDocs/len(tempInvertedIdx[term]))
        for doc in tempInvertedIdx[term]:
            tf = 1+math.log(tempInvertedIdx[term][doc][0])
            invertedIdx[term][doc] = round(tf*idf*tempInvertedIdx[term][doc][1],7)
            
            # add to docIdx
            if doc not in docIdx:
                docIdx[doc] = dict()
            docIdx[doc][term] = invertedIdx[term][doc]
            
    return invertedIdx, docIdx


# Returns tf-idf scores for tokens in query
def computeQueryScores(rawQuery,invertedIdx,numOfDocs):
    rawQuery = word_tokenize(rawQuery)
    
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
            tf = 1+math.log(query.count(q))    
            idf = math.log(numOfDocs/len(invertedIdx[q])) 
            query_wt[q] = round(tf*idf,7)
    return query_wt


# Normalizes document tf-idf scores for all documents
def normalizeIndexScores(invertedIdx, docIdx):
    for doc in docIdx:
        norm = 1/math.sqrt(sum(i*i for i in docIdx[doc].values()))
        for token in docIdx[doc]:
            invertedIdx[token][doc] = round(norm*invertedIdx[token][doc],7)


# Normalizes query tf-idf scores
def normalizeQueryScores(query_wt):
    norm = 1/math.sqrt(sum(i*i for i in query_wt.values()))
    for q in query_wt:
        query_wt[q] = round(norm*query_wt[q],7)


# Returns cosine similarity of query and all the docs in the index
def getCosineSimilarity(query_wt, invertedIdx):
    scores = dict()         # {doc_id: cosine_score}
    
    for q in query_wt:
        for doc in invertedIdx[q]:
            if doc in scores:
                scores[doc] += invertedIdx[q][doc] * query_wt[q]
            else:
                scores[doc] = invertedIdx[q][doc] * query_wt[q]
    return scores


# Makes text more readable
def format(text):
    text = text.strip().replace("\n", " ").replace("\t", " ")
    if len(text) > 1:
        text = text[0].upper() + text[1:]
    return text


# Gets the title of the doc
def getTitle(soup):
    return format(soup.find('title').get_text())


# Gets the description of the doc
def getDescription(soup):
    try:
        text = format(soup.find('p').get_text())
        text = text.partition('.')[0] + '.'
    except:
        text = ''
    return text


# Returns the top 20 results of the query, ranked by scores
def rankResults(scores, data):
    results = ""
    resultCount = 0

    print()
    for k,v in sorted(scores.items(), key=operator.itemgetter(1), reverse=True):
        resultCount += 1
        if resultCount > 20:
            break
        print(str(resultCount) + ". ", data[k])

        # Process url to make soup
        url = data[k]
        fileName = pathToWebpages + k        
        file = codecs.open(fileName, "r", "utf-8")
        soup = BeautifulSoup(file.read(), features="lxml")

        yield getTitle(soup), data[k], getDescription(soup)
    print()