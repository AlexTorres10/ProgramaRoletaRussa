import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter.font import Font

# Load data from CSV file
df = pd.read_csv("base/main.csv")

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

def pergunta_selecionada(event):
    # get the selected question from the listbox
    selected_index = listbox.curselection()
    for entry in entries:
        entry.delete(0, tk.END)

    if len(selected_index) == 1:
        pergunta = listbox.get(selected_index[0])
        print(pergunta)
        texto_restante = ''
        search_results = df[df['pergunta'].str.contains(pergunta)][['pergunta','resposta_certa','alternativa_1',
                                                                    'alternativa_2','alternativa_3','alternativas']]
        row = search_results.iloc[0]
        combobox.current(row['alternativas']-3)
        if row['alternativas'] < 5:
            if row['alternativas'] == 3:
                alternativa_3_entry.configure(state='disabled')
            elif row['alternativas'] == 4:
                alternativa_3_entry.configure(state='normal')
            for col, entry in zip(row[:-1], entries):
                entry.insert(0, col)
            perg_split = row['pergunta'].split('<br>')
            perg = perg_split[0]
            if len(perg_split) > 1:
                texto_restante = perg_split[1]
            textos = [perg, texto_restante, row['resposta_certa'], row['alternativa_1'], row['alternativa_2'], row['alternativa_3']]
        else:
            alternativa_3_entry.configure(state='disabled')
            perg_split = row['pergunta'].split('. ')[1].split('<br>')
            perg = perg_split[0]
            if len(perg_split) > 1:
                texto_restante = perg_split[1]

            alts = row['pergunta'].split('. ')[0].replace(' ou ', ', ').split(', ')
            if row['alternativas'] == 'A':
                data = [perg, alts[0], alts[1], alts[2]]
            elif row['alternativas'] == 'B':
                data = [perg, alts[1], alts[0], alts[2]]
            else:
                data = [perg, alts[2], alts[0], alts[1]]
            
            textos = [alts[0]+", "+alts[1]+" ou "+alts[2]+". "+perg, '', '-', '-', '-', '-']
            for col, entry in zip(data, entries):
                entry.insert(0, col)
        
        zip_alternativas = ['', '', 'A: ', 'B: ', 'C: ', 'D: ']
        
        for item, z, t in zip(all_canvas, zip_alternativas, textos):
            if t != '-' and t != '':
                canvas.itemconfig(item, text=z+t)
            else:
                canvas.itemconfig(item, text='')


def add_question():
    # get the question from the entry widget
    question = 'A'

    # add the question to the dataframe
    df = pd.concat([df, pd.DataFrame({"question": [question]})], ignore_index=True)

    # show a message box to confirm the question was added
    messagebox.showinfo("Question added", f"The question '{question}' was added to the database.")


def replace_question():
    # get the selected question
    selected_question = listbox.get(listbox.curselection())[0]

    # get the new question from the entry widget
    new_question = 'B'

    # replace the selected question with the new question
    df.loc[df["question"] == selected_question, "question"] = new_question

    # show a message box to confirm the question was replaced
    messagebox.showinfo("Question replaced", f"The question '{selected_question}' was replaced with '{new_question}'.")


def save_database():
    # show a message box to confirm the user wants to save the database
    confirm = messagebox.askyesno("Save Database", "Are you sure you want to save the database?")

    if confirm:
        # save the database to disk
        df.to_csv("base/main.csv", index=False)

        # show a message box to confirm the database was saved
        messagebox.showinfo("Database saved", "The database was saved to 'base/main.csv'.")
# Create main window
root = tk.Tk()
root.geometry("960x600")

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
listbox.bind("<<ListboxSelect>>", pergunta_selecionada)

listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#
# # Create entry boxes
entry_frame = tk.Frame(root)
pergunta_label = tk.Label(entry_frame, text="Pergunta:",font=Font(size=12))
pergunta_label.grid(row=0, column=0, sticky="w")
pergunta_entry = tk.Entry(entry_frame, width=50,font=Font(size=12))
pergunta_entry.grid(row=0, column=1)
obs_label = tk.Label(entry_frame, text="Obs.: Use '<br>' para fazer a quebra de linha.",font=Font(size=9, slant='italic'))
obs_label.grid(row=1, column=1, sticky="w")
resposta_certa_label = tk.Label(entry_frame, text="Resposta certa:",font=Font(size=12))
resposta_certa_label.grid(row=2, column=0, sticky="w")
resposta_certa_entry = tk.Entry(entry_frame, width=50, font=Font(size=12))
resposta_certa_entry.grid(row=2, column=1)
alternativa_1_label = tk.Label(entry_frame, text="Alternativa 1:",font=Font(size=12))
alternativa_1_label.grid(row=3, column=0, sticky="w")
alternativa_1_entry = tk.Entry(entry_frame, width=50, font=Font(size=12))
alternativa_1_entry.grid(row=3, column=1)
alternativa_2_label = tk.Label(entry_frame, text="Alternativa 2:",font=Font(size=12))
alternativa_2_label.grid(row=4, column=0, sticky="w")
alternativa_2_entry = tk.Entry(entry_frame, width=50, font=Font(size=12))
alternativa_2_entry.grid(row=4, column=1)
alternativa_3_label = tk.Label(entry_frame, text="Alternativa 3:",font=Font(size=12))
alternativa_3_label.grid(row=5, column=0, sticky="w")
alternativa_3_entry = tk.Entry(entry_frame, width=50, font=Font(size=12))
alternativa_3_entry.grid(row=5, column=1)

combobox_label = tk.Label(entry_frame, text="Rodada:", font=Font(size=12))
combobox_label.grid(row=6, column=0, sticky="w")
options = ["1ª e 2ª rodadas", "3ª e 4ª rodadas", "Rodada Final"]
entries = [pergunta_entry, resposta_certa_entry, alternativa_1_entry, alternativa_2_entry, alternativa_3_entry]
combobox = ttk.Combobox(entry_frame, values=options, font=Font(size=12))
combobox.grid(row=6, column=1)

entry_frame.pack(anchor=W)
# entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# entry_frame.grid(row=0, column=0)

canvas = tk.Canvas(root, width=1000, height=800)
canvas.pack()

# load the image and create a PhotoImage object from it
image = Image.open("img/pergunta_espera.png")
image = image.resize((int(image.width * 0.5), int(image.height * 0.5)))
photo = ImageTk.PhotoImage(image)

# add the image to the canvas
canvas.create_image(0, 0, anchor="nw", image=photo)

# add text to the image
perg_img = canvas.create_text(125, 60, text="Lorem ipsum", font=("FreeSans", 13), fill='white', anchor="nw")
perg_img_2 = canvas.create_text(125, 80, text="Lorem ipsum", font=("FreeSans", 13), fill='white', anchor="nw")
perg_alt1 = canvas.create_text(125, 120, text="A: Dolor cit amet", font=("FreeSans", 13), fill='white', anchor="nw")
perg_alt2 = canvas.create_text(400, 120, text="B: Consectetur", font=("FreeSans", 13), fill='white', anchor="nw")
perg_alt3 = canvas.create_text(125, 145, text="C: Adpiscing elit", font=("FreeSans", 13), fill='white', anchor="nw")
perg_alt4 = canvas.create_text(400, 145, text="D: Duis efficitur", font=("FreeSans", 13), fill='white', anchor="nw")
all_canvas = [perg_img, perg_img_2, perg_alt1, perg_alt2, perg_alt3, perg_alt4]

# button_frame = tk.Frame(root)

# # Add the buttons to the button frame
# add_button = tk.Button(button_frame, text='Add Question')
# add_button.pack(side=tk.LEFT, padx=200)
# replace_button = tk.Button(button_frame, text='Replace Question')
# replace_button.pack(side=tk.LEFT, padx=200)

# # Pack the button frame below the canvas
# button_frame.pack(side=tk.BOTTOM, padx=200, pady=10)
# Start GUI loop
root.mainloop()
