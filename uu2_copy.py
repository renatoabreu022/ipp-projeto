import customtkinter as ctk
from tkinter import messagebox
import json
import hashlib
import os
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from main import carregar_cidades_disponiveis

from engine.calculo_percurso3 import CalculoPeso
from models.user import Preferencias
from models.percursos import ParametrosAcessibilidade, ParametrosAmbiente, ParametrosPopulacao
from models.grafo import Mapa
from models.bicicletas import GestorBicicletas


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def carregar_bd(nome_ficheiro): 
    if os.path.exists(nome_ficheiro):
        try:
            with open(nome_ficheiro, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                return json.loads(conteudo) if conteudo else {}
        except: return {}
    return {}

def guardar_bd(dados, nome_ficheiro):
    try:
        with open(nome_ficheiro, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao guardar base de dados: {e}")

def carregar_cidades():
    with open('locais.json', 'r', encoding='utf-8') as f:
        locais = json.load(f)
    return locais

# --- BASE DE DADOS DE LOCAIS ---
DADOS_CIDADES = carregar_cidades()
class JanelaBicicletas(ctk.CTkToplevel):
    def __init__(self, master, gestor, db_cidades, mapa, utilizador_nome, bd_utilizadores):
        super().__init__(master)
        
        self.gestor = gestor
        self.db_cidades = db_cidades
        self.mapa = mapa
        self.utilizador_nome = utilizador_nome
        self.bd_utilizadores = bd_utilizadores
    
        self.title("Mobilidade Urbana - Bicicletas")
        self.geometry("414x740")
        self.configure(fg_color="#F4F1EA")
        self.resizable(False, False)
        
        self.grab_set() 
        
        self.master_app = master # Guarda a referência da janela principal
        self.gestor = gestor
        
        self.cor_fundo = "#F4F1EA"
        self.cor_verde_forte = "#2A8569"
        self.cor_texto = "#2A8569"  
        
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.protocol("WM_DELETE_WINDOW", self.voltar_ao_menu_principal)
        
        self.mostrar_tela_selecao()

    def limpar_ecra(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def mostrar_tela_selecao(self):
        self.limpar_ecra()
        
        ctk.CTkLabel(self.main_container, text="🚲 SISTEMA DE BICICLETAS", 
                    font=("Helvetica", 24, "bold"), text_color=self.cor_verde_forte).pack(pady=20)
        
        #Seleção de Cidade
        ctk.CTkLabel(self.main_container, text="Selecione a cidade:", font=("Helvetica", 14, "bold"), text_color=self.cor_texto).pack(pady=5)
        self.combo_cidades = ctk.CTkComboBox(
            self.main_container, 
            values=sorted(list(self.db_cidades.keys())), 
            width=300,
            command=self.atualizar_origens,
            state="readonly",
            fg_color="white",            
            border_color="#1F634E",     
            button_color="#1F634E",      
            button_hover_color="#2A8569", 
            text_color="black",           
            dropdown_fg_color="white",     
            dropdown_text_color="black"    
        )
        self.combo_cidades.pack(pady=10)
        self.combo_cidades.set("Escolha a cidade...")

        #Seleção de Origem
        ctk.CTkLabel(self.main_container, text="Onde se encontra agora?", font=("Helvetica", 14, "bold"), text_color=self.cor_texto).pack(pady=5)
        self.combo_origem = ctk.CTkComboBox(
            self.main_container, 
            values=[], 
            width=300,
            state="readonly",
            fg_color="white",             
            border_color="#1F634E",
            button_color="#1F634E",
            text_color="black",            
            dropdown_fg_color="white",
            dropdown_text_color="black"
        )
        self.combo_origem.pack(pady=10)
        self.combo_origem.set("Selecione a cidade primeiro")

        ctk.CTkButton(self.main_container, text="PESQUISAR ESTAÇÕES", fg_color="#2A8569", hover_color="#1F634E", height=45, width=250, command=self.ir_para_listagem).pack(pady=30)
        ctk.CTkButton(self.main_container, text="VOLTAR", fg_color="#757575", hover_color="#3E3E3E", command=self.voltar_ao_menu_principal).pack(pady=10)
        
    def voltar_ao_menu_principal(self):
        self.master_app.deiconify() # Mostra a janela principal de volta
        self.destroy()
    
    def atualizar_origens(self, cidade):
        if hasattr(self, 'cidades_ficheiros') and cidade in self.cidades_ficheiros:
            ficheiro = self.cidades_ficheiros[cidade]
            if os.path.exists(ficheiro):
                self.mapa.load_mapa(ficheiro)
        
        locais = self.db_cidades.get(cidade, [])
        self.combo_origem.configure(values=locais)
        if locais: self.combo_origem.set(locais[0])

    def ir_para_listagem(self):
        cidade = self.combo_cidades.get()
        origem = self.combo_origem.get()
        if "Escolha" in cidade or not origem:
            messagebox.showwarning("Aviso", "Selecione a cidade e localização.")
            return
        self.mostrar_tela_estacoes(cidade, origem)

    def mostrar_tela_estacoes(self, cidade, origem):
        self.limpar_ecra()
        self.gestor.gerar_estacoes_para_cidade(self.db_cidades[cidade])
        
        ctk.CTkLabel(self.main_container, text=f"Estações em {cidade}", font=("Helvetica", 20, "bold"), text_color=self.cor_verde_forte).pack(pady=10)

        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="white", corner_radius=10, height=350)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        for local, info in self.gestor.estacoes.items():
            f = ctk.CTkFrame(scroll, fg_color="transparent")
            f.pack(fill="x", pady=5)
            ctk.CTkLabel(f, text=f"📍 {local}", font=("Helvetica", 12), text_color=self.cor_texto).pack(side="left", padx=10)
            ctk.CTkLabel(f, text=f"{info['disponiveis']} 🚲 disponíveis", text_color=self.cor_verde_forte, font=("Helvetica", 14, "bold")).pack(side="right", padx=10)

        btn_box = ctk.CTkFrame(self.main_container, fg_color="transparent")
        btn_box.pack(pady=15)
        ctk.CTkButton(btn_box, text="CALCULAR PERCURSOS", fg_color="#2A8569", hover_color='#1F4E3D', command=lambda: self.abrir_popup_resultados(origem)).pack(side="left", padx=5)
        ctk.CTkButton(btn_box, text="VOLTAR", fg_color="#757575", hover_color="#3E3E3E", command=self.mostrar_tela_selecao).pack(side="left", padx=5)

    def abrir_popup_resultados(self, origem):
        hora_atual = datetime.now().hour
        ranking = []
        
        #preferências reais do utilizador da BD da interface principal
        prefs_raw = self.bd_utilizadores[self.utilizador_nome]["preferencias"]
        perfil = Preferencias()
        perfil.atualizar_parametros(prefs_raw)

        for estacao in self.gestor.estacoes.keys():
            res = self.mapa.pesquisa_perc(origem, estacao, perfil, hora=hora_atual, k=1)
            if res:
                score, caminho = res[0]
                ranking.append({'local': estacao, 'score': score, 'percurso': caminho})

        if not ranking:
            messagebox.showerror("Erro", "Não foi possível traçar rotas.")
            return

        ranking.sort(key=lambda x: x['score'])
        top_opcoes = ranking[:5]  

        popup = ctk.CTkToplevel(self)
        popup.title("Melhores Opções Encontradas")
        popup.geometry("414x740")
        popup.configure(fg_color=self.cor_fundo)
        popup.grab_set() 

        popup.protocol("WM_DELETE_WINDOW", lambda: self.fechar_popup(popup))
    
        ctk.CTkLabel(popup, text="SUGESTÕES DE PERCURSO", font=("Helvetica", 18, "bold"), text_color=self.cor_verde_forte).pack(pady=15)

        def fechar_popup(self, popup_window):
            popup_window.destroy()
            self.deiconify()
    
        
        scroll_res = ctk.CTkScrollableFrame(popup, fg_color="white", corner_radius=12)
        scroll_res.pack(fill="both", expand=True, padx=20, pady=10)

        for i, opcao in enumerate(top_opcoes):
            card = ctk.CTkFrame(scroll_res, fg_color="#F9F9F9", corner_radius=8, border_width=1, border_color="#E0E0E0")
            card.pack(fill="x", pady=8, padx=5)

            
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(header, text=f"{i+1}ª OPÇÃO: {opcao['local']}", font=("Helvetica", 13, "bold"), text_color=self.cor_verde_forte).pack(side="left")
            
            ctk.CTkLabel(header, text=f"Score: {round(opcao['score'], 1)}", font=("Helvetica", 12, "bold"), text_color="#299480").pack(side="right")

            scroll_rota = ctk.CTkScrollableFrame(
                card, 
                orientation="horizontal", 
                fg_color="transparent", 
                height=60, 
                scrollbar_button_color=self.cor_verde_forte, 
                scrollbar_button_hover_color="#2A8569"
            )
            scroll_rota.pack(fill="x", padx=10, pady=(0, 5))
            
            rota_texto = " -> ".join(opcao['percurso'])
            lbl_rota = ctk.CTkLabel(
                scroll_rota, 
                text=rota_texto, 
                font=("Helvetica", 11), 
                text_color=self.cor_texto
            )
            lbl_rota.pack(side="left", padx=5)

        ctk.CTkButton(popup, text="FECHAR", fg_color=self.cor_verde_forte, hover_color='#1F4E3D', command=popup.destroy).pack(pady=15)
        
    def calcular_rota(self, origem):
        hora_atual = datetime.now().hour
        ranking = []

        for estacao in self.gestor.estacoes.keys():
            res = self.mapa.pesquisa_perc(origem, estacao, self.user_login.u_preferencias, hora=hora_atual, k=1)
            if res:
                score, caminho = res[0]
                ranking.append({'local': estacao, 'score': score, 'percurso': caminho})

        if ranking:
            ranking.sort(key=lambda x: x['score'])
            melhor = ranking[0]
            
            msg = f"MELHOR OPÇÃO: {melhor['local']}\n"
            msg += f"Score de Conforto: {round(melhor['score'], 1)}\n\n"
            msg += f"Caminho: {' -> '.join(melhor['percurso'])}"
            messagebox.showinfo("Rota Sugerida", msg)
        else:
            messagebox.showerror("Erro", "Não foi possível traçar rota para as estações.")
            
    def voltar_atras(self):
        self.pop_listagem.destroy()
        self.pop_cidade.deiconify()

class AppAcessibilidade(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de Percursos")
        self.geometry("414x740")
        self.configure(fg_color="#F4F1EA")
        
        self.motor_mapa = Mapa()
        self.gestor_bike = GestorBicicletas()
        self.utilizador_atual = None
        self.bd = carregar_bd("utilizadores.json")
        self.mostrar_login()

    def limpar_janela(self):
        for widget in self.winfo_children(): widget.destroy()

    def mostrar_login(self):
        self.limpar_janela()
        ctk.CTkLabel(self, text="Seja Bem-Vind@!", font=("Helvetica", 24, "bold"), text_color="#2A8569").pack(pady=40)
        self.ent_user = ctk.CTkEntry(self, placeholder_text="Utilizador", width=250)
        self.ent_user.pack(pady=10)
        self.ent_pass = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.ent_pass.pack(pady=10)
        ctk.CTkButton(self, text="Entrar", command=self.fazer_login, width=250).pack(pady=20)
        ctk.CTkButton(self, text="Criar Conta", command=self.mostrar_registo, width=250, fg_color="transparent", text_color="#2A8569", border_width=2, border_color="#3AC098").pack()

    def fazer_login(self):
        user, pw = self.ent_user.get(), self.ent_pass.get()
        if user in self.bd and self.bd[user]["pass"] == hash_password(pw):
            self.utilizador_atual = user
            self.mostrar_menu_principal()
        else:
            messagebox.showerror("Erro", "Utilizador ou Password incorretos.")

    def mostrar_registo(self):
        self.limpar_janela()
        ctk.CTkLabel(self, text="Novo Registo", font=("Helvetica", 20, "bold"), text_color="#2A8569").pack(pady=30)
        self.reg_user = ctk.CTkEntry(self, placeholder_text="Utilizador", width=250)
        self.reg_user.pack(pady=10)
        self.reg_pass1 = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.reg_pass1.pack(pady=10)
        self.reg_pass2 = ctk.CTkEntry(self, placeholder_text="Confirmar Password", show="*", width=250)
        self.reg_pass2.pack(pady=10)
        ctk.CTkButton(self, text="Seguinte: Parâmetros", command=self.validar_registo, width=250).pack(pady=30)
        ctk.CTkButton(self, text="Voltar", command=self.mostrar_login, fg_color="#757575", hover_color="#3E3E3E").pack()

    def validar_registo(self):
        user, p1, p2 = self.reg_user.get(), self.reg_pass1.get(), self.reg_pass2.get()
        if not user or not p1: 
            messagebox.showwarning("Aviso", "Preencha todos os campos."); return
        if p1 != p2: 
            messagebox.showerror("Erro", "As passwords não coincidem."); return
        if user in self.bd: 
            messagebox.showerror("Erro", "Utilizador já existe."); return
        self.utilizador_atual, self.temp_pw = user, hash_password(p1)
        self.mostrar_preferencias(primeira_vez=True)

    def mostrar_menu_perfil(self):
        self.limpar_janela()
        ctk.CTkLabel(self, text="Definições de Perfil", font=("Helvetica", 22, "bold"), text_color="#2A8569").pack(pady=40)
        ctk.CTkButton(self, text="Alterar Parâmetros de Percurso", width=300, command=lambda: self.mostrar_preferencias(False)).pack(pady=15)
        ctk.CTkButton(self, text="Alterar Palavra-passe", width=300, command=self.mostrar_alterar_pass).pack(pady=15)
        ctk.CTkButton(self, text="Voltar ao Menu Principal", width=300, fg_color="#757575", hover_color="#3E3E3E", command=self.mostrar_menu_principal).pack(pady=30)

    def mostrar_alterar_pass(self):
        self.limpar_janela()
        ctk.CTkLabel(self, text="Alterar Password", font=("Helvetica", 20, "bold"), text_color="#2A8569").pack(pady=30)
        self.new_p1 = ctk.CTkEntry(self, placeholder_text="Nova Password", show="*", width=250)
        self.new_p1.pack(pady=10)
        self.new_p2 = ctk.CTkEntry(self, placeholder_text="Confirmar Nova Password", show="*", width=250)
        self.new_p2.pack(pady=10)
        ctk.CTkButton(self, text="Confirmar Alteração", command=self.confirmar_mudanca_pass).pack(pady=20)
        ctk.CTkButton(self, text="Cancelar", fg_color="#757575", hover_color="#3E3E3E", command=self.mostrar_menu_perfil).pack()

    def confirmar_mudanca_pass(self):
        p1, p2 = self.new_p1.get(), self.new_p2.get()
        if p1 == p2 and p1:
            self.bd[self.utilizador_atual]["pass"] = hash_password(p1)
            guardar_bd(self.bd, "utilizadores.json")
            messagebox.showinfo("Sucesso", "Password alterada com sucesso!")
            self.mostrar_menu_perfil()
        else: messagebox.showerror("Erro", "As passwords não coincidem.")

    

    def mostrar_preferencias(self, primeira_vez=False):
        self.limpar_janela()
        self.geometry("414x740")
        titulo = "Parâmetros de Acessibilidade"
        ctk.CTkLabel(self, text=titulo, font=("Helvetica", 18, "bold"), text_color="#2A8569").pack(pady=10)
        
        ctk.CTkButton(self, text="Guardar Perfil", command=lambda: self.finalizar_guardar(primeira_vez)).pack(side="bottom", pady=20)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#F4F1EA", width=380, height=500)
        self.scroll.pack(padx=20, pady=10, fill="both", expand=True)

        self.sliders = {}

        # ACESSIBILIDADE
        self.criar_label_seccao(self.scroll, "Acessibilidade Física")
        self.sliders["pavimento"] = self.criar_item_slider(self.scroll, "Regularidade pavimento:")
        self.sliders["inclinacao"] = self.criar_item_slider(self.scroll, "Inclinação/Rampas:")
        self.sliders["passeios"] = self.criar_item_slider(self.scroll, "Presença de Passeios:")
        self.sliders["escadas"] = self.criar_item_slider(self.scroll, "Presença de Escadas:")
        self.c_pod = ctk.CTkCheckBox(self.scroll, text="Piso Podotátil (Textura Cego)", border_color="#3AC098", fg_color="#3AC098")
        self.c_pod.pack(anchor="w", pady=10)

        # AMBIENTE
        self.criar_label_seccao(self.scroll, "Conforto e Ambiente")
        self.sliders["sombra"] = self.criar_item_slider(self.scroll, "Sombra:")
        self.sliders["qualidade_ar"] = self.criar_item_slider(self.scroll, "Qualidade do Ar:")
        self.sliders["nivel_polen"] = self.criar_item_slider(self.scroll, "Presença de Pólen:")
        self.sliders["poluicao_sonora"] = self.criar_item_slider(self.scroll, "Poluição Sonora:")
        self.sliders["poluicao_visual"] = self.criar_item_slider(self.scroll, "Poluição Visual:")
        self.sliders["iluminacao"] = self.criar_item_slider(self.scroll, "Iluminação:")

        # MOVIMENTO
        self.criar_label_seccao(self.scroll, "População e Movimento")
        self.sliders["transito"] = self.criar_item_slider(self.scroll, "Evitar Trânsito:")
        self.sliders["multidao"] = self.criar_item_slider(self.scroll, "Evitar Multidões:")

        if not primeira_vez:
            p = self.bd[self.utilizador_atual]["preferencias"]
            for k, v in p.items():
                if k in self.sliders: self.sliders[k].set(v)
            if p.get("textura_cego") == 10: self.c_pod.select()

    def criar_label_seccao(self, master, texto):
        ctk.CTkLabel(master, text=texto, font=("Helvetica", 13, "bold"), text_color="#1F4E3D").pack(anchor="w", pady=(15, 5))

    def criar_item_slider(self, master, texto):
        f = ctk.CTkFrame(master, fg_color="transparent")
        f.pack(fill="x", pady=2)
        ctk.CTkLabel(f, text=texto, width=150, anchor="w", font=("Helvetica", 11)).grid(row=0, column=0)
        s = ctk.CTkSlider(f, from_=1, to=10, number_of_steps=9, progress_color="#3AC098", button_color="#2A8569")
        s.set(5); s.grid(row=0, column=1, sticky="ew")
        f.grid_columnconfigure(1, weight=1)
        return s

    def finalizar_guardar(self, primeira_vez):
        dict_prefs = {k: int(s.get()) for k, s in self.sliders.items()}
        dict_prefs["textura_cego"] = 10 if self.c_pod.get() else 0
        
        if primeira_vez:
            self.bd[self.utilizador_atual] = {"pass": self.temp_pw, "preferencias": dict_prefs}
        else:
            self.bd[self.utilizador_atual]["preferencias"] = dict_prefs
        
        guardar_bd(self.bd, "utilizadores.json")
        messagebox.showinfo("Sucesso", "Perfil atualizado!")
        self.mostrar_menu_principal()

    # --- MENU PRINCIPAL ---

    def mostrar_menu_principal(self):
        self.limpar_janela()
        self.geometry("414x740")
        self.configure(fg_color="#F4F1EA")
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text=f"Olá, {self.utilizador_atual}!", font=("Helvetica", 20, "bold"), text_color="#2A8569").pack(side="left")
        ctk.CTkButton(header, text="👤 Perfil", width=80, fg_color="#3AC098", command=self.mostrar_menu_perfil).pack(side="right")
        
        f_top = ctk.CTkFrame(self, fg_color='transparent')
        f_top.pack(fill='x', padx=20)
        f_top.grid_columnconfigure((0,1), weight=1)

        self.cb_cidade = ctk.CTkComboBox(f_top, values=list(DADOS_CIDADES.keys()), width=300, command=self.ao_mudar_cidade, button_color="#2A8569", border_color="#3AC098")
        self.cb_cidade.grid(row=0, column=0, padx=(0,5), sticky='ew')

        self.cb_hora = ctk.CTkComboBox(f_top, values=[f"{str(i).zfill(2)}:00" for i in range(24)], button_color="#2A8569", border_color="#3AC098")
        self.cb_hora.set(f"{str(datetime.now().hour).zfill(2)}:00")
        self.cb_hora.grid(row=0, column=1, padx=(0,5), sticky='ew')

        self.f_mapa = ctk.CTkFrame(self, fg_color='white', corner_radius=15, border_width=2, border_color="#D3D3D3")
        self.f_mapa.pack(padx=20, pady=15, fill='both', expand=True)

        f_bottom = ctk.CTkFrame(self, fg_color='transparent')
        f_bottom.pack(fill='x', padx=20, pady=(0,10))
        f_bottom.grid_columnconfigure(0, weight=3)
        f_bottom.grid_columnconfigure(1, weight=1)
        f_bottom.grid_columnconfigure(2, weight=1)

        f_inputs = ctk.CTkFrame(f_bottom, fg_color='transparent')
        f_inputs.grid(row=0, column=0, sticky='ew', padx=(0,10))

        self.cb_origem = ctk.CTkComboBox(f_inputs, values=[], button_color="#2A8569", border_color="#3AC098")
        self.cb_origem.pack(pady=2, fill='x')

        self.cb_destino = ctk.CTkComboBox(f_inputs, values=[], button_color="#2A8569", border_color="#3AC098")
        self.cb_destino.pack(pady=2, fill='x')

        btn_calc = ctk.CTkButton(f_bottom, text='🚶', command=self.simular_calculo, fg_color="#2A8569", hover_color="#1F4E3D", width=60, height=65, font=("Helvetica", 24))
        btn_calc.grid(row=0, column=1, sticky='nsew')
        btn_bike = ctk.CTkButton(f_bottom, text="🚲", command=self.abrir_interface_bicicletas, fg_color="#2A8569", hover_color="#1F4E3D", width=60, height=65, font=("Helvetica", 24))
        btn_bike.grid(row=0, column=2, sticky='nsew')

        ctk.CTkButton(self, text="Sair", command=self.mostrar_login, fg_color="#C62828", hover_color="#761616", width=100).pack(pady=5)

        self.ao_mudar_cidade(self.cb_cidade.get())
    def abrir_interface_bicicletas(self):
        # Dicionário de ficheiros igual ao encontrado no uu2.py
        cidades_disponiveis = carregar_cidades_disponiveis() 
        self.withdraw()
        # Cria a janela de bicicletas (deves copiar a classe JanelaBicicletas do uu2.py para o seu ficheiro ou importá-la)
        janela = JanelaBicicletas(
            self, 
            gestor=self.gestor_bike, 
            db_cidades=DADOS_CIDADES, 
            mapa=self.motor_mapa, 
            utilizador_nome=self.utilizador_atual,
            bd_utilizadores=self.bd
        )
        janela.cidades_ficheiros = cidades_disponiveis

    def atualizar_locais(self, cidade):
        locais = DADOS_CIDADES.get(cidade, [])
        self.cb_origem.configure(values=locais)
        self.cb_destino.configure(values=locais)
        if locais:
            self.cb_origem.set(locais[0])
            self.cb_destino.set(locais[1] if len(locais) > 1 else locais[0])
    
    def ao_mudar_cidade(self, cidade):
        self.atualizar_locais(cidade)

        cidades_disponiveis = carregar_cidades_disponiveis()

        ficheiro = cidades_disponiveis.get(cidade)
        if ficheiro and os.path.exists(ficheiro):
            self.motor_mapa = Mapa()
            self.motor_mapa.load_mapa(ficheiro)
            self.visualizar_caminhos(cidade, [])

    def simular_calculo(self):
        # 1. Obter os dados selecionados na interface
        cidade_selecionada = self.cb_cidade.get()
        origem = self.cb_origem.get()
        destino = self.cb_destino.get()
        
        # Obter a hora (opcional)
        try:
            hora_txt = self.cb_hora.get().split(":")[0]
            h_calculo = int(hora_txt)
        except:
            h_calculo = datetime.now().hour

        
        cidades_disponiveis = carregar_cidades_disponiveis()

        # 3. Procurar o ficheiro correspondente
        ficheiro_mapa = cidades_disponiveis.get(cidade_selecionada)

        if not ficheiro_mapa or not os.path.exists(ficheiro_mapa):
            messagebox.showerror("Erro", f"O mapa de {cidade_selecionada} não foi encontrado.\nCaminho: {ficheiro_mapa}")
            return

        try:
            # 4. Carregar o mapa
            self.motor_mapa = Mapa()
            self.motor_mapa.load_mapa(ficheiro_mapa)
            
            
            print(f"--- SIMULAÇÃO ---")
            print(f"Cidade: {cidade_selecionada} | Ficheiro: {ficheiro_mapa}")
            print(f"Rota: {origem} -> {destino}")

            # 5. Configurar as preferências do utilizador (Carregadas do JSON)
            p_user = self.bd[self.utilizador_atual]["preferencias"]
            perfil = Preferencias()
            perfil.atualizar_parametros(p_user)

            # 6. Executar o cálculo de percurso
            # Nota: k=3 para dar 3 opções de rota
            resultados = self.motor_mapa.pesquisa_perc(origem, destino, perfil, hora=h_calculo, k=5)

            # 7. Mostrar resultados
            if not resultados:
                messagebox.showwarning("Aviso", "Não foi possível encontrar um caminho entre esses pontos.")
                return
            
            self.visualizar_caminhos(cidade_selecionada, resultados)

            texto = f"Sugestões para {cidade_selecionada} ({h_calculo}h):\n\n"
            for i, (score, caminho) in enumerate(resultados):
                texto += f"OPÇÃO {i+1} (Esforço: {score:.2f})\n"
                texto += " ➔ ".join(caminho) + "\n\n"
            
            messagebox.showinfo("Rotas Recomendadas", texto)
            
        except Exception as e:
            # Se houver um erro (como aquele do 'no setter' ou nome inexistente), aparece aqui
            print(f"ERRO NO CÁLCULO: {e}")
            messagebox.showerror("Erro no Processamento", f"Ocorreu um erro: {e}")

    def visualizar_caminhos(self, cidade_nome, resultados):
        # Limpar o frame do mapa antes de desenhar
        for widget in self.f_mapa.winfo_children():
            widget.destroy()

        # Criar o grafo do NetworkX
        G = nx.Graph()
        if not hasattr(self, 'motor_mapa') or not self.motor_mapa.adjacencias:
            return # Evita erro se o mapa ainda não estiver carregado

        for origem, vizinhos in self.motor_mapa.adjacencias.items():
            for ligacao in vizinhos:
                G.add_edge(origem, ligacao["destino"])

        # Tentar obter as coordenadas GPS
        if hasattr(self, 'motor_mapa') and self.motor_mapa.coordenadas:
        # Assegura que passamos o tuplo (x, y) diretamente
            pos = {local: coord for local, coord in self.motor_mapa.coordenadas.items()}
        else:
            pos = nx.spring_layout(G, seed=42)

        # Configuração da Figura Matplotlib
        fig = plt.Figure(figsize=(5, 4), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        ax.set_facecolor('white')
        ax.set_title(f"Visualização: {cidade_nome}", color="#2A8569", fontdict={'fontsize': 12, 'fontweight': 'bold'})

        # Desenhar o mapa base (estilo original)
        nx.draw_networkx_nodes(G, pos, node_size=120, node_color="#3AC098", ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color="#E0E0E0", width=1.5, alpha=0.6, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=7, font_color="#1F4E3D", ax=ax)

        # Desenhar rotas calculadas
        if resultados:
            cores_rota = ["#E63946", "#457B9D", "#FFB703", "#8338EC", "#FB5607"]
            for idx, (score, caminho) in enumerate(resultados[:5]):
                arestas_caminho = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
                nx.draw_networkx_edges(G, pos, edgelist=arestas_caminho, 
                                     edge_color=cores_rota[idx], width=3, 
                                     label=f"Opção {idx+1}", ax=ax)
            ax.legend(fontsize='8')

        ax.axis('off')

        # Integrar no Canvas do Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.f_mapa)
        canvas.draw()
        
        # Barra de Ferramentas (Toolbar) para Pan/Zoom interativo
        toolbar = NavigationToolbar2Tk(canvas, self.f_mapa, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side="bottom", fill="x")
        
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AppAcessibilidade()
    app.mainloop()