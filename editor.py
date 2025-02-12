import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from PIL import Image, ImageTk
from tkinter.font import Font
from random import randint, shuffle
from itertools import permutations


class EditorPerguntas:
    """
    Classe principal que gerencia a interface gráfica para editar perguntas.
    """
    def __init__(self, root):
        """
        Construtor que inicializa a janela, carrega dados e cria os widgets.
        """
        self.root = root
        self.root.geometry("960x600")

        # Carregar dados padrão ou arquivo existente
        self.df = self.carregar_dados_padrao()

        # Cria o menu principal
        self.criar_menu()

        # Cria todos os elementos da interface
        self.criar_widgets()

        # Preenche o listbox com os dados iniciais
        self.atualizar_listbox(self.df)

    def carregar_dados_padrao(self):
        """
        Tenta carregar o CSV principal. Caso não encontre, retorna um DataFrame padrão.
        """
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
        return df

    def criar_menu(self):
        """
        Cria o menu superior com opções de criar nova base e abrir base.
        """
        menu_bar = tk.Menu(self.root)
        menu_bar.add_command(label="Criar nova base", command=self.criar_nova_base)
        menu_bar.add_command(label="Abrir base", command=self.abrir_base)
        self.root.config(menu=menu_bar)

    def criar_widgets(self):
        """
        Cria todos os elementos da interface gráfica: campos de texto, listbox, canvas etc.
        """

        # --- Seção de pesquisa ---
        search_frame = tk.Frame(self.root)
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT)
        self.search_entry.bind("<KeyRelease>", self.atualizar_pesquisa)
        search_frame.pack(anchor="w", pady=5)

        # --- Listbox e Label "Results" ---
        listbox_frame = tk.Frame(self.root)
        tk.Label(listbox_frame, text="Results:").pack(anchor="w")
        self.listbox = tk.Listbox(listbox_frame, height=50, width=50)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.selecionar_pergunta)
        listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # --- Frame para os campos de entrada (Pergunta, Resposta certa, etc.) ---
        entry_frame = tk.Frame(self.root)
        font_label = Font(size=12)

        # Dicionário para armazenar as Entries
        self.entries = {}

        # Label e campo para "Pergunta"
        tk.Label(entry_frame, text="Pergunta:", font=font_label).grid(row=0, column=0, sticky="w")
        self.entries["pergunta"] = tk.Entry(entry_frame, width=50, font=font_label, state='disabled')
        self.entries["pergunta"].grid(row=0, column=1, padx=5, pady=2)

        # Observação para quebra de linha
        tk.Label(
            entry_frame,
            text="Obs.: Use '<br>' para fazer a quebra de linha.",
            font=Font(size=9, slant='italic')
        ).grid(row=1, column=1, sticky="w")

        # Label e campo para "Resposta certa"
        tk.Label(entry_frame, text="Resposta certa:", font=font_label).grid(row=2, column=0, sticky="w")
        self.entries["resposta_certa"] = tk.Entry(entry_frame, width=45, font=font_label, state='disabled')
        self.entries["resposta_certa"].grid(row=2, column=1, padx=5, pady=2)

        # Label e campo para "Alternativa 1"
        tk.Label(entry_frame, text="Alternativa 1:", font=font_label).grid(row=3, column=0, sticky="w")
        self.entries["alternativa_1"] = tk.Entry(entry_frame, width=45, font=font_label, state='disabled')
        self.entries["alternativa_1"].grid(row=3, column=1, padx=5, pady=2)

        # Label e campo para "Alternativa 2"
        tk.Label(entry_frame, text="Alternativa 2:", font=font_label).grid(row=4, column=0, sticky="w")
        self.entries["alternativa_2"] = tk.Entry(entry_frame, width=45, font=font_label, state='disabled')
        self.entries["alternativa_2"].grid(row=4, column=1, padx=5, pady=2)

        # Label e campo para "Alternativa 3"
        tk.Label(entry_frame, text="Alternativa 3:", font=font_label).grid(row=5, column=0, sticky="w")
        self.entries["alternativa_3"] = tk.Entry(entry_frame, width=45, font=font_label, state='disabled')
        self.entries["alternativa_3"].grid(row=5, column=1, padx=5, pady=2)

        # --- Combobox para a Rodada ---
        tk.Label(entry_frame, text="Rodada:", font=("Arial", 12)).grid(row=6, column=0, sticky="w")
        self.round_options = ["1ª e 2ª rodadas", "3ª e 4ª rodadas", "Rodada Final"]
        self.round_combobox = ttk.Combobox(entry_frame, values=self.round_options, state="readonly")
        self.round_combobox.grid(row=6, column=1, padx=5, pady=2)
        self.round_combobox.current(0)
        self.round_combobox.bind("<<ComboboxSelected>>", self.atualizar_opcoes_ordem)

        # --- Combobox para a Ordem das Respostas ---
        tk.Label(entry_frame, text="Ordem das Respostas:", font=("Arial", 12)).grid(row=7, column=0, sticky="w")
        self.order_combobox = ttk.Combobox(entry_frame, state="readonly")
        self.order_combobox.grid(row=7, column=1, padx=5, pady=2)

        # Inicializa as opções de ordem
        self.atualizar_opcoes_ordem()

        entry_frame.pack(anchor="w", padx=5, pady=5)

        # --- Canvas para mostrar imagem e textos ---
        self.canvas = tk.Canvas(self.root, width=1000, height=400)
        self.canvas.pack(pady=5)
        self.carregar_imagem_canvas()

        # Cria textos sobre a imagem
        tam_fonte = 13
        self.text_ids = {}
        texts = ["", "", "A: ", "B: ", "C: ", "D: "]
        positions = [(115, 55), (115, 75), (115, 100), (370, 100), (115, 125), (370, 125)]
        keys = ["perg1", "perg2", "alt1", "alt2", "alt3", "alt4"]
        for key, pos, prefix in zip(keys, positions, texts):
            self.text_ids[key] = self.canvas.create_text(
                pos[0], pos[1],
                text=prefix,
                font=("FreeSans", tam_fonte),
                fill='white',
                anchor="nw"
            )

        # Botões
        tk.Button(self.canvas, text='Adicionar pergunta', command=self.adicionar_pergunta)\
            .place(relx=0.5, rely=0.6, anchor='center')
        tk.Button(self.canvas, text='Substituir pergunta', command=self.substituir_pergunta)\
            .place(relx=0.5, rely=0.7, anchor='center')
        tk.Button(self.canvas, text='Salvar base', command=self.salvar_base_de_dados)\
            .place(relx=0.5, rely=0.9, anchor='center')

    def carregar_imagem_canvas(self):
        """
        Carrega a imagem de fundo no Canvas. Ajuste o caminho conforme necessário.
        """
        try:
            image = Image.open("img/pergunta_espera.png")
            image = image.resize((int(image.width * 0.46), int(image.height * 0.46)))
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        except Exception as e:
            print("Erro ao carregar a imagem:", e)

    def atualizar_listbox(self, df_subset):
        """
        Limpa e repopula o listbox com base em um DataFrame específico.
        """
        self.listbox.delete(0, tk.END)
        for row in df_subset.itertuples(index=False):
            self.listbox.insert(tk.END, row.pergunta)

    def criar_nova_base(self):
        """
        Cria uma nova base de perguntas com dados padrão.
        """
        self.df = pd.DataFrame({
            'pergunta': ['Lorem Ipsum'],
            'alternativas': [3],
            'resposta_certa': ['Dolor cit amet'],
            'alternativa_1': ['Consectetur'],
            'alternativa_2': ['Adpiscing elit'],
            'alternativa_3': ['Duis efficitur'],
            'embaralhar': ['N']
        })
        self.atualizar_listbox(self.df)

    def abrir_base(self):
        """
        Abre um arquivo CSV e carrega seu conteúdo no DataFrame.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[('Arquivo CSV', '*.csv')],
            title='Abra um arquivo CSV'
        )
        if file_path:
            self.df = pd.read_csv(file_path, sep=';', encoding='utf-8')
            self.atualizar_listbox(self.df)
        else:
            print("Sem arquivo")

    def atualizar_pesquisa(self, event):
        """
        Filtra as perguntas no listbox com base no texto digitado no campo de pesquisa.
        """
        query = self.search_entry.get().lower()
        filtered = self.df[
            self.df['pergunta'].str.lower().str.contains(query) |
            self.df['resposta_certa'].str.lower().str.contains(query) |
            self.df['alternativa_1'].str.lower().str.contains(query) |
            self.df['alternativa_2'].str.lower().str.contains(query) |
            self.df['alternativa_3'].str.lower().str.contains(query)
        ]
        self.atualizar_listbox(filtered)

    def selecionar_pergunta(self, event):
        """
        Quando uma pergunta é selecionada no listbox, este método preenche os campos de texto
        e atualiza o Canvas com a pergunta correspondente.
        """
        selection = self.listbox.curselection()
        if not selection:
            return

        selected_text = self.listbox.get(selection[0])
        # Localiza a linha correspondente no DataFrame (caso haja duplicados, pega a primeira)
        row = self.df[self.df['pergunta'].str.contains(selected_text)].iloc[0]

        # Ajusta o Combobox de Rodada com base no valor de 'alternativas'
        self.round_combobox.current(row['alternativas'] - 3)
        # Atualiza a ordem das respostas para refletir a rodada correta
        self.atualizar_opcoes_ordem()

        # Habilita e limpa as entradas
        for key, entry in self.entries.items():
            entry.configure(state='normal')
            entry.delete(0, tk.END)

        # Preenche as entradas com os valores do DataFrame
        self.entries["pergunta"].insert(0, row['pergunta'])
        self.entries["resposta_certa"].insert(0, row['resposta_certa'])
        self.entries["alternativa_1"].insert(0, row['alternativa_1'])
        self.entries["alternativa_2"].insert(0, row['alternativa_2'])
        self.entries["alternativa_3"].insert(0, row['alternativa_3'] if row['alternativas'] >= 4 else '')

        # Atualiza o Canvas
        self.atualizar_canvas(row)

    def atualizar_canvas(self, row):
        """
        Exibe a pergunta e as alternativas no Canvas, de acordo com o número de alternativas.
        """
        # Divide a pergunta em partes usando <br>
        pergunta_parts = row['pergunta'].split('<br>')

        # Atualiza a parte principal da pergunta
        self.canvas.itemconfig(self.text_ids["perg1"], text=pergunta_parts[0])
        if len(pergunta_parts) > 1:
            self.canvas.itemconfig(self.text_ids["perg2"], text=pergunta_parts[1])
        else:
            self.canvas.itemconfig(self.text_ids["perg2"], text="")

        # Se for rodada final, normalmente o texto já contém as alternativas
        if row['alternativas'] == 5:
            self.canvas.itemconfig(self.text_ids["alt1"], text="")
            self.canvas.itemconfig(self.text_ids["alt2"], text="")
            self.canvas.itemconfig(self.text_ids["alt3"], text="")
            self.canvas.itemconfig(self.text_ids["alt4"], text="")
            return

        # Para as demais rodadas, exibe as alternativas individualmente
        self.canvas.itemconfig(self.text_ids["alt1"], text=f"A: {row['resposta_certa']}")
        self.canvas.itemconfig(self.text_ids["alt2"], text=f"B: {row['alternativa_1']}")
        self.canvas.itemconfig(self.text_ids["alt3"], text=f"C: {row['alternativa_2']}")
        if row['alternativas'] == 4:
            self.canvas.itemconfig(self.text_ids["alt4"], text=f"D: {row['alternativa_3']}")
        else:
            self.canvas.itemconfig(self.text_ids["alt4"], text="")

    def atualizar_opcoes_ordem(self, event=None):
        """
        Atualiza as opções de 'Ordem das Respostas' com base na rodada selecionada.
        """
        round_selected = self.round_combobox.get()
        if round_selected in ["1ª e 2ª rodadas", "Rodada Final"]:
            new_options = ["Qualquer ordem"] + [''.join(p) for p in permutations("ABC")]
        elif round_selected == "3ª e 4ª rodadas":
            new_options = ["Qualquer ordem"] + [''.join(p) for p in permutations("ABCD")]
        else:
            new_options = ["Qualquer ordem"]

        self.order_combobox["values"] = new_options
        self.order_combobox.current(0)

    def adicionar_pergunta(self):
        """
        Adiciona uma nova pergunta ao DataFrame, dependendo da rodada selecionada.
        Para a Rodada Final, valida que o formato da pergunta seja "A, B, C. Question" e
        que a resposta certa seja A, B, C ou 1, 2, 3 (convertendo se necessário).
        """
        data = {key: entry.get() for key, entry in self.entries.items()}

        # Rodadas 1 e 2
        if self.round_combobox.current() < 2:
            if self.round_combobox.current() == 0:
                data['alternativa_3'] = '-'
            data['alternativas'] = self.round_combobox.current() + 3
            data['embaralhar'] = 'N'
            self.df = pd.concat([self.df, pd.DataFrame(data, index=[0])], ignore_index=True)

        # Rodada Final
        else:
            text = data["pergunta"].strip()
            # Valida se há um ponto e divide a string
            if '.' not in text:
                messagebox.showerror("Pergunta inválida!",
                                     "A pergunta da rodada final precisa estar separada das alternativas por ponto.")
                return
            alternatives_text, question_text = text.split('.', 1)
            # Divide as alternativas usando vírgula e espaço
            alternatives_list = [alt.strip() for alt in alternatives_text.split(',')]
            if len(alternatives_list) != 3:
                messagebox.showerror("Pergunta inválida!",
                                     "A pergunta da rodada final precisa ter 3 alternativas ou uma das alternativas " +
                                     "tem ponto ou vírgula, o que pode confundir o jogo. Se isso for o caso, retire " +
                                     "o ponto ou vírgula para que o jogo não tenha problemas ao ler a pergunta.")
                return

            # Validação e conversão da resposta certa
            resp_certa = data["resposta_certa"].strip()
            if resp_certa in ['1', '2', '3']:
                data["resposta_certa"] = chr(64 + int(resp_certa))  # Converte 1->A, 2->B, 3->C
            elif resp_certa.upper() in ['A', 'B', 'C']:
                data["resposta_certa"] = resp_certa.upper()
            else:
                messagebox.showerror("Pergunta inválida!", "A resposta certa deve ser A, B, C ou 1, 2, 3")
                return

            # Reconstroi a pergunta de forma normalizada
            data["pergunta"] = f"{', '.join(alternatives_list)}. {question_text.strip()}"
            data['alternativas'] = 5
            data['embaralhar'] = 'N'
            self.df = pd.concat([self.df, pd.DataFrame(data, index=[0])], ignore_index=True)

        self.atualizar_listbox(self.df)
        messagebox.showinfo("Pergunta adicionada!",
                            "A pergunta foi adicionada com sucesso! Não esqueça de salvar a base.")

    def substituir_pergunta(self):
        """
        Substitui a pergunta selecionada no DataFrame pelos dados atualmente nos campos de texto.
        Para a Rodada Final, valida o formato da pergunta e da resposta certa.
        """
        # Usa o texto atual do Canvas (perg1) para identificar a pergunta (poderia ser melhorado)
        current_text = self.canvas.itemcget(self.text_ids["perg1"], 'text')
        new_data = {key: entry.get() for key, entry in self.entries.items()}

        # Rodadas 1 e 2
        if self.round_combobox.current() < 2:
            self.df.loc[self.df["pergunta"] == current_text, "pergunta"] = new_data["pergunta"]
            self.df.loc[self.df["pergunta"] == current_text, "resposta_certa"] = new_data["resposta_certa"]
            self.df.loc[self.df["pergunta"] == current_text, "alternativa_1"] = new_data["alternativa_1"]
            self.df.loc[self.df["pergunta"] == current_text, "alternativa_2"] = new_data["alternativa_2"]
            self.df.loc[self.df["pergunta"] == current_text, "alternativa_3"] = (
                new_data["alternativa_3"] if self.round_combobox.current() == 1 else '-'
            )
            self.df.loc[self.df["pergunta"] == current_text, "alternativas"] = self.round_combobox.current() + 3

        # Rodada Final
        else:
            text = new_data["pergunta"].strip()
            if '.' not in text:
                messagebox.showerror("Pergunta inválida!",
                                     "A pergunta da rodada final precisa estar separada das alternativas por ponto.")
                return
            alternatives_text, question_text = text.split('.', 1)
            alternatives_list = [alt.strip() for alt in alternatives_text.split(',')]
            if len(alternatives_list) != 3:
                messagebox.showerror("Pergunta inválida!",
                                     "A pergunta da rodada final precisa ter 3 alternativas ou uma das alternativas " +
                                     "tem ponto ou vírgula, o que pode confundir o jogo. Se isso for o caso, retire " +
                                     "o ponto ou vírgula para que o jogo não tenha problemas ao ler a pergunta.")
                return

            resp_certa = new_data["resposta_certa"].strip()
            if resp_certa in ['1', '2', '3']:
                new_data["resposta_certa"] = chr(64 + int(resp_certa))
            elif resp_certa.upper() in ['A', 'B', 'C']:
                new_data["resposta_certa"] = resp_certa.upper()
            else:
                messagebox.showerror("Pergunta inválida!", "A resposta certa deve ser A, B, C ou 1, 2, 3")
                return

            new_question_text = f"{', '.join(alternatives_list)}. {question_text.strip()}"
            mask = self.df["pergunta"].str.contains(current_text)
            self.df.loc[mask, "pergunta"] = new_question_text
            self.df.loc[mask, "resposta_certa"] = new_data["resposta_certa"]
            self.df.loc[mask, ["alternativa_1", "alternativa_2", "alternativa_3"]] = '-'
            self.df.loc[mask, "alternativas"] = 5

        self.atualizar_listbox(self.df)
        messagebox.showinfo("Pergunta substituída!",
                            "A pergunta foi substituída com sucesso! Não esqueça de salvar a base.")

    def salvar_base_de_dados(self):
        """
        Salva o DataFrame atual em um arquivo CSV escolhido pelo usuário.
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('Arquivo CSV', '*.csv')],
            title='Salvar base de dados'
        )
        if file_path:
            self.df.to_csv(file_path, sep=';', encoding='utf-8', index=False)
            messagebox.showinfo("Base salva", "A base de perguntas foi salva com sucesso!")


if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap("rr_editor.ico")
    except Exception as e:
        print("Ícone não carregado:", e)
    app = EditorPerguntas(root)
    root.mainloop()
