#-------@Cláudia e @Inês------ 03/05/2026

import customtkinter as ctk
from tkinter import messagebox

# Configurações globais de design
ctk.set_appearance_mode("light")  # Modo Claro
ctk.set_default_color_theme("green")  # Tema verde padrão para botões e sliders

class MenuPercurso(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela (Aumentei ligeiramente a altura para caber a nova secção)
        self.title("Sistema de Percursos - Lucas & Cláudia")
        self.geometry("650x820")
        self.configure(fg_color="#F4F1EA")  # Fundo bege clarinho
        self.resizable(False, False)

        # --- CABEÇALHO ---
        self.titulo = ctk.CTkLabel(
            self, 
            text="Configuração de Percurso Acessível", 
            font=("Helvetica", 18, "bold"), 
            text_color="#2A8569"
        )
        self.titulo.pack(pady=(20, 5))

        self.subtitulo = ctk.CTkLabel(
            self, 
            text="Defina o peso das suas preferências (1 = Pouco Importante, 10 = Muito Importante):", 
            font=("Helvetica", 11, "italic"),
            text_color="#555555"
        )
        self.subtitulo.pack(pady=(0, 15))

        # --- ÁREA COM SCROLL ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#F4F1EA", width=590, height=600)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # ==========================================
        # BLOCO 1: ACESSIBILIDADE FÍSICA
        # ==========================================
        self.lbl_seccao1 = ctk.CTkLabel(
            self.scroll_frame, 
            text="Acessibilidade Física", 
            font=("Helvetica", 13, "bold"), 
            text_color="#1F4E3D"
        )
        self.lbl_seccao1.pack(anchor="w", pady=(10, 10))

        self.slider_pavimento = self.criar_item_slider("Regularidade do pavimento:", 5)
        self.slider_inclinacao = self.criar_item_slider("Inclinação/Rampas:", 5)
        self.slider_passadeiras = self.criar_item_slider("Presença de Passadeiras:", 5)
        self.slider_passeios = self.criar_item_slider("Presença de Passeios:", 5)
        self.slider_escadas = self.criar_item_slider("Presença de Escadas:", 5)

        self.check_textura = ctk.CTkCheckBox(
            self.scroll_frame, 
            text="Necessito de Piso Podotátil (Textura Cego)",
            font=("Helvetica", 11),
            text_color="#2C3E50",
            border_color="#3AC098",
            fg_color="#3AC098"
        )
        self.check_textura.pack(anchor="w", pady=(15, 20))

        self.criar_separador()

        # ==========================================
        # BLOCO 2: CONFORTO E AMBIENTE
        # ==========================================
        self.lbl_seccao2 = ctk.CTkLabel(
            self.scroll_frame, 
            text="Conforto e Ambiente", 
            font=("Helvetica", 13, "bold"), 
            text_color="#1F4E3D"
        )
        self.lbl_seccao2.pack(anchor="w", pady=(10, 10))

        self.slider_sombra = self.criar_item_slider("Sombra:", 5)
        self.slider_ar = self.criar_item_slider("Qualidade do Ar:", 5)
        self.slider_polen = self.criar_item_slider("Presença de Pólen (Alergias):", 5)
        self.slider_ruido = self.criar_item_slider("Poluição Sonora:", 5)
        self.slider_visual = self.criar_item_slider("Poluição Visual:", 5)
        self.slider_iluminacao = self.criar_item_slider("Iluminação:", 5)

        self.criar_separador()

        # ==========================================
        # BLOCO 3: POPULAÇÃO (NOVO)
        # ==========================================
        self.lbl_seccao3 = ctk.CTkLabel(
            self.scroll_frame, 
            text="População e Movimento", 
            font=("Helvetica", 13, "bold"), 
            text_color="#1F4E3D"
        )
        self.lbl_seccao3.pack(anchor="w", pady=(10, 10))

        self.slider_transito = self.criar_item_slider("Evitar Trânsito de Veículos:", 5)
        self.slider_multidao = self.criar_item_slider("Evitar Grandes Multidões:", 5)


        # --- BOTÕES DE AÇÃO ---
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(fill="x", padx=30, pady=20)

        self.btn_calcular = ctk.CTkButton(
            self.frame_botoes, 
            text="Calcular Percurso", 
            font=("Helvetica", 12, "bold"),
            fg_color="#3AC098", 
            hover_color="#2A8569", 
            text_color="white",
            height=40,
            corner_radius=8,
            command=self.calcular_percurso
        )
        self.btn_calcular.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.btn_sair = ctk.CTkButton(
            self.frame_botoes, 
            text="Sair", 
            font=("Helvetica", 12, "bold"),
            fg_color="#C62828", 
            hover_color="#9E1F1F", 
            text_color="white",
            height=40,
            width=120,
            corner_radius=8,
            command=self.destroy
        )
        self.btn_sair.pack(side="right")

    # --- AUXILIAR: CRIAR SLIDER COM 1 E 10 ---
    def criar_item_slider(self, texto, valor_inicial):
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=5)
        
        row_frame.grid_columnconfigure(0, weight=0)
        row_frame.grid_columnconfigure(1, weight=0)
        row_frame.grid_columnconfigure(2, weight=1)
        row_frame.grid_columnconfigure(3, weight=0)

        lbl = ctk.CTkLabel(row_frame, text=texto, font=("Helvetica", 11), text_color="#2C3E50", width=190, anchor="w")
        lbl.grid(row=0, column=0, sticky="w", padx=(0, 5))

        lbl_min = ctk.CTkLabel(row_frame, text="1", font=("Helvetica", 10, "bold"), text_color="#7F8C8D", width=15)
        lbl_min.grid(row=0, column=1, sticky="e", padx=(5, 5))

        slider = ctk.CTkSlider(
            row_frame, 
            from_=1, 
            to=10, 
            number_of_steps=9, 
            fg_color="#D1D1D1", 
            progress_color="#3AC098", 
            button_color="#3AC098",
            button_hover_color="#2A8569",
            height=16
        )
        slider.set(valor_inicial)
        slider.grid(row=0, column=2, sticky="ew")

        lbl_max = ctk.CTkLabel(row_frame, text="10", font=("Helvetica", 10, "bold"), text_color="#7F8C8D", width=20)
        lbl_max.grid(row=0, column=3, sticky="w", padx=(5, 0))

        return slider

    def criar_separador(self):
        linha = ctk.CTkFrame(self.scroll_frame, height=2, fg_color="#E0DCD3")
        linha.pack(fill="x", pady=15)

    # --- AÇÃO DO BOTÃO CALCULAR ---
    def calcular_percurso(self):
        # Mapeamento exato de todos os sliders, incluindo os novos de população
        preferencias_usuario = {
            "peso_pavimento": int(self.slider_pavimento.get()),
            "peso_inclinacao": int(self.slider_inclinacao.get()),
            "peso_passadeiras": int(self.slider_passadeiras.get()),
            "peso_passeios": int(self.slider_passeios.get()),
            "peso_textura_cego": 10 if self.check_textura.get() else 0,
            "peso_escadas": 50 if int(self.slider_escadas.get()) >= 5 else 0,
            "peso_temperatura": int(self.slider_sombra.get()),
            "peso_sombra": int(self.slider_sombra.get()),  
            "peso_ar": int(self.slider_ar.get()),
            "peso_polen": int(self.slider_polen.get()),
            "peso_ruido": int(self.slider_ruido.get()),
            "peso_visual": int(self.slider_visual.get()),
            "peso_iluminacao": int(self.slider_iluminacao.get()),
            "peso_transito": int(self.slider_transito.get()), 
            "peso_multidao": int(self.slider_multidao.get())  
        }


        messagebox.showinfo(
            "Sucesso",
            f"Preferências guardadas com sucesso!\n\n"
            f"Pavimento: {preferencias_usuario['peso_pavimento']}\n"
            f"Trânsito: {preferencias_usuario['peso_transito']}\n"
            f"Multidão: {preferencias_usuario['peso_multidao']}\n\n"
            f"A calcular a rota ideal..."
        )

if __name__ == "__main__":
    app = MenuPercurso()
    app.mainloop()