import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter.font import Font
from random import randint
from tkinter import filedialog
import random

try:
    df = pd.read_csv("base/main.csv", sep=';', encoding='utf-8')
except FileNotFoundError:
    df = pd.DataFrame({
        'pergunta': ['Lorem Ipsum'],
        'alternativas': [3],
        'resposta_certa': ['Dolor cit amet'],
        'alternativa_1': ['Consectetur'],
        'alternativa_2': ['Adpiscing elit'],
        'alternativa_3': ['Duis efficitur'],
        'embaralhar': ['N']
    })


def criar_nova_base():
    global df
    df = pd.DataFrame({
        'pergunta': ['Lorem Ipsum'],
        'alternativas': [3],
        'resposta_certa': ['Dolor cit amet'],
        'alternativa_1': ['Consectetur'],
        'alternativa_2': ['Adpiscing elit'],
        'alternativa_3': ['Duis efficitur'],
        'embaralhar': ['N']
    })
    listbox.delete(0, tk.END)
    for row in df.itertuples(index=False):
        listbox.insert(tk.END, row.pergunta)


def abrir_base():
    global df
    file_path = filedialog.askopenfilename(
        filetypes=[('Arquivo CSV', '*.csv')],
        title='Abra um arquivo CSV'
    )

    if file_path:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
    else:
        print("Sem arquivo")
    listbox.delete(0, tk.END)
    for row in df.itertuples(index=False):
        listbox.insert(tk.END, row.pergunta)


def update(event):
    search_query = search_entry.get()
    search_query = search_query.lower()
    search_results = df[df['pergunta'].str.lower().str.contains(search_query) |
                        df['resposta_certa'].str.lower().str.contains(search_query) |
                        df['alternativa_1'].str.lower().str.contains(search_query) |
                        df['alternativa_2'].str.lower().str.contains(search_query) |
                        df['alternativa_3'].str.lower().str.contains(search_query)]
    listbox.delete(0, tk.END)
    for row in search_results.itertuples(index=False):
        listbox.insert(tk.END, row.pergunta)


def pergunta_selecionada(event):
    # get the selected question from the listbox
    selected_index = listbox.curselection()

    if len(selected_index) == 1:
        pergunta = listbox.get(selected_index[0]).strip().split('<br>')[0]
        print(pergunta)

        texto_restante = ''
        search_results = df[df['pergunta'].str.contains(pergunta)][['pergunta', 'resposta_certa', 'alternativa_1',
                                                                    'alternativa_2', 'alternativa_3', 'alternativas']]
        if search_results.shape[0] == 1:
            row = search_results.iloc[0]
        else:
            seg_parte = listbox.get(selected_index[0]).strip().split('<br>')[1]
            search_results = search_results[search_results['pergunta'].str.contains(seg_parte)][['pergunta',
                                                                                                 'resposta_certa',
                                                                                                 'alternativa_1',
                                                                        'alternativa_2', 'alternativa_3',
                                                                        'alternativas']]
            row = search_results.iloc[0]
        combobox.current(row['alternativas'] - 3)
        for entry in entries[:-1]:
            entry.configure(state='normal')
            entry.delete(0, tk.END)
        if row['alternativas'] < 5:
            alternativa_3_entry.delete(0, tk.END)
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
            textos = [perg, texto_restante, row['resposta_certa'], row['alternativa_1'], row['alternativa_2'],
                      row['alternativa_3']]
            if row['alternativas'] == 3:
                textos[2:-1] = random.sample(textos[2:-1], len(textos[2:-1]))
            else:
                textos[2:] = random.sample(textos[2:], len(textos[2:]))
        else:
            alternativa_3_entry.delete(0, tk.END)
            alternativa_3_entry.configure(state='disabled')
            perg_split = row['pergunta'].split('. ', 1)[1].split('<br>')
            perg = perg_split[0]
            if len(perg_split) > 1:
                texto_restante = '<br>' + perg_split[1]

            alts = row['pergunta'].split('. ')[0].replace(' ou ', ', ').split(', ')
            if row['resposta_certa'] == 'A':
                data = [perg + texto_restante, alts[0], alts[1], alts[2]]
            elif row['resposta_certa'] == 'B':
                data = [perg + texto_restante, alts[1], alts[0], alts[2]]
            else:
                data = [perg + texto_restante, alts[2], alts[0], alts[1]]

            textos = [alts[0] + ", " + alts[1] + " ou " + alts[2] + ". " + perg, texto_restante, '-', '-', '-', '-']

            for col, entry in zip(data, entries):
                entry.insert(0, col)

        zip_alternativas = ['', '', 'A: ', 'B: ', 'C: ', 'D: ']

        for item, z, t in zip(all_canvas, zip_alternativas, textos):
            if t != '-' and t != '':
                t = t.replace('<br>', '')
                canvas.itemconfig(item, text=z + t)
            else:
                canvas.itemconfig(item, text='')


