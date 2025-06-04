import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.cidade import Cidade
from controllers.cidade_controller import CidadeController
from utils.theme import ThemeManager

class MainView:
    def __init__(self, root):
        self.root = root
        self.controller = CidadeController()
        self.theme_manager = ThemeManager()
        self.style = ttk.Style()  # Inicializa estilo aqui
        
        self.root.title("Gestão de Cidades - CRUD")
        self.root.geometry("900x600")

        # Frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Componentes
        self.setup_toolbar()  # Cria botões antes de configurar o tema
        self.setup_table()
        self.setup_status_bar()

        # Configuração do tema
        self.setup_theme()

        # Barra de menu
        self.setup_menu()

        # Carregar view inicial
        self.show_list_view()

    def setup_theme(self):
        theme = self.theme_manager.theme
        
        self.root.configure(bg=theme["bg"])
        
        self.style.theme_use('default')
        self.style.configure("Treeview",
                             background=theme["bg"],
                             foreground=theme["fg"],
                             fieldbackground=theme["bg"])
        self.style.configure("Treeview.Heading",
                             background=theme["button_bg"],
                             foreground=theme["fg"],
                             relief="flat")
        self.style.map('Treeview', background=[('selected', '#6A8CAF')])
        
        if hasattr(self, 'main_frame'):
            self.main_frame.configure(bg=theme["bg"])
        if hasattr(self, 'status_bar'):
            self.status_bar.configure(bg=theme["bg"], fg=theme["fg"])

        # Armazena os botões para alterar tema depois
        self.toolbar_buttons = [
            self.btn_add,
            self.btn_edit,
            self.btn_delete,
            self.btn_refresh,
            self.btn_search
        ]
        for btn in self.toolbar_buttons:
            btn.configure(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["button_bg"])

    def toggle_theme(self):
        novo_tema = "escuro" if self.theme_manager.current_theme == "claro" else "claro"
        self.theme_manager.set_theme(novo_tema)
        self.setup_theme()

    def setup_menu(self):
        menubar = tk.Menu(self.root)

        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Importar Excel", command=self.importar_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)

        # Menu Cidades
        city_menu = tk.Menu(menubar, tearoff=0)
        city_menu.add_command(label="Adicionar Cidade", command=self.show_add_form)
        city_menu.add_command(label="Listar Cidades", command=self.show_list_view)
        menubar.add_cascade(label="Cidades", menu=city_menu)

        # Menu Relatórios
        report_menu = tk.Menu(menubar, tearoff=0)
        report_menu.add_command(label="Cidade Mais Extensa", command=self.show_mais_extensa)
        report_menu.add_command(label="Cidade Mais Populosa", command=self.show_mais_populosa)
        report_menu.add_command(label="Média de População", command=self.show_media_populacao)
        menubar.add_cascade(label="Relatórios", menu=report_menu)

        # Menu Tema
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Alternar Tema", command=self.toggle_theme)
        menubar.add_cascade(label="Tema", menu=theme_menu)

        self.root.config(menu=menubar)

    def setup_toolbar(self):
        toolbar = tk.Frame(self.main_frame, bd=1, relief=tk.RAISED)
        toolbar.pack(fill=tk.X)

        # Botões da toolbar
        icons = {
            'add': '➕',
            'edit': '✏️',
            'delete': '🗑️',
            'refresh': '🔄',
            'search': '🔍'
        }

        self.btn_add = tk.Button(toolbar, text=f"{icons['add']} Adicionar", command=self.show_add_form)
        self.btn_add.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_edit = tk.Button(toolbar, text=f"{icons['edit']} Editar", command=self.show_edit_form)
        self.btn_edit.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_delete = tk.Button(toolbar, text=f"{icons['delete']} Remover", command=self.remover_cidade)
        self.btn_delete.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_refresh = tk.Button(toolbar, text=f"{icons['refresh']} Atualizar", command=self.refresh_table)
        self.btn_refresh.pack(side=tk.LEFT, padx=2, pady=2)

        # Campo de pesquisa
        self.search_frame = tk.Frame(toolbar)
        self.search_frame.pack(side=tk.RIGHT, padx=5)

        self.search_entry = tk.Entry(self.search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=2)

        self.btn_search = tk.Button(self.search_frame, text=icons['search'], command=self.pesquisar_cidades)
        self.btn_search.pack(side=tk.LEFT)

    def setup_table(self):
        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(expand=True, fill=tk.BOTH)

        self.tree = ttk.Treeview(table_frame, columns=('nome', 'dimensao', 'populacao'), show='headings')

        self.tree.heading('nome', text='Cidade', anchor=tk.W)
        self.tree.heading('dimensao', text='Dimensão (km²)', anchor=tk.CENTER)
        self.tree.heading('populacao', text='População', anchor=tk.CENTER)

        self.tree.column('nome', width=300, anchor=tk.W)
        self.tree.column('dimensao', width=150, anchor=tk.CENTER)
        self.tree.column('populacao', width=150, anchor=tk.CENTER)

        yscroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        xscroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=yscroll.set, xscroll=xscroll.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        yscroll.grid(row=0, column=1, sticky='ns')
        xscroll.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind('<Double-1>', self.on_double_click)

    def setup_status_bar(self):
        self.status_bar = tk.Label(self.root, text="Pronto", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def refresh_table(self, cidades=None):
        self.tree.delete(*self.tree.get_children())
        cidades = cidades if cidades else self.controller.listar_cidades()

        for cidade in cidades:
            self.tree.insert('', tk.END, values=(
                cidade.nome,
                f"{cidade.dimensao:,.2f}",
                f"{cidade.populacao:,d}"
            ))

    def show_list_view(self):
        for widget in self.main_frame.winfo_children():
            if widget not in [self.tree.master, self.btn_add.master]:
                widget.destroy()
        self.refresh_table()

    def show_add_form(self):
        self.form_window("Adicionar Cidade", self.save_cidade)

    def show_edit_form(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma cidade para editar")
            return
        item = self.tree.item(selected[0])
        nome = item['values'][0]
        cidade = self.controller.buscar_por_nome(nome)
        if cidade:
            self.form_window(
                "Editar Cidade",
                lambda data: self.update_cidade(nome, data),
                cidade
            )

    def form_window(self, title, save_callback, cidade=None):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.resizable(False, False)

        tk.Label(window, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        nome_entry = tk.Entry(window, width=30)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(window, text="Dimensão (km²):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        dimensao_entry = tk.Entry(window, width=30)
        dimensao_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(window, text="População:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        populacao_entry = tk.Entry(window, width=30)
        populacao_entry.grid(row=2, column=1, padx=5, pady=5)

        if cidade:
            nome_entry.insert(0, cidade.nome)
            dimensao_entry.insert(0, str(cidade.dimensao))
            populacao_entry.insert(0, str(cidade.populacao))

        btn_frame = tk.Frame(window)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Salvar", command=lambda: self.validate_and_save(
            nome_entry.get(),
            dimensao_entry.get(),
            populacao_entry.get(),
            save_callback,
            window
        )).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Cancelar", command=window.destroy).pack(side=tk.LEFT, padx=5)

    def validate_and_save(self, nome, dimensao, populacao, save_callback, window):
        if not nome:
            messagebox.showerror("Erro", "O nome da cidade é obrigatório")
            return
        try:
            dimensao = float(dimensao)
            populacao = int(populacao)
            if dimensao <= 0 or populacao <= 0:
                raise ValueError("Valores devem ser positivos")
            save_callback({
                'nome': nome.strip().title(),
                'dimensao': dimensao,
                'populacao': populacao
            })
            window.destroy()
            self.refresh_table()
        except ValueError as e:
            messagebox.showerror("Erro", f"Dados inválidos: {str(e)}")

    def save_cidade(self, data):
        self.controller.adicionar_cidade(data['nome'], data['dimensao'], data['populacao'])
        messagebox.showinfo("Sucesso", "Cidade adicionada com sucesso!")

    def update_cidade(self, nome_antigo, novos_dados):
        if self.controller.atualizar_cidade(nome_antigo, novos_dados):
            messagebox.showinfo("Sucesso", "Cidade atualizada com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível atualizar a cidade")

    def remover_cidade(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma cidade para remover")
            return
        item = self.tree.item(selected[0])
        nome = item['values'][0]
        if messagebox.askyesno("Confirmar", f"Remover a cidade {nome}?"):
            if self.controller.remover_cidade(nome):
                messagebox.showinfo("Sucesso", "Cidade removida com sucesso!")
                self.refresh_table()
            else:
                messagebox.showerror("Erro", "Não foi possível remover a cidade")

    def pesquisar_cidades(self):
        termo = self.search_entry.get().strip()
        if termo:
            cidades = self.controller.listar_cidades(filtro=termo)
            self.refresh_table(cidades)
        else:
            self.refresh_table()

    def importar_excel(self):
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if filepath:
            success, message = self.controller.importar_excel(filepath)
            if success:
                messagebox.showinfo("Sucesso", message)
                self.refresh_table()
            else:
                messagebox.showerror("Erro", message)

    def on_double_click(self, event):
        self.show_edit_form()

    def show_mais_extensa(self):
        cidade = self.controller.cidade_mais_extensa()
        if cidade:
            messagebox.showinfo("Cidade Mais Extensa", 
                              f"{cidade.nome} - {cidade.dimensao:,.2f} km²")
        else:
            messagebox.showwarning("Aviso", "Nenhuma cidade cadastrada")

    def show_mais_populosa(self):
        cidade = self.controller.cidade_mais_populosa()
        if cidade:
            messagebox.showinfo("Cidade Mais Populosa", 
                              f"{cidade.nome} - {cidade.populacao:,d} habitantes")
        else:
            messagebox.showwarning("Aviso", "Nenhuma cidade cadastrada")

    def show_media_populacao(self):
        media = self.controller.media_populacao()
        messagebox.showinfo("Média de População", 
                          f"Média populacional: {media:,.2f} habitantes")

    def show_menu_inicial(self):
        # Limpa o main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Título
        tk.Label(self.main_frame, text="Menu Inicial", font=("Arial", 20), bg=self.theme_manager.theme["bg"], fg=self.theme_manager.theme["fg"]).pack(pady=20)

        # Botões principais do menu inicial
        btns_info = [
            ("Adicionar Cidade", self.show_add_form),
            ("Listar Cidades", self.show_list_view),
            ("Cidade Mais Extensa", self.show_mais_extensa),
            ("Cidade Mais Populosa", self.show_mais_populosa),
            ("Média de População", self.show_media_populacao),
            ("Importar Excel", self.importar_excel)
        ]

        for (text, command) in btns_info:
            btn = tk.Button(self.main_frame, text=text, command=command, width=30, height=2,
                            bg=self.theme_manager.theme["button_bg"], fg=self.theme_manager.theme["button_fg"])
            btn.pack(pady=5)

    def show_add_form(self):
        # Limpa main_frame antes de abrir formulário dentro dele (ou abre em Toplevel como faz)
        # Se abrir dentro do main_frame, lembre de adicionar botão voltar que chama show_menu_inicial
        super_show_add_form = super().show_add_form if hasattr(super(), 'show_add_form') else None
        # Se está abrindo modal, só alterar o menu inicial para fechamento do modal
        # Aqui apenas exemplo do botão voltar:
        # posso abrir modal normalmente, botão voltar no modal é o Cancelar

        # Ao abrir aqui, o usuário fecha a modal e volta para o menu inicial automaticamente
        self.show_menu_inicial()
        # Mas para modal, basta não fazer nada

        # Como você usa janela modal, pode abrir normalmente:
        super_show_add_form()

    def show_list_view(self):
        # Aqui você pode limpar e mostrar a tabela normalmente
        # Se quiser adicionar o botão voltar, faça assim:

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Botão Voltar
        btn_voltar = tk.Button(self.main_frame, text="⬅ Voltar ao Menu", command=self.show_menu_inicial,
                               bg=self.theme_manager.theme["button_bg"], fg=self.theme_manager.theme["button_fg"])
        btn_voltar.pack(anchor="w", padx=10, pady=5)

        self.setup_table()
        self.refresh_table()

    # Adapte os outros métodos que mostram telas próprias para incluir botão voltar,
    # ou se forem modais (Toplevel) o botão cancelar já funciona como voltar.

# Ajuste a inicialização para abrir o menu inicial primeiro:

if __name__ == "__main__":
    root = tk.Tk()
    app = MainView(root)
    app.show_menu_inicial()  # Começa pelo menu inicial
    root.mainloop()