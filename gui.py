import tkinter as tk
from tkinter import *
from query import *

path = "webpages/WEBPAGES_RAW/bookkeeping.json"
with open(path) as file:
    data = json.load(file)
        
# load and decompress invertedIdx from pickle file
invertedIdx = decompressPickle('invertedIdx.pbz2')

def displayResults():
    query = entry.get()
    first = True

    resultsText.configure(state='normal')
    resultsText.delete('1.0', END)
    resultsText.configure(state='disabled')

    getResults(query, invertedIdx, data, resultsText)

    
# Clears the search box and results
def clearEntry():
    entry.delete(0, tk.END)
    resultsText.configure(state='normal')
    resultsText.delete('1.0', END)
    resultsText.configure(state='disabled')
    

window = tk.Tk()
window.geometry("700x450")
window.title("UCI ICS Search Engine")

frame1 = tk.Frame()
frame2 = tk.Frame()
frame3 = tk.Frame()
frame4 = tk.Frame()
frame5 = tk.Frame()

scrollbar = tk.Scrollbar(frame5)

frame1.grid(row=1, column=0, ipadx=20, ipady=10)
entry = tk.Entry(master=frame1, width=80)
entry.pack(expand=True, ipady=3)

frame2.grid(row=1, column=1, padx=(15,5), pady=10)
searchButton = tk.Button(master=frame2, text="Search", command=displayResults, width=7, height=1)
searchButton.pack()

frame3.grid(row=1, column=2, ipadx=5, pady=10)
clearButton = tk.Button(master=frame3, text="Clear", command=clearEntry, width=7, height=1)
clearButton.pack()

frame4.grid(row=2, columnspan=3, padx=(16,2))
resultsText = tk.Text(frame4, yscrollcommand=scrollbar.set)
resultsText.pack()

frame5.grid(row=2, column=3, sticky=N+S+W)

scrollbar.config(command=resultsText.yview)
scrollbar.pack(side='right', fill='y')


window.mainloop()










