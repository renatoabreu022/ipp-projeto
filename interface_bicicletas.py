import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class AppBicicletas(ctk.CTk):
    def __init__(self, gestor, db_cidades, mapa, user_login):
        super().__init__()
        
        self.gestor = gestor
        self.db_cidades = db_cidades
        self.mapa = mapa
        self.user_login = user_login
    
        self.title("Mobilidade Urbana - Bicicletas")
        self.geometry("414x740")
        self.configure(fg_color="#F4F1EA")
        
        
        self.cor_fundo = "#F4F1EA"
        self.cor_verde_forte = "#299480"
        self.cor_texto = "#000000"  
        
        
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_tela_selecao()

    def limpar_ecra(self, container=None):
        target = container if container else self.main_container
        for widget in target.winfo_children():
            widget.destroy()

    def mostrar_tela_selecao(self):
        self.limpar_ecra()
        
        ctk.CTkLabel(self.main_container, text="🚲SISTEMA DE BICICLETAS", 
                    font=("Helvetica", 24, "bold"), text_color=self.cor_verde_forte).pack(pady=20)
        
        # Seleção de Cidade
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

        # Seleção de Origem
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

    def atualizar_origens(self, cidade):
        locais = self.db_cidades.get(cidade, [])
        self.combo_origem.configure(values=locais)
        if locais: 
            self.combo_origem.set(locais[0])

    def ir_para_listagem(self):
        cidade = self.combo_cidades.get()
        origem = self.combo_origem.get()
        
        if "Escolha" in cidade or not origem or "Selecione" in origem:
            messagebox.showwarning("Aviso", "Selecione a cidade e a sua localização.")
            return

        self.mostrar_tela_estacoes(cidade, origem)

    def mostrar_tela_estacoes(self, cidade, origem):
        self.limpar_ecra()
        
        self.gestor.gerar_estacoes_para_cidade(self.db_cidades[cidade])
        
        ctk.CTkLabel(self.main_container, text=f"Estações em {cidade}", 
                    font=("Helvetica", 20, "bold"), text_color=self.cor_verde_forte).pack(pady=10)

        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="white", corner_radius=10, height=280)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        for local, info in self.gestor.estacoes.items():
            f = ctk.CTkFrame(scroll, fg_color="transparent")
            f.pack(fill="x", pady=5)
            ctk.CTkLabel(f, text=f"📍 {local}", font=("Helvetica", 12), text_color=self.cor_texto).pack(side="left", padx=10)
            ctk.CTkLabel(f, text=f"{info['disponiveis']} 🚲 disponíveis", text_color=self.cor_verde_forte, font=("Helvetica", 13, "bold")).pack(side="right", padx=10)

        btn_box = ctk.CTkFrame(self.main_container, fg_color="transparent")
        btn_box.pack(pady=15)

        ctk.CTkButton(btn_box, text="CALCULAR PERCURSOS", fg_color="#299480", hover_color="#1F634E",  command=lambda: self.abrir_popup_resultados(origem)).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_box, text="VOLTAR", fg_color="#757575", hover_color="#616161", command=self.mostrar_tela_selecao).pack(side="left", padx=5)

    def abrir_popup_resultados(self, origem):
        hora_atual = datetime.now().hour
        ranking = []

        for estacao in self.gestor.estacoes.keys():
            res = self.mapa.pesquisa_perc(origem, estacao, self.user_login.u_preferencias, hora=hora_atual, k=1)
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

        ctk.CTkLabel(popup, text="SUGESTÕES DE PERCURSO", font=("Helvetica", 18, "bold"), text_color=self.cor_verde_forte).pack(pady=15)

        
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

        ctk.CTkButton(popup, text="FECHAR", fg_color=self.cor_verde_forte, command=popup.destroy).pack(pady=15)
        
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
        
