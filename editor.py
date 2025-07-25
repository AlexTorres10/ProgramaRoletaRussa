import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from PIL import Image, ImageTk
from tkinter.font import Font
from random import randint, shuffle
from itertools import permutations
import os
from PIL import ImageFont

class EditorPerguntas:
    """
    Classe principal que gerencia a interface gráfica para editar perguntas.
    """
    def __init__(self, root):
        """
        Construtor que inicializa a janela, carrega os dados e cria os widgets.
        """
        self.root = root
        self.root.geometry("960x600")

        # Carrega os dados padrão ou uma base existente
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
        Cria todos os elementos da interface gráfica: campos de texto, listbox, canvas, etc.
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
        Carrega a imagem de fundo no Canvas. Tenta primeiro a pasta local,
        depois a pasta de instalação padrão.
        """
        caminhos = [
            "img/pergunta_espera.png",
            r"C:\Program Files (x86)\Roleta Russa\img\pergunta_espera.png"
        ]

        for caminho in caminhos:
            if os.path.exists(caminho):
                try:
                    image = Image.open(caminho)
                    image = image.resize((int(image.width * 0.46), int(image.height * 0.46)))
                    self.photo = ImageTk.PhotoImage(image)
                    self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
                    return  # imagem carregada com sucesso
                except Exception as e:
                    print(f"Erro ao carregar a imagem em '{caminho}':", e)
                    break

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
        Se ocorrer algum erro, exibe uma messagebox com o erro.
        """
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[('Arquivo CSV', '*.csv')],
                title='Abra um arquivo CSV'
            )
            if file_path:
                self.df = pd.read_csv(file_path, sep=';', encoding='utf-8')
                self.atualizar_listbox(self.df)
            else:
                print("Sem arquivo")
        except Exception as e:
            messagebox.showerror("Erro ao abrir CSV", f"Ocorreu o seguinte erro: {e}")

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
        row = self.df[self.df['pergunta'].str.contains(selected_text.strip(), regex=False)].iloc[0]

        # Ajusta o Combobox de Rodada com base no valor de 'alternativas'
        # (1ª e 2ª rodadas: alternativas = 3 ou 4; 3ª e 4ª: alternativas = 4)
        if row['alternativas'] == 3:
            self.round_combobox.current(0)
        elif row['alternativas'] == 4:
            self.round_combobox.current(1)
        else:
            self.round_combobox.current(2)
        # Atualiza as opções de ordem para refletir a rodada correta
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

        # Verifica o valor de 'embaralhar' e atualiza o order_combobox
        embaralhar_val = str(row['embaralhar']).strip()
        # Para rodadas 1/2 ou 3/4, o número esperado de dígitos é igual ao número de alternativas (3 ou 4)
        expected_len = row['alternativas'] if row['alternativas'] in [3, 4] else 0

        # Se 'embaralhar' for "N" ou não tiver o tamanho esperado ou não conter exatamente os dígitos necessários,
        # define a opção como "Qualquer ordem"
        if embaralhar_val == "N" or len(embaralhar_val) != expected_len or set(embaralhar_val) != set(
                str(i) for i in range(1, expected_len + 1)):
            self.order_combobox.set("Qualquer ordem")
        else:
            # Converte cada dígito para a letra correspondente (1->A, 2->B, 3->C, 4->D)
            mapping = {'1': 'A', '2': 'B', '3': 'C', '4': 'D'}
            order_letters = "".join(mapping[d] for d in embaralhar_val)
            self.order_combobox.set(order_letters)

        # Atualiza o Canvas
        self.atualizar_canvas(row)

    def atualizar_canvas(self, row):
        """
        Updates the canvas with the question and answer choices based on the selected round.
        Wraps long questions based on pixel width using the same font as Pygame.
        """

        # Fonte usada para medir o texto
        tam_fonte = 36
        font_path = "fonts/FreeSans.ttf"
        font = ImageFont.truetype(font_path, tam_fonte)

        # Quebrar a pergunta em linhas com até 1000px
        palavras = row['pergunta'].split(' ')
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            test_line = f"{linha_atual} {palavra}".strip()
            largura = font.getbbox(test_line)[2]
            if largura <= 1000:
                linha_atual = test_line
            else:
                linhas.append(linha_atual)
                linha_atual = palavra

        if linha_atual:
            linhas.append(linha_atual)

        # Atualizar canvas com no máximo 2 linhas da pergunta
        self.canvas.itemconfig(self.text_ids["perg1"], text=linhas[0])
        self.canvas.itemconfig(self.text_ids["perg2"], text=linhas[1] if len(linhas) > 1 else "")

        # Se for pergunta da final, limpar as alternativas
        if row['alternativas'] == 5:
            self.canvas.itemconfig(self.text_ids["alt1"], text="")
            self.canvas.itemconfig(self.text_ids["alt2"], text="")
            self.canvas.itemconfig(self.text_ids["alt3"], text="")
            self.canvas.itemconfig(self.text_ids["alt4"], text="")
            return

        # Alternativas e rótulos
        alternativas_originais = [row['resposta_certa'], row['alternativa_1'], row['alternativa_2']]
        labels = ["A: ", "B: ", "C: "]

        if row['alternativas'] == 4:
            alternativas_originais.append(row['alternativa_3'])
            labels.append("D: ")

        if row['embaralhar'].isdigit():
            perm = row['embaralhar']
            nova_ordem = [alternativas_originais[int(ch) - 1] for ch in perm]
        else:
            nova_ordem = alternativas_originais

        # Atualizar alternativas no canvas
        self.canvas.itemconfig(self.text_ids["alt1"], text=f"{labels[0]}{nova_ordem[0]}")
        self.canvas.itemconfig(self.text_ids["alt2"], text=f"{labels[1]}{nova_ordem[1]}")
        self.canvas.itemconfig(self.text_ids["alt3"], text=f"{labels[2]}{nova_ordem[2]}")

        if row['alternativas'] == 3:
            self.canvas.itemconfig(self.text_ids["alt4"], text="")
        else:
            self.canvas.itemconfig(self.text_ids["alt4"], text=f"{labels[3]}{nova_ordem[3]}")

    
    def atualizar_opcoes_ordem(self, event=None):
        """
        Atualiza as opções de 'Ordem das Respostas' com base na rodada selecionada.
        Se a opção for "Qualquer ordem", não haverá alteração (embaralhar = "N").
        Caso contrário, o valor selecionado será convertido (ex.: "DCBA" → "4321").
        """
        rodada_selecionada = self.round_combobox.get()
        if rodada_selecionada in ["1ª e 2ª rodadas", "Rodada Final"]:
            novas_opcoes = ["Qualquer ordem"] + [''.join(p) for p in permutations("ABC")]
        elif rodada_selecionada == "3ª e 4ª rodadas":
            novas_opcoes = ["Qualquer ordem"] + [''.join(p) for p in permutations("ABCD")]
        else:
            novas_opcoes = ["Qualquer ordem"]

        self.order_combobox["values"] = novas_opcoes
        self.order_combobox.current(0)

    def adicionar_pergunta(self):
        """
        Adiciona uma nova pergunta ao DataFrame, dependendo da rodada selecionada.
        Para rodadas 1/2 e 3/4, valida e armazena a ordem das respostas escolhida.
        Para a Rodada Final, a validação permanece conforme implementado anteriormente.
        """
        data = {key: entry.get() for key, entry in self.entries.items()}

        # Rodadas 1 e 2 (índices 0 e 1 na combobox)
        if self.round_combobox.current() < 2:
            if self.round_combobox.current() == 0:
                data['alternativa_3'] = '-'
                data['alternativas'] = 3
            else:
                data['alternativas'] = 4
            # Processa a opção de ordem selecionada
            ordem = self.order_combobox.get()
            if ordem == "Qualquer ordem":
                data['embaralhar'] = "N"
            else:
                mapeamento = {'A': '1', 'B': '2', 'C': '3', 'D': '4'}
                data['embaralhar'] = "".join(mapeamento[letra] for letra in ordem)
            data['embaralhar'] = data['embaralhar']
            print(data)
            self.df = pd.concat([self.df, pd.DataFrame(data, index=[0])], ignore_index=True)

        # Rodada Final
        else:
            text = data["pergunta"].strip()
            if '.' not in text:
                messagebox.showerror("Pergunta inválida!", "A pergunta da rodada final precisa ter 3 alternativas")
                return
            alternativas_texto, texto_pergunta = text.split('.', 1)
            alternativas_lista = [alt.strip() for alt in alternativas_texto.split(',')]
            if len(alternativas_lista) != 3:
                messagebox.showerror("Pergunta inválida!", "A pergunta da rodada final precisa ter 3 alternativas")
                return

            resp_certa = data["resposta_certa"].strip()
            if resp_certa in ['1', '2', '3']:
                data["resposta_certa"] = chr(64 + int(resp_certa))  # Converte 1->A, 2->B, 3->C
            elif resp_certa.upper() in ['A', 'B', 'C']:
                data["resposta_certa"] = resp_certa.upper()
            else:
                messagebox.showerror("Pergunta inválida!", "A resposta certa deve ser A, B, C ou 1, 2, 3")
                return

            data["pergunta"] = f"{', '.join(alternativas_lista)}. {texto_pergunta.strip()}"
            data['alternativas'] = 5
            data['embaralhar'] = 'N'
            self.df = pd.concat([self.df, pd.DataFrame(data, index=[0])], ignore_index=True)

        self.atualizar_listbox(self.df)
        messagebox.showinfo("Pergunta adicionada!",
                            "A pergunta foi adicionada com sucesso! Não esqueça de salvar a base.")

    def substituir_pergunta(self):
        """
        Substitui a pergunta selecionada no DataFrame pelos dados atualmente nos campos de texto.
        Agora captura a pergunta completa do Canvas, garantindo a substituição correta.
        Para a Rodada Final, mantém a lógica de validação e atualização correta.
        """
        # Obtém o texto completo da pergunta do Canvas
        pergunta_parte1 = self.canvas.itemcget(self.text_ids["perg1"], 'text')
        pergunta_parte2 = self.canvas.itemcget(self.text_ids["perg2"], 'text')

        # Junta as partes da pergunta, tratando casos onde há apenas uma linha
        pergunta_completa = pergunta_parte1
        if pergunta_parte2:
            pergunta_completa += "<br>" + pergunta_parte2

        # Obtém os novos valores dos campos de entrada
        nova_pergunta = {key: entry.get().strip() for key, entry in self.entries.items()}

        # Localiza a pergunta correta na base de dados
        mask = self.df["pergunta"] == pergunta_completa
        if not mask.any():
            messagebox.showerror("Erro ao substituir", "A pergunta não foi encontrada na base.")
            return

        # Se for uma pergunta das rodadas 1/2 ou 3/4
        if self.round_combobox.current() < 2:
            self.df.loc[mask, "pergunta"] = nova_pergunta["pergunta"]
            self.df.loc[mask, "resposta_certa"] = nova_pergunta["resposta_certa"]
            self.df.loc[mask, "alternativa_1"] = nova_pergunta["alternativa_1"]
            self.df.loc[mask, "alternativa_2"] = nova_pergunta["alternativa_2"]

            if self.round_combobox.current() == 1:  # Rodadas 3 e 4 (com 4 alternativas)
                self.df.loc[mask, "alternativa_3"] = nova_pergunta["alternativa_3"]
                self.df.loc[mask, "alternativas"] = 4
            else:  # Rodadas 1 e 2 (com 3 alternativas)
                self.df.loc[mask, "alternativa_3"] = "-"
                self.df.loc[mask, "alternativas"] = 3

            # Atualiza a ordem das respostas
            ordem = self.order_combobox.get()
            if ordem == "Qualquer ordem":
                self.df.loc[mask, "embaralhar"] = "N"
            else:
                mapeamento = {'A': '1', 'B': '2', 'C': '3', 'D': '4'}
                nova_ordem = "".join(mapeamento[letra] for letra in ordem)
                self.df.loc[mask, "embaralhar"] = nova_ordem

        # Se for uma pergunta da Rodada Final
        else:
            text = nova_pergunta["pergunta"].strip()
            if '.' not in text:
                messagebox.showerror("Pergunta inválida!", "A pergunta da rodada final precisa ter 3 alternativas.")
                return
            alternativas_texto, texto_pergunta = text.split('.', 1)
            alternativas_lista = [alt.strip() for alt in alternativas_texto.split(',')]
            if len(alternativas_lista) != 3:
                messagebox.showerror("Pergunta inválida!", "A pergunta da rodada final precisa ter 3 alternativas.")
                return

            # Valida e converte a resposta correta
            resp_certa = nova_pergunta["resposta_certa"].strip()
            if resp_certa in ['1', '2', '3']:
                nova_pergunta["resposta_certa"] = chr(64 + int(resp_certa))  # Converte 1→A, 2→B, 3→C
            elif resp_certa.upper() in ['A', 'B', 'C']:
                nova_pergunta["resposta_certa"] = resp_certa.upper()
            else:
                messagebox.showerror("Pergunta inválida!", "A resposta certa deve ser A, B, C ou 1, 2, 3.")
                return

            # Atualiza a pergunta com a formatação correta
            nova_pergunta_texto = f"{', '.join(alternativas_lista)}. {texto_pergunta.strip()}"
            self.df.loc[mask, "pergunta"] = nova_pergunta_texto
            self.df.loc[mask, "resposta_certa"] = nova_pergunta["resposta_certa"]
            self.df.loc[mask, ["alternativa_1", "alternativa_2", "alternativa_3"]] = '-'
            self.df.loc[mask, "alternativas"] = 5
            self.df.loc[mask, "embaralhar"] = "N"  # Rodada final não tem ordem embaralhada

        # Atualiza a lista de perguntas
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
