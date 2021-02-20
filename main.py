# Builds the inverted index


import json
import pickle
import re
import codecs
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import math

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





def main():
    
    lemmatizer = WordNetLemmatizer()
    
    path = "/Users/Aishah/Documents/GitHub/webpages/WEBPAGES_RAW/bookkeeping.json"#"webpages/WEBPAGES_RAW/bookkeeping.json"
    with open(path) as file:
        data = json.load(file)

    tempInvertedIdx = dict()
    invertedIdx = dict()            # {token: {doc_id1: [tf_idf1, word_importance_score], doc_id2: tf_idf2}}
    validTokensInDoc = dict()       # tracks number of valid tokens in each document
    documentsInIdx = set()          # tracks set of documents containing valid words
    pathToWebpages = '/Users/Aishah/Documents/GitHub/webpages/WEBPAGES_RAW/' #"webpages/WEBPAGES_RAW/"
    

    for folder in range(2):        # 75 
        for file in range(500):     # 500
            currentIdx = str(folder) + "/" + str(file)
            fileName = pathToWebpages + currentIdx
            url = data[currentIdx]
            print(str(currentIdx), " : ", url)

            file = codecs.open(fileName, "r", "utf-8")
    
            soup = BeautifulSoup(file.read(), features="lxml")


            # Find all content in title tags.
            title_text = list(''.join(s.findAll(text=True)) for s in soup.findAll('title'))
            title_tokens_all = []
            title_tokens = []
            for text in title_text:
                title_tokens_all += word_tokenize(text)
            for token in title_tokens_all:
                if len(token) > 1 and re.match("^[A-Za-z]*$", token) and token.lower() not in stopWords:
                    title_tokens.append(lemmatizer.lemmatize(token.lower()))



            # Find all content in b tags. (bold)
            b_text = list(''.join(s.findAll(text=True)) for s in soup.findAll('b'))
            b_tokens_all = []
            b_tokens = []
            for text in b_text:
                b_tokens_all += word_tokenize(text)
            for token in b_tokens_all:
                if len(token) > 1 and re.match("^[A-Za-z]*$", token) and token.lower() not in stopWords:
                    b_tokens.append(lemmatizer.lemmatize(token.lower()))


            # Find all content in h1 tags.
            h1_text = list(''.join(s.findAll(text=True)) for s in soup.findAll('h1'))
            h1_tokens_all = []
            h1_tokens = []
            for text in h1_text:
                h1_tokens_all += word_tokenize(text)
            #print()
            for token in h1_tokens_all:
                if len(token) > 1 and re.match("^[A-Za-z]*$", token) and token.lower() not in stopWords:
                    h1_tokens.append(lemmatizer.lemmatize(token.lower()))
            

            # Find all content in h2 tags.
            h2_text = list(''.join(s.findAll(text=True)) for s in soup.findAll('h2'))
            h2_tokens_all = []
            h2_tokens = []
            for text in h2_text:
                h2_tokens_all += word_tokenize(text)
            for token in h2_tokens_all:
                if len(token) > 1 and re.match("^[A-Za-z]*$", token) and token.lower() not in stopWords:
                    h2_tokens.append(lemmatizer.lemmatize(token.lower()))

            # Find all content in h3 tags.
            h3_text = list(''.join(s.findAll(text=True)) for s in soup.findAll('h3'))
            h3_tokens = []
            h3_tokens_all = []
            for text in h3_text:
                h3_tokens_all += word_tokenize(text)
            for token in h3_tokens_all:
                if len(token) > 1 and re.match("^[A-Za-z]*$", token) and token.lower() not in stopWords:
                    h3_tokens.append(lemmatizer.lemmatize(token.lower()))


            content = soup.get_text()
            tokens = word_tokenize(content)
            
            numOfTokens = 0    # tracks the number of valid tokens in each doc_id
            
            for token in tokens:

                # check for alphanumeric tokens and remove stop words
                if len(token) > 1 and re.match("^[A-Za-z]*$", token) and token.lower() not in stopWords:
                    currentToken = lemmatizer.lemmatize(token.lower())      # lemmatize and lower
                    numOfTokens += 1
                    
                    
                    # insert in temp inverted index with doc_id
                    if currentToken not in tempInvertedIdx:
                        #if (currentToken in h1_tokens):
                        #    print(currentToken, " : ", 'True', end = ', ')
                        tempInvertedIdx[currentToken] = {currentIdx: [1, 0]} # Initiate the score for each token to 0. 
                    elif currentIdx not in tempInvertedIdx[currentToken]:
                        tempInvertedIdx[currentToken][currentIdx] = [1, 0]
                    else:
                        tempInvertedIdx[currentToken][currentIdx][0] += 1
                    
                    documentsInIdx.add(currentIdx)

            # store the number of valid tokens
            validTokensInDoc[currentIdx] = numOfTokens

            file.close()
            
            # Below, increment the score for each document if the token is in the doc and it's h1, h2, or h3.
            
            for token in h1_tokens:
                try:
                    if(token in tempInvertedIdx.keys()):
                        tempInvertedIdx[token][currentIdx][1] += 5
                except:
                    
                    pass

            for token in h2_tokens:
                try:
                    if(token in tempInvertedIdx.keys()):
                        tempInvertedIdx[token][currentIdx][1] += 4
                except:
                    
                    pass

            for token in h3_tokens:
                try:
                    if(token in tempInvertedIdx.keys()):
                        # print(token)
                        tempInvertedIdx[token][currentIdx][1] += 3
                except:
                    
                    pass

    

            if currentIdx == "74/496":
                break


    # store the tf-idf score (rounded to nearest 7 digits)
    numOfDocs = len(documentsInIdx)
    for term in tempInvertedIdx:
        invertedIdx[term] = {}
        idf = math.log(numOfDocs/(len(tempInvertedIdx[term])+1))
        for doc in tempInvertedIdx[term]:
            tf = tempInvertedIdx[term][doc][0]/validTokensInDoc[doc]
            invertedIdx[term][doc] = [round(tf*idf,7), tempInvertedIdx[term][doc][1]]     # store it in the final invertedIdx

    #print(invertedIdx)
    #print()
    #print()
    print("count: ", count)
    
        

    # store invertedIdx to invertedIdx.pkl
    f = open("invertedIdx.pkl","wb")
    pickle.dump(invertedIdx, f)
    f.close()

if __name__ == "__main__":
    main()