def opcao_combobox(event):
    if combobox.current() >= 0:
        print(combobox.current())
        for entry in entries:
            # txt = entry.get()
            # entry.delete(0, tk.END)
            # entry.insert(0, txt)
            entry.configure(state='normal')
    if combobox.current() != 1:
        alternativa_3_entry.configure(state='disabled')


def add_question():
    global df
    nova_pergunta_dados = []
    valid = True
    dict_nova_pergunta = {'pergunta': '', 'resposta_certa': '', 'alternativa_1': '',
                          'alternativa_2': '', 'alternativa_3': ''}

    for entry in entries:
        value = entry.get()
        nova_pergunta_dados.append(value)

    for i, key in enumerate(dict_nova_pergunta.keys()):
        dict_nova_pergunta[key] = nova_pergunta_dados[i]

    # add the question to the dataframe
    if combobox.current() < 2:
        # df = pd.concat([df, pd.DataFrame(nova_pergunta)], ignore_index=True)
        if combobox.current() == 0:
            dict_nova_pergunta['alternativa_3'] = '-'
        dict_nova_pergunta['alternativas'] = combobox.current() + 3
        dict_nova_pergunta['embaralhar'] = 'N'
        df = pd.concat([df, pd.DataFrame(dict_nova_pergunta, index=[0])], ignore_index=True)
    else:
        valid = not any('.' in dict_nova_pergunta[i] for i in ['resposta_certa', 'alternativa_1', 'alternativa_2'])
        if valid:
            pos_resp_certa = randint(1, 3)
            comb = randint(0, 1)
            if pos_resp_certa == 1:
                if comb == 0:
                    texto_pergunta = dict_nova_pergunta['resposta_certa'] + ", " + dict_nova_pergunta['alternativa_1'] + \
                                     " ou " + dict_nova_pergunta['alternativa_2'] + ". " + \
                                     dict_nova_pergunta['pergunta']
                else:
                    texto_pergunta = dict_nova_pergunta['resposta_certa'] + ", " + dict_nova_pergunta['alternativa_2'] + \
                                     " ou " + dict_nova_pergunta['alternativa_1'] + ". " + \
                                     dict_nova_pergunta['pergunta']
                dict_nova_pergunta['pergunta'] = texto_pergunta
                dict_nova_pergunta['resposta_certa'] = 'A'
            elif pos_resp_certa == 2:
                if comb == 0:
                    texto_pergunta = dict_nova_pergunta['alternativa_1'] + ", " + dict_nova_pergunta['resposta_certa'] \
                                     + " ou " + dict_nova_pergunta['alternativa_2'] + ". " + \
                                     dict_nova_pergunta['pergunta']
                else:
                    texto_pergunta = dict_nova_pergunta['alternativa_2'] + ", " + dict_nova_pergunta['resposta_certa'] \
                                     + " ou " + dict_nova_pergunta['alternativa_1'] + ". " + \
                                     dict_nova_pergunta['pergunta']
                dict_nova_pergunta['pergunta'] = texto_pergunta
                dict_nova_pergunta['resposta_certa'] = 'B'
            else:
                if comb == 0:
                    texto_pergunta = dict_nova_pergunta['alternativa_2'] + ", " + dict_nova_pergunta['alternativa_1'] + \
                                     " ou " + dict_nova_pergunta['resposta_certa'] + ". " + dict_nova_pergunta['pergunta']
                else:
                    texto_pergunta = dict_nova_pergunta['alternativa_1'] + ", " + dict_nova_pergunta['alternativa_2'] + \
                                     " ou " + dict_nova_pergunta['resposta_certa'] + ". " + dict_nova_pergunta['pergunta']
                dict_nova_pergunta['pergunta'] = texto_pergunta
                dict_nova_pergunta['resposta_certa'] = 'C'
            dict_nova_pergunta['alternativa_1'] = '-'
            dict_nova_pergunta['alternativa_2'] = '-'
            dict_nova_pergunta['alternativa_3'] = '-'
            dict_nova_pergunta['alternativas'] = 5
            dict_nova_pergunta['embaralhar'] = 'N'
            df = pd.concat([df, pd.DataFrame(dict_nova_pergunta, index=[0])], ignore_index=True)
    if valid:
        listbox.delete(0, tk.END)
        for row in df.itertuples(index=False):
            listbox.insert(tk.END, row.pergunta)
        # show a message box to confirm the question was replaced
        messagebox.showinfo("Pergunta substituída!",
                            "A pergunta está substituída! Lembre-se de salvar a base ao final da sua edição para "
                            "que as mudanças tenham efeito.")
    else:
        messagebox.showinfo("Pergunta inválida!",
                            "Na final, as alternativas não podem ter ponto (.), pois isso vai confundir o "
                            "jogo. Retire os pontos das alternativas e tente novamente.")


