#-------@Cláudia e @Inês------ 03/05/2026


import FreeSimpleGUI as sg  


#------ CORES

tema = "#000000"


#------------


def criar_menu():
    sg.theme("LightGreen")

    # --- LAYOUT DA INTERFACE ---
    layout = [
        # Cabeçalho        
        [sg.Text("Configuração de Percurso Acessível", font=("Helvetica", 16, "bold"), text_color="#3AC098")],
        [sg.Text("Defina o peso das suas preferências (1 = Pouco Importante, 10 = Muito Importante):", font=("Helvetica", 10, "italic"))],
        [sg.HSeparator(pad=(0, 15))],

        # Bloco 1: Acessibilidade Física
        [sg.Text("Acessibilidade Física", font=("Helvetica", 12, "bold"))],
        [
            sg.Text("Regularidade do pavimento:", size=(22, 1)), 
            sg.Slider(range=(1, 10), default_value=5, orientation="h", size=(20, 15), key="-PESO_PAVIMENTO-")
        ],
        [
            sg.Text("Inclinação/Rampas:", size=(22, 1)), 
            sg.Slider(range=(1, 10), default_value=5, orientation="h", size=(20, 15), key="-PESO_INCLINACAO-")
        ],
        [
            sg.Text("Presença de Passadeiras:", size=(22, 1)), 
            sg.Slider(range=(1, 10), default_value=5, orientation="h", size=(20, 15), key="-PESO_PASSADEIRAS-")
        ],
        [
            sg.Text("Presença de Passeios:", size=(22, 1)), 
            sg.Slider(range=(1, 10), default_value=5, orientation="h", size=(20, 15), key="-PESO_PASSEIOS-")
        ],
        [
            sg.Text("Presença de Escadas:", size=(22, 1)), 
            sg.Slider(range=(1, 10), default_value=5, orientation="h", size=(20, 15), key="-PESO_ESCADAS-")
        ],
        [
            sg.Checkbox("Necessito de Piso Podotátil (Textura Cego)", default=False, key="-USA_TEXTURA-")],

        
        [sg.HSeparator(pad=(0, 15))],

        # Bloco 2: Conforto e Ambiente
        [sg.Text("Conforto e Ambiente", font=("Helvetica", 12, "bold"))],
        [
            sg.Text("Sombra:", size=(22, 1)), 
            sg.Slider(range=(1, 10), default_value=5, orientation="h", size=(20, 15), key="-PESO_AMBIENTE-")
        ],
        [
            sg.Text("Qualidade do Ar:", size=(22, 1)), 
            sg.Slider(range=(1, 10), default_value=5, orientation="h", size=(20, 15), key="-PESO_AR-")
        ],
        [
            sg.Text("Presença de Pólen (Alergias):", size=(22, 1)), 
            sg.Slider(range=(1, 10), default_value=5, orientation="h", size=(20, 15), key="-PESO_POLEN-")
        ],
        [
            sg.Text("Poluição Sonora:", size=(22, 1)), 
            sg.Slider(range=(1, 10), default_value=5, orientation="h", size=(20, 15), key="-PESO_RUIDO-")
        ],
        [
            sg.Text("Poluição Visual:", size=(22, 1)), 
            sg.Slider(range=(1, 10), default_value=5, orientation="h", size=(20, 15), key="-PESO_VISUAL-")
        ],
        [
            sg.Text("Iluminação", size=(22, 1)), 
            sg.Slider(range=(1, 10), default_value=5, orientation="h", size=(20, 15), key="-PESO_ILUMINACAO-")
        ],

        [sg.HSeparator(pad=(0, 15))],

        # Botões de Ação
        [
            sg.Button("Calcular Percurso", size=(18, 1), button_color=("white", "#3AC098"), font=("Helvetica", 11, "bold"), key="-CALCULAR-"),
            sg.Button("Sair", size=(10, 1), button_color=("white", "#C62828"), key="-SAIR-")
        ]
    ]


    window = sg.Window("Sistema de Percursos", layout, finalize=True)
    return window

def main():
    window = criar_menu()

    # --- CICLO DE EVENTOS ---
    while True:
        event, values = window.read()

        
        if event == sg.WIN_CLOSED or event == "-SAIR-":
            break

        
        if event == "-CALCULAR-":
            
            preferencias_usuario = {
                "peso_pavimento": values["-PESO_PAVIMENTO-"],
                "peso_inclinacao": values["-PESO_INCLINACAO-"],
                "peso_passadeiras": values["-PESO_PASSADEIRAS-"],
                "peso_passeios": values["-PESO_PASSEIOS-"],
                "peso_textura_cego": 10 if values["-USA_TEXTURA-"] else 0,
                "peso_escadas": 50 if values["-PESO_ESCADAS-"] else 0,
                "peso_temperatura": values["-PESO_AMBIENTE-"],
                "peso_sombra": values["-PESO_AMBIENTE-"],  
                "peso_ar": values["-PESO_AR-"],
                "peso_polen": values["-PESO_POLEN-"],
                "peso_ruido": values["-PESO_RUIDO-"],
                "peso_visual": values["-PESO_VISUAL-"]  
            }

            
            sg.popup_success(
                f"Preferências guardadas com sucesso!\n\n"
                f"Pavimento: {preferencias_usuario['peso_pavimento']}\n"
                f"Escadas: {preferencias_usuario['peso_escadas']}\n"
                f"A calcular a rota ideal...", 
                title="Sucesso"
            )
            


    window.close()

if __name__ == "__main__":
    main()





