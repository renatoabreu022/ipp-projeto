import customtkinter as ctk
from tkinter import messagebox


import random

class GestorBicicletas:
    def __init__(self):
        self.estacoes = {}
    
    def gerar_estacoes_para_cidade(self, locais_da_cidade):
        self.estacoes = {}
        k_vagas = random.choice([3, 4])
        num_estacoes = min(len(locais_da_cidade), k_vagas)
        locais_sorteados = random.sample(locais_da_cidade, k=num_estacoes)
        
        for local in locais_sorteados:
            self.estacoes[local] = {
                "total_vagas": 5,
                "disponiveis": random.randint(1, 5),
                "estado": "Operacional"
            }

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class AppBicicletas(ctk.CTk):
    def __init__(self, gestor, db_cidades):
        super().__init__()
        
        self.gestor = gestor
        self.db_cidades = db_cidades
    
        self.title("Sistema de Mobilidade")
        self.geometry("0x0+0+0")
        self.withdraw() 
        
        self.cor_verde_texto = "#1F634E"
        self.fonte_titulo = ("Helvetica", 24, "bold")
        self.fonte_p = ("Helvetica", 15)
        
        self.abrir_popup_selecao()

    def abrir_popup_selecao(self):
        self.pop_cidade = ctk.CTkToplevel(self)
        self.pop_cidade.title("Rede de Mobilidade")
        self.pop_cidade.geometry("450x300")
        self.pop_cidade.configure(fg_color="#F4F1EA")
        self.pop_cidade.resizable(False, False)
        
        self.pop_cidade.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        
        ctk.CTkLabel(self.pop_cidade, text="BICICLETAS PÚBLICAS", font=("Helvetica", 14), text_color="#1F634E").pack(pady=(50, 5))
        ctk.CTkLabel(self.pop_cidade, text="Selecione a sua cidade", font=self.fonte_titulo, text_color="#333333").pack(pady=10)

        cidades_ordenadas = sorted(list(self.db_cidades.keys()))
        self.combo_cidades = ctk.CTkComboBox(self.pop_cidade, values=cidades_ordenadas, width=250, font=self.fonte_p, state="readonly")
        self.combo_cidades.pack(pady=25)
        self.combo_cidades.set("Escolha a cidade...")

        ctk.CTkButton(self.pop_cidade, text="CONSULTAR ESTAÇÕES", font=("Helvetica", 12, "bold"), fg_color="#2A8569", hover_color="#1F634E", height=45, width=250, command=self.ir_para_listagem).pack(pady=15)

    def ir_para_listagem(self):
        cidade_escolhida = self.combo_cidades.get()
        if cidade_escolhida == "Escolha a cidade...": 
            return

    
        self.pop_cidade.withdraw()
        self.abrir_popup_listagem(cidade_escolhida)

    def abrir_popup_listagem(self, cidade):
        self.pop_listagem = ctk.CTkToplevel(self)
        self.pop_listagem.title(f"Estações Ativas - {cidade}")
        self.pop_listagem.geometry("600x400") 
        self.pop_listagem.configure(fg_color="#F4F1EA")

        self.pop_listagem.protocol("WM_DELETE_WINDOW", self.voltar_atras)

        ctk.CTkLabel(self.pop_listagem, text=f"Estações disponíveis: {cidade}", font=("Helvetica", 16, "bold"), text_color=self.cor_verde_texto).pack(pady=15)

        self.gestor.gerar_estacoes_para_cidade(self.db_cidades[cidade])
        
    
        self.scroll_lista = ctk.CTkScrollableFrame(self.pop_listagem, fg_color="white", corner_radius=15, width=520, height=150)
        self.scroll_lista.pack(padx=30, pady=10, fill="both", expand=True)


        header_frame = ctk.CTkFrame(self.scroll_lista, fg_color="transparent")
        header_frame.pack(fill="x", pady=(5, 10))
        ctk.CTkLabel(header_frame, text="ESTAÇÃO", font=("Helvetica", 11, "bold"), text_color="#1F4E3D").pack(side="left", padx=15)
        ctk.CTkLabel(header_frame, text="DISPONÍVEL", font=("Helvetica", 11, "bold"), text_color="#1F4E3D").pack(side="right", padx=15)


        for local, info in self.gestor.estacoes.items():
            row_frame = ctk.CTkFrame(self.scroll_lista, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(row_frame, text=f"📍 {local}", font=self.fonte_p, text_color="#333333", anchor="w").pack(side="left", padx=15)
            ctk.CTkLabel(row_frame, text=f"🚲 {info['disponiveis']} bicicletas", font=("Helvetica", 14, "bold"), text_color=self.cor_verde_texto, anchor="e").pack(side="right", padx=15)


        btn_frame = ctk.CTkFrame(self.pop_listagem, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="VOLTAR", font=("Helvetica", 14, "bold"), fg_color="#2A8569", hover_color="#1F4E3D", height=40, width=150, command=self.voltar_atras).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="SAIR", font=("Helvetica", 14, "bold"), fg_color="#C62828", hover_color="#A12121", height=40, width=100, command=self.fechar_programa).pack(side="left", padx=10)

    def voltar_atras(self):
        if hasattr(self, 'pop_listagem'):
            self.pop_listagem.destroy()
        self.pop_cidade.deiconify() 

    def fechar_programa(self):
        self.quit()
        self.destroy()


# BLOCO PRINCIPAL (MAIN)
if __name__ == "__main__":
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

    root = AppBicicletas(GestorBicicletas(), DADOS_CIDADES)
    root.mainloop()