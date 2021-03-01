import tkinter as tk
import tkinter.font as tkFont
import json
import pickle
import operator

path = "webpages/WEBPAGES_RAW/bookkeeping.json"
with open(path) as file:
    data = json.load(file)
        
# load from pickle
file = open("invertedIdx.pkl",'rb')
invertedIdx = pickle.load(file)

def searchQuery():
    query = app.query_box.get(1.0, tk.END+"-1c")

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
    display_result = ""
    if len(query_result) == 0:
        display_result = "\nSorry, we couldn't find anything related to your search."
    else:
        resultCount = 0
        print("Number of URLs retrieved = ", len(query_result))
        for k,v in sorted(query_result.items(), key=operator.itemgetter(1), reverse=True):
            resultCount += 1
            if resultCount > 20:
                break
            display_result += (str(resultCount) + ". " + data[k] + "\n")

    app.show_result = tk.Label(text=display_result)
    app.show_result.place(x=0, y=50)
    
app = tk.Tk()
app.geometry("600x400")
app.title("UCI ICS Search Engine")

fontStyle = tkFont.Font(family="Lucida Grande", size=10)

app.query_box = tk.Text(height=1, width=40)
app.query_box.pack()

app.search_btn = tk.Button(text="Search", command=searchQuery, width=10, height=1, font=fontStyle)
app.search_btn.pack(side="top", anchor="ne")
        


app.mainloop()
