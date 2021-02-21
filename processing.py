import re
from nltk.stem import WordNetLemmatizer
import json
import codecs
from bs4 import BeautifulSoup
from nltk import word_tokenize

path = "webpages/WEBPAGES_RAW/bookkeeping.json"
with open(path) as file:
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

def validToken(token):
    if type(token) == str and len(token) > 1 and re.match("^[A-Za-z]*$", token) and token.lower() not in stopWords:
        lemmatizer = WordNetLemmatizer()
        return lemmatizer.lemmatize(token.lower())
    else:
        return False

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

def getTokens(docID, output=True):
    pathToWebpages = "webpages/WEBPAGES_RAW/"
    fileName = pathToWebpages + docID
    url = data[docID]
    
    if output:
        print(str(docID), " : ", url)

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

def assignWeights(invertedIdx, doc, inputList):
    for tokens,weight in inputList:
        for token in tokens:
            if token in invertedIdx and doc in invertedIdx[token]:
                invertedIdx[token][doc][1] += weight
