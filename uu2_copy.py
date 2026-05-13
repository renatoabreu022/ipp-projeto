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

class AppAcessibilidade(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de Percursos")
        self.geometry("414x740")
        self.configure(fg_color="#F4F1EA")
        
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
        ctk.CTkButton(self, text="Voltar", command=self.mostrar_login, fg_color="gray").pack()

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
        ctk.CTkButton(self, text="Voltar ao Menu Principal", width=300, fg_color="gray", command=self.mostrar_menu_principal).pack(pady=30)

    def mostrar_alterar_pass(self):
        self.limpar_janela()
        ctk.CTkLabel(self, text="Alterar Password", font=("Helvetica", 20, "bold"), text_color="#2A8569").pack(pady=30)
        self.new_p1 = ctk.CTkEntry(self, placeholder_text="Nova Password", show="*", width=250)
        self.new_p1.pack(pady=10)
        self.new_p2 = ctk.CTkEntry(self, placeholder_text="Confirmar Nova Password", show="*", width=250)
        self.new_p2.pack(pady=10)
        ctk.CTkButton(self, text="Confirmar Alteração", command=self.confirmar_mudanca_pass).pack(pady=20)
        ctk.CTkButton(self, text="Cancelar", fg_color="gray", command=self.mostrar_menu_perfil).pack()

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

        f_inputs = ctk.CTkFrame(f_bottom, fg_color='transparent')
        f_inputs.grid(row=0, column=0, sticky='ew', padx=(0,10))

        self.cb_origem = ctk.CTkComboBox(f_inputs, values=[], button_color="#2A8569", border_color="#3AC098")
        self.cb_origem.pack(pady=2, fill='x')

        self.cb_destino = ctk.CTkComboBox(f_inputs, values=[], button_color="#2A8569", border_color="#3AC098")
        self.cb_destino.pack(pady=2, fill='x')

        btn_calc = ctk.CTkButton(f_bottom, text='CALCULAR ROTA', command=self.simular_calculo, fg_color="#2A8569", hover_color="#1F4E3D", height=65, font=("Helvetica", 13, "bold"))
        btn_calc.grid(row=0, column=1, sticky='nsew')

        ctk.CTkButton(self, text="Sair", command=self.mostrar_login, fg_color="#C62828", width=100).pack(pady=5)

        self.ao_mudar_cidade(self.cb_cidade.get())

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
            resultados = self.motor_mapa.pesquisa_perc(origem, destino, perfil, k=5)

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
        try:
            # Usa self.motor_mapa.coordenadas que é o atributo correto da classe Mapa
            pos = {local: (coord, coord) for local, coord in self.motor_mapa.coordenadas.items()}
        except Exception as e:
            print(f"Erro nas coordenadas: {e}. A usar layout automático.")
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