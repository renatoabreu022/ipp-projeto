#-------@Cláudia e @Inês------ 03/05/2026

import customtkinter as ctk
from tkinter import messagebox

# Configurações globais de design
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# --- BASE DE DADOS DE LOCAIS ---
DADOS_CIDADES = {
    "Porto": ["FEUP", "Farmácia Barreiros", "Jardim do Palácio de Cristal", "Estação de São Bento", "NorteShopping", "Centro Hospitalar Universitário de São João", "Bebedouro Jardim do Morro", "Posto de Primeiros Socorros Aliados", "Ecoponto Asprela", "WC Público Cordoaria", "Zona de Descanso Aliados"],
    "Braga": ["Bom Jesus do Monte", "Avenida da Liberdade", "Hospital de Braga", "Universidade do Minho - Gualtar", "Braga Parque", "Bebedouro Arcada", "Ciclovia do Rio Este", "Ecoponto Gualtar", "WC Público Praça do Município"],
    "Fafe": ["Praça Mártires de Ferreira do Amaral", "Hospital da Misericórdia", "Parque da Cidade", "Pavilhão Multiusos", "Terminal Rodoviário", "Bebedouro Parque da Cidade", "Parque Infantil do Centro", "Ecoponto Multiusos"],
    "Marco de Canaveses": ["Igreja de Santa Maria (Siza Vieira)", "Hospital Santa Isabel", "Estação Ferroviária", "Jardim Municipal", "Marco Fórum", "Bebedouro Jardim Municipal", "Posto de Informação Turística", "Ecoponto Marco Fórum"],
    "Guimarães": ["Castelo de Guimarães", "Hospital da Senhora da Oliveira", "Universidade do Minho (Azurém)", "GuimarãeShopping", "Largo do Toural", "Bebedouro Largo da Oliveira", "Parque da Cidade Guimarães", "WC Público Toural"],
    "Vila Nova de Gaia": ["El Corte Inglés", "Hospital Eduardo Santos Silva", "Cais de Gaia", "GaiaShopping", "Jardim do Morro", "Bebedouro Cais de Gaia", "Ciclovia da Orla Marítima", "Ecoponto Jardim do Morro"],
    "Famalicão": ["Hospital de Famalicão", "Parque da Devesa", "Estação de Famalicão", "Universidade Lusíada", "Praça D. Maria II", "Bebedouro Parque da Devesa", "Posto de Primeiros Socorros", "WC Público Praça D. Maria II"],
    "Barcelos": ["IPCA", "Campo da Feira", "Hospital Santa Maria Maior", "Templo do Senhor da Cruz", "Estação de Barcelos", "Bebedouro IPCA", "Parque Infantil de Barcelos", "Ecoponto Estação"],
    "Póvoa de Varzim": ["Casino da Póvoa", "Hospital da Luz Póvoa de Varzim", "Passeio Alegre", "Biblioteca Municipal Rocha Peixoto", "Estação de Metro da Póvoa", "Bebedouro Passeio Alegre", "Posto de Socorros da Praia", "WC Público Biblioteca"],
    "Coimbra": ["Universidade de Coimbra - Polo I", "Hospitais da Universidade de Coimbra", "Portugal dos Pequenitos", "Estação Coimbra-B", "Forum Coimbra", "Bebedouro Praça da República", "Parque Verde do Mondego", "WC Público Baixa"],
    "Figueira da Foz": ["Casino Figueira", "Hospital Distrital da Figueira da Foz", "Mercado Municipal", "Torre do Relógio", "Parque das Abadias", "Bebedouro Marginal", "Ciclovia da Marginal", "Ecoponto Mercado"],
    "Covilhã": ["UBI", "Centro Hospitalar Cova da Beira", "Praça do Município", "Serra Shopping", "Ponte da Carpinteira", "Bebedouro UBI", "Jardim Público da Covilhã", "WC Público Praça"],
    "Caldas da Rainha": ["Praça da Fruta", "Hospital Termal", "Parque D. Carlos I", "Centro Comercial La Vie", "ESAD.CR", "Bebedouro Parque D. Carlos I", "Posto de Informação"],
    "Tomar": ["Convento de Cristo", "Praça da República", "Hospital de Tomar", "Mata dos Sete Montes", "Politécnico de Tomar", "Bebedouro Mata", "Parque do Mouchão", "WC Público Centro"],
    "Viseu": ["Sé de Viseu", "Palácio do Gelo", "Hospital de São Teotónio", "Parque do Fontelo", "Rossio", "Bebedouro Parque do Fontelo", "Ecoponto Sé", "Posto de Primeiros Socorros"],
    "Aveiro": ["Fórum Aveiro", "Universidade de Aveiro", "Estação de Aveiro", "Hospital Infante D. Pedro", "Salinas de Aveiro", "Bebedouro Salinas", "Parque Infante D. Pedro", "WC Público Estação"],
    "Lisboa": ["Hospital de Santa Maria", "Estação do Oriente", "Castelo de São Jorge", "Terreiro do Paço", "Centro Comercial Colombo", "Bebedouro Parque das Nações", "Jardim da Estrela", "WC Público Rossio", "Posto Polícia Baixa"],
    "Évora": ["Sé de Évora", "Templo Romano", "Colégio do Espírito Santo", "Hospital do Espírito Santo", "Praça do Giraldo", "Bebedouro Templo Romano", "Jardim Público de Évora", "Ecoponto Centro"],
    "Beja": ["Castelo de Beja", "Hospital José Joaquim Fernandes", "Politécnico de Beja", "Parque de Feiras", "Museu Regional", "Bebedouro Castelo", "Parque de Merendas", "WC Público Parque de Feiras"],
    "Portimão": ["Portimão Arena", "Hospital Particular", "Praia da Rocha", "Aqua Portimão", "Museu de Portimão", "Bebedouro Praia da Rocha", "Posto de Socorros Marítimo", "WC Público Centro"],
    "Lagos": ["Marina de Lagos", "Hospital de Lagos", "Mercado Municipal", "Ponta da Piedade", "Praça Infante Dom Henrique", "Bebedouro Marina", "Centro de Ciência Viva", "WC Público Centro"],
    "Faro": ["UAlg - Penha", "Hospital de Faro", "Fórum Algarve", "Doca de Faro", "Arco da Vila", "Bebedouro Doca", "Parque Ribeirinho", "Ecoponto Fórum"]
}