def replace_question():
    # get the selected question
    pergunta = canvas.itemcget(perg_img, 'text')
    pergunta_2 = canvas.itemcget(perg_img_2, 'text')
    valid = True

    if pergunta_2 != '':
        pergunta = pergunta + '<br>' + pergunta_2

    nova_pergunta = []
    for entry in entries:
        value = entry.get()
        nova_pergunta.append(value)

    # replace the selected question with the new question
    if combobox.current() < 2:
        if combobox.current() == 1:
            df.loc[df["pergunta"] == pergunta, "alternativa_3"] = nova_pergunta[4]
        else:
            df.loc[df["pergunta"] == pergunta, "alternativa_3"] = '-'
        df.loc[df["pergunta"] == pergunta, "alternativas"] = combobox.current() + 3
        df.loc[df["pergunta"] == pergunta, "resposta_certa"] = nova_pergunta[1]
        df.loc[df["pergunta"] == pergunta, "alternativa_1"] = nova_pergunta[2]
        df.loc[df["pergunta"] == pergunta, "alternativa_2"] = nova_pergunta[3]
        df.loc[df["pergunta"] == pergunta, "pergunta"] = nova_pergunta[0]
    else:
        pos_resp_certa = randint(1, 3)
        valid = not any('.' in nova_pergunta[i] for i in range(1, 4))
        perg = pergunta.split('. ')[1]

        if valid:
            df.loc[df["pergunta"].str.contains(perg), "alternativa_1"] = '-'
            df.loc[df["pergunta"].str.contains(perg), "alternativa_2"] = '-'
            df.loc[df["pergunta"].str.contains(perg), "alternativa_3"] = '-'
            df.loc[df["pergunta"].str.contains(perg), "alternativas"] = 5
            if pos_resp_certa == 1:
                texto_pergunta = nova_pergunta[1] + ", " + nova_pergunta[2] + " ou " + nova_pergunta[3] + ". " + \
                                 nova_pergunta[0]
                df.loc[df["pergunta"].str.contains(perg), "resposta_certa"] = 'A'
                df.loc[df["pergunta"].str.contains(perg), "pergunta"] = texto_pergunta
            elif pos_resp_certa == 2:
                texto_pergunta = nova_pergunta[2] + ", " + nova_pergunta[1] + " ou " + nova_pergunta[3] + ". " + \
                                 nova_pergunta[0]
                df.loc[df["pergunta"].str.contains(perg), "resposta_certa"] = 'B'
                df.loc[df["pergunta"].str.contains(perg), "pergunta"] = texto_pergunta
            else:
                texto_pergunta = nova_pergunta[3] + ", " + nova_pergunta[2] + " ou " + nova_pergunta[1] + ". " + \
                                 nova_pergunta[0]
                df.loc[df["pergunta"].str.contains(perg), "resposta_certa"] = 'C'
                df.loc[df["pergunta"].str.contains(perg), "pergunta"] = texto_pergunta

        if valid:
            listbox.delete(0, tk.END)
            for row in df.itertuples(index=False):
                listbox.insert(tk.END, row.pergunta)
            # show a message box to confirm the question was replaced
            messagebox.showinfo("Pergunta substituída!",
                                "A pergunta está substituída! Lembre-se de salvar a base ao final da sua edição para "
                                "que as mudanças tenham efeito.")
        else:
            messagebox.showinfo("Pergunta inválida!",
                                "Na final, as alternativas não podem ter ponto (.), pois isso vai confundir o "
                                "jogo.")


def save_database():
    # show a message box to confirm the user wants to save the database
    file_path = filedialog.asksaveasfilename(
        defaultextension='.csv',
        filetypes=[('Arquivo CSV', '*.csv')],
        title='Salvar base de dados'
    )

    if file_path:
        df.to_csv(file_path, sep=';', encoding='utf-8', index=False)
        messagebox.showinfo("Base salva", "A base de perguntas foi salva.")


# Create main window
root = tk.Tk()
try:
    root.iconbitmap("rr_editor.ico")
except:
    pass
root.geometry("960x600")

menu_bar = tk.Menu(root)
# Create the "File" menu
menu_bar.add_command(label="Criar nova base", command=criar_nova_base)

# Add "Abrir base" option to the menu bar
menu_bar.add_command(label="Abrir base", command=abrir_base)

