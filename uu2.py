import customtkinter as ctk
from tkinter import messagebox
import json
import hashlib
import os
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt


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

# --- BASE DE DADOS DE LOCAIS ---
DADOS_CIDADES = {
    "Porto": [
    "FEUP", "Farmácia Barreiros", "Jardim do Palácio de Cristal", "Estação de São Bento", 
    "NorteShopping", "Centro Hospitalar Universitário de São João", "Bebedouro Jardim do Morro", 
    "Posto de Primeiros Socorros Aliados", "Ecoponto Asprela", "WC Público Cordoaria", "Zona de Descanso Aliados"
  ],

  "Braga": [
    "Bom Jesus do Monte", "Avenida da Liberdade", "Hospital de Braga", "Universidade do Minho - Gualtar", 
    "Braga Parque", "Bebedouro Arcada", "Ciclovia do Rio Este", "Ecoponto Gualtar", "WC Público Praça do Município"
  ],

  "Fafe": [
    "Praça Mártires de Ferreira do Amaral", "Hospital da Misericórdia", "Parque da Cidade", "Pavilhão Multiusos", 
    "Terminal Rodoviário", "Bebedouro Parque da Cidade", "Parque Infantil do Centro", "Ecoponto Multiusos"
  ],

  "Marco de Canaveses": [
    "Igreja de Santa Maria (Siza Vieira)", "Hospital Santa Isabel", "Estação Ferroviária", "Jardim Municipal", 
    "Marco Fórum", "Bebedouro Jardim Municipal", "Posto de Informação Turística", "Ecoponto Marco Fórum"
  ],

  "Guimarães": [
    "Castelo de Guimarães", "Hospital da Senhora da Oliveira", "Universidade do Minho (Azurém)", 
    "GuimarãeShopping", "Largo do Toural", "Bebedouro Largo da Oliveira", "Parque da Cidade Guimarães", "WC Público Toural"
  ],

  "Vila Nova de Gaia": [
    "El Corte Inglés", "Hospital Eduardo Santos Silva", "Cais de Gaia", "GaiaShopping", "Jardim do Morro", 
    "Bebedouro Cais de Gaia", "Ciclovia da Orla Marítima", "Ecoponto Jardim do Morro"
  ],

  "Famalicão": [
    "Hospital de Famalicão", "Parque da Devesa", "Estação de Famalicão", "Universidade Lusíada", 
    "Praça D. Maria II", "Bebedouro Parque da Devesa", "Posto de Primeiros Socorros", "WC Público Praça D. Maria II"
  ],

  "Barcelos": [
    "IPCA", "Campo da Feira", "Hospital Santa Maria Maior", "Templo do Senhor da Cruz", 
    "Estação de Barcelos", "Bebedouro IPCA", "Parque Infantil de Barcelos", "Ecoponto Estação"
  ],

  "Póvoa de Varzim": [
    "Casino da Póvoa", "Hospital da Luz Póvoa de Varzim", "Passeio Alegre", "Biblioteca Municipal Rocha Peixoto", 
    "Estação de Metro da Póvoa", "Bebedouro Passeio Alegre", "Posto de Socorros da Praia", "WC Público Biblioteca"
  ],

  "Coimbra": [
    "Universidade de Coimbra - Polo I", "Hospitais da Universidade de Coimbra", "Portugal dos Pequenitos", 
    "Estação Coimbra-B", "Forum Coimbra", "Bebedouro Praça da República", "Parque Verde do Mondego", "WC Público Baixa"
  ],

  "Figueira da Foz": [
    "Casino Figueira", "Hospital Distrital da Figueira da Foz", "Mercado Municipal", "Torre do Relógio", 
    "Parque das Abadias", "Bebedouro Marginal", "Ciclovia da Marginal", "Ecoponto Mercado"
  ],

  "Covilhã": [
    "UBI", "Centro Hospitalar Cova da Beira", "Praça do Município", "Serra Shopping", 
    "Ponte da Carpinteira", "Bebedouro UBI", "Jardim Público da Covilhã", "WC Público Praça"
  ],

  "Caldas da Rainha": [
    "Praça da Fruta", "Hospital Termal", "Parque D. Carlos I", "Centro Comercial La Vie", 
    "ESAD.CR", "Bebedouro Parque D. Carlos I", "Posto de Informação"
  ],

  "Tomar": [
    "Convento de Cristo", "Praça da República", "Hospital de Tomar", "Mata dos Sete Montes", 
    "Politécnico de Tomar", "Bebedouro Mata", "Parque do Mouchão", "WC Público Centro"
  ],

  "Viseu": [
    "Sé de Viseu", "Palácio do Gelo", "Hospital de São Teotónio", "Parque do Fontelo", 
    "Rossio", "Bebedouro Parque do Fontelo", "Ecoponto Sé", "Posto de Primeiros Socorros"
  ],

  "Aveiro": [
    "Fórum Aveiro", "Universidade de Aveiro", "Estação de Aveiro", "Hospital Infante D. Pedro", 
    "Salinas de Aveiro", "Bebedouro Salinas", "Parque Infante D. Pedro", "WC Público Estação"
  ],

  "Lisboa": [
    "Hospital de Santa Maria", "Estação do Oriente", "Castelo de São Jorge", "Terreiro do Paço", 
    "Centro Comercial Colombo", "Bebedouro Parque das Nações", "Jardim da Estrela", "WC Público Rossio", "Posto Polícia Baixa"
  ],

  "Évora": [
    "Sé de Évora", "Templo Romano", "Colégio do Espírito Santo", "Hospital do Espírito Santo", 
    "Praça do Giraldo", "Bebedouro Templo Romano", "Jardim Público de Évora", "Ecoponto Centro"
  ],

  "Beja": [
    "Castelo de Beja", "Hospital José Joaquim Fernandes", "Politécnico de Beja", "Parque de Feiras", 
    "Museu Regional", "Bebedouro Castelo", "Parque de Merendas", "WC Público Parque de Feiras"
  ],

  "Portimão": [
    "Portimão Arena", "Hospital Particular", "Praia da Rocha", "Aqua Portimão", 
    "Museu de Portimão", "Bebedouro Praia da Rocha", "Posto de Socorros Marítimo", "WC Público Centro"
  ],

  "Lagos": [
    "Marina de Lagos", "Hospital de Lagos", "Mercado Municipal", "Ponta da Piedade", 
    "Praça Infante Dom Henrique", "Bebedouro Marina", "Centro de Ciência Viva", "WC Público Centro"
  ],

  "Faro": [
    "UAlg - Penha", "Hospital de Faro", "Fórum Algarve", "Doca de Faro", "Arco da Vila", 
    "Bebedouro Doca", "Parque Ribeirinho", "Ecoponto Fórum"
  ]
    
    
}

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
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text=f"Olá, {self.utilizador_atual}!", font=("Helvetica", 20, "bold"), text_color="#2A8569").pack(side="left")
        ctk.CTkButton(header, text="👤 Perfil", width=80, fg_color="#3AC098", command=self.mostrar_menu_perfil).pack(side="right")
        
        f_main = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        f_main.pack(padx=20, pady=10, fill="both", expand=True)

        ctk.CTkLabel(f_main, text="Cidade:", font=("Helvetica", 12)).pack(pady=(15, 0))
        self.cb_cidade = ctk.CTkComboBox(f_main, values=list(DADOS_CIDADES.keys()), width=300, command=self.atualizar_locais)
        self.cb_cidade.pack(pady=5)

        ctk.CTkLabel(f_main, text="Partida:", font=("Helvetica", 12)).pack()
        self.cb_origem = ctk.CTkComboBox(f_main, values=[], width=300)
        self.cb_origem.pack(pady=5)

        ctk.CTkLabel(f_main, text="Destino:", font=("Helvetica", 12)).pack()
        self.cb_destino = ctk.CTkComboBox(f_main, values=[], width=300)
        self.cb_destino.pack(pady=5)

        ctk.CTkLabel(f_main, text="Horário do Percurso:", font=("Helvetica", 12)).pack()
        self.cb_hora = ctk.CTkComboBox(f_main, values=[f"{str(i).zfill(2)}:00" for i in range(24)], width=300)
        self.cb_hora.set(f"{str(datetime.now().hour).zfill(2)}:00")
        self.cb_hora.pack(pady=5)

        self.atualizar_locais(self.cb_cidade.get())

        ctk.CTkButton(f_main, text="CALCULAR ROTA IDEAL", command=self.simular_calculo, height=45, font=("Helvetica", 13, "bold")).pack(pady=25)
        ctk.CTkButton(self, text="Sair", command=self.mostrar_login, fg_color="#C62828", width=100).pack(pady=10)

    def atualizar_locais(self, cidade):
        locais = DADOS_CIDADES.get(cidade, [])
        self.cb_origem.configure(values=locais)
        self.cb_destino.configure(values=locais)
        if locais:
            self.cb_origem.set(locais[0])
            self.cb_destino.set(locais[1] if len(locais) > 1 else locais[0])

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

        
        cidades_disponiveis = {
            "Aveiro": "city/grafo_aveiro.json",
            "Barcelos": "city/grafo_barcelos.json",
            "Beja": "city/grafo_beja.json",
            "Braga": "city/grafo_braga.json",
            "Caldas da Rainha": "city/grafo_caldas_da_rainha.json",
            "Coimbra": "city/grafo_coimbra.json",
            "Covilhã": "city/grafo_covilhã.json",
            "Évora": "city/grafo_évora.json",
            "Fafe": "city/grafo_fafe.json",
            "Famalicão": "city/grafo_famalicão.json",
            "Faro": "city/grafo_faro.json",
            "Figueira da Foz": "city/grafo_figueira_da_foz.json",
            "Guimarães": "city/grafo_guimarães.json",
            "Lagos": "city/grafo_lagos.json",
            "Lisboa": "city/grafo_lisboa.json",
            "Marco de Canaveses": "city/grafo_marco_de_canaveses.json",
            "Portimão": "city/grafo_portimão.json",
            "Porto": "city/grafo_porto.json",
            "Póvoa de Varzim": "city/grafo_póvoa_de_varzim.json",
            "Tomar": "city/grafo_tomar.json",
            "Viseu": "city/grafo_viseu.json",
            "Vila Nova de Gaia": "city/grafo_vila_nova_de_gaia.json"
        }

        # 3. Procurar o ficheiro correspondente
        ficheiro_mapa = cidades_disponiveis.get(cidade_selecionada)

        if not ficheiro_mapa or not os.path.exists(ficheiro_mapa):
            messagebox.showerror("Erro", f"O mapa de {cidade_selecionada} não foi encontrado.\nCaminho: {ficheiro_mapa}")
            return

        try:
            # 4. Carregar o mapa
            mapa = Mapa()
            mapa.load_mapa(ficheiro_mapa)
            
            
            print(f"--- SIMULAÇÃO ---")
            print(f"Cidade: {cidade_selecionada} | Ficheiro: {ficheiro_mapa}")
            print(f"Rota: {origem} -> {destino}")

            # 5. Configurar as preferências do utilizador (Carregadas do JSON)
            p_user = self.bd[self.utilizador_atual]["preferencias"]
            perfil = Preferencias()
            perfil.atualizar_parametros(p_user)

            # 6. Executar o cálculo de percurso
            # Nota: k=3 para dar 3 opções de rota
            resultados = mapa.pesquisa_perc(origem, destino, perfil, k=5)

            # 7. Mostrar resultados
            if not resultados:
                messagebox.showwarning("Aviso", "Não foi possível encontrar um caminho entre esses pontos.")
                return

            texto = f"Sugestões para {cidade_selecionada} ({h_calculo}h):\n\n"
            for i, (score, caminho) in enumerate(resultados):
                texto += f"OPÇÃO {i+1} (Esforço: {score:.2f})\n"
                texto += " ➔ ".join(caminho) + "\n\n"
            
            messagebox.showinfo("Rotas Recomendadas", texto)
            self.visualizar_caminhos(cidade, resultados)

        except Exception as e:
            # Se houver um erro (como aquele do 'no setter' ou nome inexistente), aparece aqui
            print(f"ERRO NO CÁLCULO: {e}")
            messagebox.showerror("Erro no Processamento", f"Ocorreu um erro: {e}")

        def visualizar_caminhos(self, cidade_nome, resultados):
            """ Cria a janela com o mapa e os 5 caminhos destacados """
            G = nx.Graph()
            
            # 1. Carregar todas as ligações do mapa (o fundo cinzento)
            for origem, vizinhos in self.motor_mapa.adjacencias.items():
                for ligacao in vizinhos:
                    G.add_edge(origem, ligacao["destino"])

            # 2. Tentar usar as coordenadas reais do JSON
            try:
                # O NetworkX usa (Longitude, Latitude) para o eixo X,Y
                pos = {local: (coord[1], coord[0]) for local, coord in self.motor_mapa.dados["coordenadas"].items()}
            except:
                # Se falhar, ele espalha os nós automaticamente
                pos = nx.spring_layout(G, seed=42)

            plt.figure(figsize=(10, 8))
            plt.title(f"Visualização de Percursos: {cidade_nome}")

            # 3. Desenhar o grafo base (nós e arestas em cinzento)
            nx.draw_networkx_nodes(G, pos, node_size=300, node_color="#D3D3D3")
            nx.draw_networkx_edges(G, pos, edge_color="#E0E0E0", width=1, alpha=0.5)
            nx.draw_networkx_labels(G, pos, font_size=8)

            # 4. Desenhar os 5 caminhos calculados com cores diferentes
            cores = ["#FF0000", "#0000FF", "#008000", "#FFA500", "#800080"] # Vermelho, Azul, Verde, Laranja, Roxo
            
            for idx, (score, caminho) in enumerate(resultados):
                if idx >= 5: break # Limite de 5 rotas
                
                # Converte a lista ['A', 'B', 'C'] em pares [('A','B'), ('B','C')]
                arestas_caminho = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
                
                nx.draw_networkx_edges(
                    G, pos, 
                    edgelist=arestas_caminho, 
                    edge_color=cores[idx], 
                    width=3, 
                    label=f"Opção {idx+1} (Peso: {score:.2f})"
                )

            plt.legend()
            plt.show() # Abre a janela do gráfico

if __name__ == "__main__":
    app = AppAcessibilidade()
    app.mainloop()