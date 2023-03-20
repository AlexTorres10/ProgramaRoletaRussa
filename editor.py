import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import ttk

# Load data from CSV file
df = pd.read_csv("base/main.csv")


# Define function to update Listbox when search query changes
def update(event):
    search_query = search_entry.get()
    search_results = df[df['pergunta'].str.contains(search_query) | df['resposta_certa'].str.contains(search_query) |
                        df['alternativa_1'].str.contains(search_query) | df['alternativa_2'].str.contains(search_query)
                        | df['alternativa_3'].str.contains(search_query)]
    listbox.delete(0, tk.END)
    for row in search_results.itertuples(index=False):
        listbox.insert(tk.END, row)
    if not search_results.empty:
        row = search_results.iloc[0]
        pergunta_entry.delete(0, tk.END)
        pergunta_entry.insert(0, row['pergunta'])
        resposta_certa_entry.delete(0, tk.END)
        resposta_certa_entry.insert(0, row['resposta_certa'])
        alternativa_1_entry.delete(0, tk.END)
        alternativa_1_entry.insert(0, row['alternativa_1'])
        alternativa_2_entry.delete(0, tk.END)
        alternativa_2_entry.insert(0, row['alternativa_2'])
        alternativa_3_entry.delete(0, tk.END)
        alternativa_3_entry.insert(0, row['alternativa_3'])


# Create main window
root = tk.Tk()
root.geometry("800x800")

# Create search entry
search_label = tk.Label(root, text="Search:")
search_label.pack(anchor=W)
search_entry = tk.Entry(root, width=50)
search_entry.bind("<KeyRelease>", update)
search_entry.pack(anchor=W)

# Create Listbox
listbox_frame = tk.Frame(root)
listbox_label = tk.Label(listbox_frame, text="Results:")
listbox = tk.Listbox(root, height=50, width=50)
for row in df.itertuples(index=False):
    listbox.insert(tk.END, row.pergunta)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#
# # Create entry boxes
entry_frame = tk.Frame(root)
pergunta_label = tk.Label(entry_frame, text="Pergunta:")
pergunta_label.grid(row=0, column=0, sticky="w")
pergunta_entry = tk.Entry(entry_frame, width=50)
pergunta_entry.grid(row=0, column=1)
resposta_certa_label = tk.Label(entry_frame, text="Resposta certa:")
resposta_certa_label.grid(row=1, column=0, sticky="w")
resposta_certa_entry = tk.Entry(entry_frame, width=50)
resposta_certa_entry.grid(row=1, column=1)
alternativa_1_label = tk.Label(entry_frame, text="Alternativa 1:")
alternativa_1_label.grid(row=2, column=0, sticky="w")
alternativa_1_entry = tk.Entry(entry_frame, width=50)
alternativa_1_entry.grid(row=2, column=1)
alternativa_2_label = tk.Label(entry_frame, text="Alternativa 2:")
alternativa_2_label.grid(row=3, column=0, sticky="w")
alternativa_2_entry = tk.Entry(entry_frame, width=50)
alternativa_2_entry.grid(row=3, column=1)
alternativa_3_label = tk.Label(entry_frame, text="Alternativa 3:")
alternativa_3_entry = tk.Entry(entry_frame, width=50)
alternativa_3_entry.grid(row=4, column=1)
combobox_label = tk.Label(entry_frame, text="Options:")
combobox_label.grid(row=5, column=0, sticky="w")
options = ["Option 1", "Option 2", "Option 3"]
combobox = ttk.Combobox(entry_frame, values=options)
combobox.grid(row=5, column=1)
entry_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Start GUI loop
root.mainloop()