root.config(menu=menu_bar)
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
pergunta_label = tk.Label(entry_frame, text="Pergunta:", font=Font(size=12))
pergunta_label.grid(row=0, column=0, sticky="w")
pergunta_entry = tk.Entry(entry_frame, width=50, font=Font(size=12), state='disabled')
pergunta_entry.grid(row=0, column=1)
obs_label = tk.Label(entry_frame, text="Obs.: Use '<br>' para fazer a quebra de linha.",
                     font=Font(size=9, slant='italic'))
obs_label.grid(row=1, column=1, sticky="w")
resposta_certa_label = tk.Label(entry_frame, text="Resposta certa:", font=Font(size=12))
resposta_certa_label.grid(row=2, column=0, sticky="w")
resposta_certa_entry = tk.Entry(entry_frame, width=45, font=Font(size=12), state='disabled')
resposta_certa_entry.grid(row=2, column=1)
alternativa_1_label = tk.Label(entry_frame, text="Alternativa 1:", font=Font(size=12))
alternativa_1_label.grid(row=3, column=0, sticky="w")
alternativa_1_entry = tk.Entry(entry_frame, width=45, font=Font(size=12), state='disabled')
alternativa_1_entry.grid(row=3, column=1)
alternativa_2_label = tk.Label(entry_frame, text="Alternativa 2:", font=Font(size=12))
alternativa_2_label.grid(row=4, column=0, sticky="w")
alternativa_2_entry = tk.Entry(entry_frame, width=45, font=Font(size=12), state='disabled')
alternativa_2_entry.grid(row=4, column=1)
alternativa_3_label = tk.Label(entry_frame, text="Alternativa 3:", font=Font(size=12))
alternativa_3_label.grid(row=5, column=0, sticky="w")
alternativa_3_entry = tk.Entry(entry_frame, width=45, font=Font(size=12), state='disabled')
alternativa_3_entry.grid(row=5, column=1)

combobox_label = tk.Label(entry_frame, text="Rodada:", font=Font(size=12))
combobox_label.grid(row=6, column=0, sticky="w")
options = ["1ª e 2ª rodadas", "3ª e 4ª rodadas", "Rodada Final"]
entries = [pergunta_entry, resposta_certa_entry, alternativa_1_entry, alternativa_2_entry, alternativa_3_entry]

combobox = ttk.Combobox(entry_frame, values=options, font=Font(size=12))
combobox.grid(row=6, column=1)
combobox.bind("<<ComboboxSelected>>", opcao_combobox)
#
# if combobox.current() >= 0:
#     for entry in entries:
#         entry.configure(state='normal')
#     if combobox.current() == 2:
#         alternativa_3_entry.configure(state='normal')

entry_frame.pack(anchor=W)
# entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# entry_frame.grid(row=0, column=0)

canvas = tk.Canvas(root, width=1000, height=400)
canvas.pack()

# load the image and create a PhotoImage object from it
image = Image.open("img/pergunta_espera.png")
image = image.resize((int(image.width * 0.46), int(image.height * 0.46)))
photo = ImageTk.PhotoImage(image)

# add the image to the canvas
canvas.create_image(0, 0, anchor="nw", image=photo)

# add text to the image
tam_fonte = 13
perg_img = canvas.create_text(115, 55, text="Lorem ipsum", font=("FreeSans", tam_fonte), fill='white', anchor="nw")
perg_img_2 = canvas.create_text(115, 75, text="Lorem ipsum", font=("FreeSans", tam_fonte), fill='white', anchor="nw")
perg_alt1 = canvas.create_text(115, 100, text="A: Dolor cit amet", font=("FreeSans", tam_fonte), fill='white', anchor="nw")
perg_alt2 = canvas.create_text(370, 100, text="B: Consectetur", font=("FreeSans", tam_fonte), fill='white', anchor="nw")
perg_alt3 = canvas.create_text(115, 125, text="C: Adpiscing elit", font=("FreeSans", tam_fonte), fill='white', anchor="nw")
perg_alt4 = canvas.create_text(370, 125, text="D: Duis efficitur", font=("FreeSans", tam_fonte), fill='white', anchor="nw")
all_canvas = [perg_img, perg_img_2, perg_alt1, perg_alt2, perg_alt3, perg_alt4]

# create the buttons
add_button = tk.Button(canvas, text='Adicionar pergunta', command=add_question)
add_button.place(relx=0.5, rely=0.6, anchor='center')

replace_button = tk.Button(canvas, text='Substituir pergunta', command=replace_question)
replace_button.place(relx=0.5, rely=0.7, anchor='center')

save_button = tk.Button(canvas, text='Salvar base', command=save_database)
save_button.place(relx=0.5, rely=0.9, anchor='center')

# Start GUI loop
root.mainloop()
