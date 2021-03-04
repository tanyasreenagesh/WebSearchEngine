from query import *

# Indexing file
path = "webpages/WEBPAGES_RAW/bookkeeping.json"
with open(path) as file:
    data = json.load(file)
        
# Load and decompress invertedIdx from pickle file
invertedIdx = decompressPickle('invertedIdx.pbz2')
numOfDocs = invertedIdx['numOfDocs']
print("Number of docs   = ", numOfDocs)
print("Number of tokens = ", len(invertedIdx))


# Displays the results of the query
def displayResults():
    query = entry.get()

    # Clear the contents of result area
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
    

# Complete GUI for Search Engine

window = tk.Tk()
window.geometry("700x450")
window.title("UCI ICS Search Engine")

titleFont = tk.font.Font(family = "Helvetica", size = 11)
normalFont = tk.font.Font(family = "Helvetica", size = 10)
infoFont = tk.font.Font(family = "Helvetica", size = 10, weight='bold')

# Search box
frame1 = tk.Frame().grid(row=1, column=0, ipadx=20, ipady=10)
entry = tk.Entry(master=frame1, width=80)
entry.pack(expand=True, ipady=3)

# Search button
frame2 = tk.Frame().grid(row=1, column=1, padx=(15,5), pady=10)
searchButton = tk.Button(master=frame2, text="Search", command=displayResults, width=7, height=1)
searchButton.pack()

# Clear button
frame3 = tk.Frame().grid(row=1, column=2, ipadx=5, pady=10)
clearButton = tk.Button(master=frame3, text="Clear", command=clearEntry, width=7, height=1)
clearButton.pack()

# Results section
frame4 = tk.Frame().grid(row=2, columnspan=3, padx=(16,2))
frame4.grid_propagate(False)
resultsText = tk.Text(frame4, yscrollcommand=scrollbar.set)
resultsText.pack(fill='both')
resultsText.tag_config('url', foreground="blue", underline=True, font=normalFont)
resultsText.tag_config('title', foreground="black", font=titleFont)
resultsText.tag_config('desc', foreground="black", font=normalFont)
resultsText.tag_config('url_count', foreground="black", font=infoFont)

# Scrollbar
frame5 = tk.Frame().grid(row=2, column=3, sticky=N+S+W)
scrollbar = tk.Scrollbar(frame5, command=resultsText.yview)
scrollbar.pack(side='right', fill='y')


window.mainloop()