BD_UTILIZADORES = {}

class AppAcessibilidade(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Percursos - Lucas & Cláudia")
        self.geometry("650x850")
        self.configure(fg_color="#F4F1EA")
        self.utilizador_atual = None
        self.mostrar_login()

    def limpar_janela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpar_janela()
        self.geometry("450x500")
        ctk.CTkLabel(self, text="Acesso ao Sistema", font=("Helvetica", 24, "bold"), text_color="#2A8569").pack(pady=40)
        self.ent_user = ctk.CTkEntry(self, placeholder_text="Utilizador", width=250)
        self.ent_user.pack(pady=10)
        self.ent_pass = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.ent_pass.pack(pady=10)
        ctk.CTkButton(self, text="Entrar", command=self.fazer_login, width=250).pack(pady=20)
        ctk.CTkButton(self, text="Criar Conta", command=self.mostrar_registo, width=250, fg_color="transparent", text_color="#2A8569", border_width=2, border_color="#3AC098").pack()

    def fazer_login(self):
        user, pw = self.ent_user.get(), self.ent_pass.get()
        if user in BD_UTILIZADORES and BD_UTILIZADORES[user]["pass"] == pw:
            self.utilizador_atual = user
            self.mostrar_menu_principal()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas.")

    def mostrar_registo(self):
        self.limpar_janela()
        self.geometry("450x550")
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
        if not user or not p1: messagebox.showwarning("Aviso", "Preencha tudo."); return
        if p1 != p2: messagebox.showerror("Erro", "Passwords não coincidem!"); return
        if user in BD_UTILIZADORES: messagebox.showerror("Erro", "Utilizador já existe."); return
        self.utilizador_atual, self.temp_pw = user, p1
        self.mostrar_preferencias(primeira_vez=True)

    def mostrar_preferencias(self, primeira_vez=False):
        self.limpar_janela()
        self.geometry("650x850")
        ctk.CTkLabel(self, text="Parâmetros de Acessibilidade", font=("Helvetica", 18, "bold"), text_color="#2A8569").pack(pady=10)
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#F4F1EA", width=600, height=600)
        self.scroll.pack(padx=20, pady=10, fill="both", expand=True)

        # BLOCO 1: FÍSICA
        self.criar_label_seccao(self.scroll, "Acessibilidade Física")
        self.s_pav = self.criar_item_slider(self.scroll, "Regularidade pavimento:")
        self.s_inc = self.criar_item_slider(self.scroll, "Inclinação/Rampas:")
        self.s_pss = self.criar_item_slider(self.scroll, "Presença de Passeios:")
        self.s_esc = self.criar_item_slider(self.scroll, "Presença de Escadas:")
        self.c_pod = ctk.CTkCheckBox(self.scroll, text="Piso Podotátil (Textura Cego)", border_color="#3AC098", fg_color="#3AC098")
        self.c_pod.pack(anchor="w", pady=10)

        # BLOCO 2: AMBIENTE
        self.criar_label_seccao(self.scroll, "Conforto e Ambiente")
        self.s_som = self.criar_item_slider(self.scroll, "Sombra:")
        self.s_ar  = self.criar_item_slider(self.scroll, "Qualidade do Ar:")
        self.s_pol = self.criar_item_slider(self.scroll, "Presença de Pólen:")
        self.s_rui = self.criar_item_slider(self.scroll, "Poluição Sonora:")
        self.s_vis = self.criar_item_slider(self.scroll, "Poluição Visual:")
        self.s_ilu = self.criar_item_slider(self.scroll, "Iluminação:")

        # BLOCO 3: MOVIMENTO
        self.criar_label_seccao(self.scroll, "População e Movimento")
        self.s_tra = self.criar_item_slider(self.scroll, "Evitar Trânsito:")
        self.s_mul = self.criar_item_slider(self.scroll, "Evitar Multidões:")

        if not primeira_vez:
            p = BD_UTILIZADORES[self.utilizador_atual]["prefs"]
            self.s_pav.set(p["pav"]); self.s_inc.set(p["inc"]); self.s_pss.set(p["pss"]); self.s_esc.set(p["esc"])
            self.s_som.set(p["som"]); self.s_ar.set(p["ar"]); self.s_pol.set(p["pol"]); self.s_rui.set(p["rui"])
            self.s_vis.set(p["vis"]); self.s_ilu.set(p["ilu"]); self.s_tra.set(p["tra"]); self.s_mul.set(p["mul"])
            if p["pod"]: self.c_pod.select()

        ctk.CTkButton(self, text="Guardar Perfil", command=lambda: self.guardar_dados(primeira_vez)).pack(pady=20)

    def criar_label_seccao(self, master, texto):
        ctk.CTkLabel(master, text=texto, font=("Helvetica", 13, "bold"), text_color="#1F4E3D").pack(anchor="w", pady=(10, 5))

    def criar_item_slider(self, master, texto):
        f = ctk.CTkFrame(master, fg_color="transparent")
        f.pack(fill="x", pady=2)
        ctk.CTkLabel(f, text=texto, width=190, anchor="w", font=("Helvetica", 11)).grid(row=0, column=0)
        ctk.CTkLabel(f, text="1", font=("Helvetica", 9)).grid(row=0, column=1, padx=2)
        s = ctk.CTkSlider(f, from_=1, to=10, number_of_steps=9)
        s.set(5); s.grid(row=0, column=2, sticky="ew")
        ctk.CTkLabel(f, text="10", font=("Helvetica", 9)).grid(row=0, column=3, padx=2)
        f.grid_columnconfigure(2, weight=1)
        return s

    def guardar_dados(self, primeira_vez):
        prefs = {
            "pav": self.s_pav.get(), "inc": self.s_inc.get(), "pss": self.s_pss.get(), "esc": self.s_esc.get(),
            "som": self.s_som.get(), "ar": self.s_ar.get(), "pol": self.s_pol.get(), "rui": self.s_rui.get(),
            "vis": self.s_vis.get(), "ilu": self.s_ilu.get(), "tra": self.s_tra.get(), "mul": self.s_mul.get(),
            "pod": self.c_pod.get()
        }
        if primeira_vez: BD_UTILIZADORES[self.utilizador_atual] = {"pass": self.temp_pw, "prefs": prefs}
        else: BD_UTILIZADORES[self.utilizador_atual]["prefs"] = prefs
        self.mostrar_menu_principal()

    def mostrar_menu_principal(self):
        self.limpar_janela()
        self.geometry("600x700")
        ctk.CTkLabel(self, text=f"Olá, {self.utilizador_atual}", font=("Helvetica", 20, "bold"), text_color="#2A8569").pack(pady=20)
        
        f_calc = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        f_calc.pack(padx=30, pady=10, fill="both", expand=True)

        ctk.CTkLabel(f_calc, text="Cidade:").pack(pady=(10, 0))
        self.cb_cidade = ctk.CTkComboBox(f_calc, values=list(DADOS_CIDADES.keys()), command=self.atualizar_locais, width=300)
        self.cb_cidade.pack(pady=5)

        ctk.CTkLabel(f_calc, text="Origem:").pack()
        self.cb_origem = ctk.CTkComboBox(f_calc, values=[], width=350)
        self.cb_origem.pack(pady=5)

        ctk.CTkLabel(f_calc, text="Destino:").pack()
        self.cb_destino = ctk.CTkComboBox(f_calc, values=[], width=350)
        self.cb_destino.pack(pady=5)

        ctk.CTkButton(f_calc, text="CALCULAR ROTA", command=self.calcular, height=50).pack(pady=20)
        ctk.CTkButton(self, text="Editar Parâmetros", command=lambda: self.mostrar_preferencias(False), fg_color="#5D6D7E").pack(pady=5)
        ctk.CTkButton(self, text="Sair", command=self.mostrar_login, fg_color="#C62828").pack(pady=10)

    def atualizar_locais(self, cidade_escolhida):
        locais = DADOS_CIDADES[cidade_escolhida]
        self.cb_origem.configure(values=locais)
        self.cb_destino.configure(values=locais)
        self.cb_origem.set(locais[0])
        self.cb_destino.set(locais[1] if len(locais) > 1 else locais[0])

    def calcular(self):
        msg = f"Rota em {self.cb_cidade.get()}\nDe: {self.cb_origem.get()}\nPara: {self.cb_destino.get()}\n\nA calcular com base no seu perfil..."
        messagebox.showinfo("Cálculo", msg)

if __name__ == "__main__":
    app = AppAcessibilidade()
    app.mainloop()