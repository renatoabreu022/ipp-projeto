# ----Dia 30/03/2026 @Renato
# este ficheiro vai servir como o Controller no MVC
# ele estará num ciclo infinito à espera de inputs e chama quem os deve processar

# ----Dia 31/03/2026 @Renato @Claudia

# ----Dia 02/04/2026 @Renato

#---- Dia 18/04/2026 @Cláudia

# @Renato --- PODEMOS USAR ARVORES BINARIAS PARA CRIAR O PERFIL DO UTILIZADOR, TIPO:
# USA CADEIRA DE RODAS? - ESQUERDA(SIM); DIREITA(NÃO); DEPOIS SE SIM AS PERGUNTAS SEGUINTES SERÃO MAIS ADEQUADAS PARA CADEIRA DE RODAS
# SE NÃO, NAS PERGUNTAS SEGUINTES ASSUME-SE QUE A PESSOA CONSEGUE ANDAR POR QUALQUER PAVIMENTO, MAS TEM PREFERÊNCIAS E QUESTIONA-SE SOBRE ESSAS PREFERÊNCIAS

from models.grafo import Mapa
from models.user import Sistema, Utilizador, Preferencias
import json
from datetime import datetime
from models.bicicletas import GestorBicicletas
import city
import os
from interface_bicicletas import AppBicicletas

#------Meti aqui (@Lucas) porque esta seleção deve ser feita durante a execução da app..#
def hora(values):
    if values["-USAR_HORA_ATUAL-"]:  #A ideia é meter 2 botões: Hora atual ou marcar agendameento de previsão de condições
        hora_calculo=datetime.now().hour  #Seleciona atual
        print(f"Hora atual selecionada: {hora_calculo}h")
    else:
        hora_calculo = int(values["-HORA_SIMULAR-"]) # Transforma o input numa hora que dá para trabalhar
        print(f"Hora selecionada para simulação: {hora_calculo}h")
    return hora_calculo

#--------------------#

def help():
    print("\n--- COMANDOS DISPONÍVEIS --------------------------------------------------------------------------")
    print("signin <nome>                                        -> Regista novo utilizador")
    print("login <nome> <password>                              -> Login")
    print("alterar_password <password_atual> <password_nova>    -> Alterar a password")
    print("preferencias                                         -> Altera os parâmetros de preferências")
    print("simular                                              -> Calcula as melhores rotas entre dois pontos")
    print("gravar <ficheiro>                                    -> Salva utilizadores")
    print("ler <ficheiro>                                       -> Carrega utilizadores")
    print("bicicletas                                           -> Mostra as bicicletas disponiveis")
    print("gravar_mapa <ficheiro>                               -> Guarda o mapa atual")
    print("carregar_mapa <ficheiro>                             -> Carrega um mapa guardado")
    print("ins_cidade                                           -> Cria uma cidade nova")
    print("ins_local                                            -> Adiciona um local a uma cidade")
    print("ins_percurso                                         -> Adiciona um percurso entre dois pontos")
    print("ver                                                  -> Mostra a informação associada a um percurso")
    print("sair                                                 -> Encerra a aplicação")
    print("----------------------------------------------------------------------------------------------------")

# --- LOOP PRINCIPAL ---
def carregar_cidades_disponiveis():
    cidades = {}
    pasta = "city"
    prefixo = "grafo_"
    
    for ficheiro in os.listdir(pasta):
        if ficheiro.startswith(prefixo) and ficheiro.endswith(".json"):
            # extrai o nome: "grafo_vila_nova_de_gaia.json" -> "Vila Nova De Gaia"
            nome_fich = ficheiro[len(prefixo):-len(".json")]  # remove prefixo e extensão
            nome_cidade = nome_fich.replace("_", " ").title()  # "vila nova de gaia" -> "Vila Nova De Gaia"
            cidades[nome_cidade] = os.path.join(pasta, ficheiro)
    
    return cidades

def main():
    sistema = Sistema()  # cria a base de dados de utilizadores
    mapa = Mapa()
    user_login = None
    arquivo_db = "utilizadores"
    
    #Tenta carregar os utilizadores logo ao iniciar o programa
    sistema.load_users(arquivo_db)
    gestor_bicicletas = GestorBicicletas()
    print("Bem-vind@! Digite 'help' para comandos.")
    caminho_anterior = None
    cidade_atual = None
    while True:
        entrada = input("> ").strip().split()
        if not entrada:
            continue

        comando = entrada[0].lower()
        args = entrada[1:]

        if comando == "sair":
            print("A encerrar...")
            break

        elif comando == "help":
            help()

        elif comando == "signin":
            if len(args) != 1:
                print("ERRO: Uso indevido do comando.\nDeverá seguir este modelo: signin <nome>.")

            else:
                nome = args[0]
                if sistema.cria_username(nome):
                    #criamos um utilizador com a password padrão e preferências padrão (tudo a 5)
                    novo_user = Utilizador(nome, "0000", Preferencias())
                    sistema.add_user(novo_user)
                    
                    #guardamos logo na base de dados
                    sistema.save_users(arquivo_db)
                    
                    print(f"Utilizador {nome} criado com sucesso!")
                    print("Note que lhe foi atribuída a password 0000. Por favor, modifique-a assim que puder.")
        
        elif comando == 'login':
            if len(args) != 2:
                print("ERRO: Uso indevido do comando.\nDeverá seguir este modelo: login <nome> <password>.")
            
            else:
                nome, password = args
                if sistema.login(nome,password):
                    for u in sistema._users:
                        if u.u_username == nome:
                            user_login = u
                            break
                    print(f"Login realizado com sucesso. Bem-vind@, {nome}!")
        
        elif comando == "alterar_password":
            if user_login is None:
                print(print("ERRO: Precisa de fazer login primeiro para alterar as suas preferências."))
            elif len(args) != 2:
                print("ERRO: Uso indevido do comando.\nDeverá seguir este modelo: alterar_pass <password atual> <password nova>")
            else:
                password_atual, nova_password = args
                
                if user_login.verifica_credenciais(user_login.u_username, password_atual):
                    if nova_password.strip() != "":
                        user_login.alterar_password(nova_password)
                        sistema.save_users(arquivo_db)
                        print("[Sucesso] Password alterada com sucesso!")
                    else:
                        print("ERRO: A nova password não pode ser vazia.")
                else:
                    print("ERRO: Password atual incorreta.")
        
        
        elif comando == "preferencias":
            if user_login is None:
                print("ERRO: Precisa de fazer login primeiro para alterar as suas preferências.")
            else:
                #chama o questionário que já criámos no user.py da classe Preferências
                user_login.u_preferencias.forms_pref()
                
                sistema.save_users(arquivo_db)
                print("\n[Sucesso] As suas preferências foram atualizadas na base de dados!")
        
        elif comando == 'gravar':
            nome_arquivo = args[0] if args else arquivo_db
            sistema.save_users(nome_arquivo)
            print(f"Utilizadores gravados com sucesso em '{nome_arquivo}.json'.")

        elif comando == 'ler':
            if not args:
                print("ERRO: Uso indevido do comando.\nDeverá seguir este modelo: ler <arquivo.json>.")
            else:
                sistema.load_users(args[0])
        
        elif comando == 'gravar_mapa':
            if not args:
                print('ERRO: Uso indevido do comando.\nDeverá seguir este modelo: gravar_mapa <ficheiro>.')
            else:
                mapa.save_mapa(f"city/{args[0]}")
        
        elif comando == 'carregar_mapa':
            if not args:
                print('ERRO: Uso indevido do comando.\nDeverá seguir este modelo: carregar_mapa <ficheiro>.')
            else:
                caminho = f"city/{args[0]}"
                mapa.load_mapa(caminho)
                caminho_mapa_atual = caminho  # <-- guarda o caminho completo

                # Deriva o nome da cidade a partir do ficheiro
                # ex: "grafo_setúbal.json" -> "Setúbal"
                nome_fich = args[0]
                if nome_fich.endswith(".json"):
                    nome_fich = nome_fich[:-5]
                if nome_fich.startswith("grafo_"):
                    nome_fich = nome_fich[len("grafo_"):]
                cidade_atual = nome_fich.replace("_", " ").title()
                
        #novo comando simular com a nova função que está nos grafos
        elif comando == "simular":
            if user_login is None:
                print("ERRO: O processo de login não foi efetuado.")
                continue
            #mapeamento de ficheiros
            # Adicionei o prefixo da pasta 'city_graphs/' antes de cada nome
            cidades_disponiveis = carregar_cidades_disponiveis()

            print(f"\nCidades disponíveis:{list(cidades_disponiveis.keys())}")            
            selecao = input("Escolha a cidade para a simulação: ").strip()

            if selecao not in cidades_disponiveis:
                print(f"ERRO: A cidade {selecao} não está carregada no sistema.")
                continue
            
            try: #carregar o mapa da Cidade
                mapa.load_mapa(cidades_disponiveis[selecao])
                print(f"\n-- MAPA DE {selecao.upper()} CARREGADO ---")
                print(f"Locais detetados: {','.join(list(mapa.adjacencias.keys()))}")

                #DEFINIR A HORA
                print("\nEscolha do horário para o percurso")
                print("[1] Horário Atual ")
                print("[2] Agendar percurso")
                op_h=input("Opção: ")

                if op_h == "2":
                    h_calculo = int(input("Insira a hora pretendida:"))
                else:
                    h_calculo = datetime.now().hour

                print(f"Calculando a melhora rota para as {h_calculo}h...")

                #DEFINIR ROTA
                origem = input("\nDigite o ponto de Partida:").strip()
                destino = input("\nDigite o ponto de Chegada:").strip()
                
                if origem not in mapa.adjacencias or destino not in mapa.adjacencias:
                    print("ERRO: Um ou ambos os locais não existem nesta cidade.")
                    continue
                
                
                
                #EXECUTAR A SIMULAÇÃO
                resultado = mapa.pesquisa_perc(origem, destino, user_login.u_preferencias, hora=h_calculo, k=5)

                if resultado:
                    print("\n" + "="*30)
                    print("MELHORES ROTAS ENCONTRADAS")
                    print("(Nota: Quanto menor o score, mais confortável é o percurso)")
                    for i in range (len(resultado)):
                        score_total, caminhos = resultado[i]
                        print("-"*80)
                        print(f" {i+1}º caminho sugerido: {' -> '.join(caminhos)}")
                        print(f"Penalização total (Score): {round(score_total, 0)}")
                        print("-" * 80)

                #___________Spider_Chart_____________________#
                    while True: # Ciclo para permitir ver vários gráficos
                        print("\n" + "-"*30)
                        print("[ OPÇÕES DE VISUALIZAÇÃO ]")
                        print("Introduza o nº do caminho para ver o gráfico (ou 'N' para voltar ao menu)")
                        opcao = input("Escolha: ").strip().lower()

                        if opcao == 'n':
                            break # Sai do ciclo e volta ao menu principal

                        if opcao.isdigit():
                            indice = int(opcao) - 1
                            if 0 <= indice < len(resultado):
                                from engine.visualizador_gráficos import AnalisadorVisual
                                
                                _, caminho_selecionado = resultado[indice]
                                
                                print(f"\nA exibir comparação visual...")
                                # Chamamos a nova função passando o atual E o anterior
                                AnalisadorVisual.radar (caminho_selecionado, caminho_anterior, mapa,hora=h_calculo)
                                
                                # Após fechar o gráfico, o atual passa a ser o anterior para a próxima vez
                                caminho_anterior = caminho_selecionado
                            else:
                                print("Número de caminho inválido.")
                        else:
                            print("Opção inválida. Digite o número ou 'N'.")            
            except Exception as e:
                print(f"ERRO durante a simulação: {e}")
        
        
        elif comando == "bicicletas":
            if user_login is None:
                print("ERRO: Precisa de fazer login primeiro para alterar as suas preferências.")
                continue
            try:
                with open("locais.json", "r", encoding="utf-8") as f:
                    db_cidades = json.load(f)
            except FileNotFoundError:
                db_cidades = {}
            
            cidades_disponiveis = carregar_cidades_disponiveis()
            
            
            print(f"Cidades disponíveis: {', '.join(db_cidades.keys())}")
            cidade_escolhida = input("Em que cidade se encontra? ").strip()
            
            if cidade_escolhida in db_cidades and cidade_escolhida in cidades_disponiveis:
                locais = db_cidades[cidade_escolhida]
                mapa.load_mapa(cidades_disponiveis[cidade_escolhida])
                gestor_bicicletas.gerar_estacoes_para_cidade(locais)
                estacoes_bicicletas = list(gestor_bicicletas.estacoes.keys())
                
                
                print(f"Estações de Bicicletas em {cidade_escolhida}")
                for local, info in gestor_bicicletas.estacoes.items():
                    print(f"{local}: {info['disponiveis']} bicicletas disponíveis")
                
                print("""Se pretende que calculemos o melhor percurso até chegar a uma bicicleta, insira o número 1. Se quiser regressar ao menu, insira o número 2""")
                quer = input("Insira a sua opção: ")
                if quer == "1":
                    print(f"{locais}")
                    origem = input("Em que local se encontra? ").strip()
                    
                    if origem not in mapa.adjacencias:
                        print("ERRO: Local de origem não reconhecido no mapa.")
                        continue
                    
                    print("\nA calcular os melhores percursos até uma bicicleta...")
                    ranking_bicicletas = []
                    
                    hora_atual = datetime.now().hour

                    for destino_bicicleta in estacoes_bicicletas:
                        resultado_grafo = mapa.pesquisa_perc(origem, destino_bicicleta, user_login.u_preferencias, hora = hora_atual, k=1)

                        if resultado_grafo:
                            score, caminho = resultado_grafo[0]
                            ranking_bicicletas.append({'local' : destino_bicicleta, 'score':score, 'percurso':caminho, 'quantidade' : gestor_bicicletas.estacoes[destino_bicicleta]['disponiveis']})
            
                    ranking_bicicletas.sort(key=lambda x: x['score'])
                    k = ranking_bicicletas[:5]
                    print(f"Os 5 melhores percursos para alcançar uma bicicleta desde {origem} são:")
            
                    for i, opcao in enumerate(k):
                        print("-"*80)
                        print(f" {i+1}º caminho sugerido: {' -> '.join(opcao['percurso'])}")
                        print(f"Penalização total (Score): {round(opcao['score'], 0)}")
                        print("-" * 80)
                        
                app = AppBicicletas(gestor_bicicletas, db_cidades, mapa, user_login)
                app.mainloop()  

            else:
                print("Cidade não encontrada na base de dados.")  

        elif comando == "ver":
            if not mapa.adjacencias:
                print("ERRO: Nenhum mapa carregado. \nUse 'carregar_mapa' primeiro.")
                continue

            print(f"\nLocais disponíveis: {','.join(mapa.get_locais())}")

            origem = input("Origem: ")
            if origem not in list(mapa.adjacencias):
                print("ERRO: A origem não existe nesta cidade.")
                continue

            destino = input("Destino: ")
            if destino not in list(mapa.adjacencias):
                print("ERRO: O destino não existe nesta cidade.")
                continue
            
            perc = mapa.get_percurso(origem,destino)
            if perc is None:
                continue

            acess = perc['acessibilidade']
            amb = perc['ambiente']
            pop = perc['populacao']

            print(f"\n{'='*50}")
            print(f"PERCURSO: {origem} -> {destino}")
            print(f"DISTÂNCIA: {round(perc['distancia'], 1)}")
            print(f"\n{'='*50}")

            print("\nACESSIBILIDADE")
            print(f"Pavimento       : {acess.pavimento}")
            print(f"Inclinação      : {acess.inclinacao}")
            print(f"Passadeiras     : {acess.passadeiras}")
            print(f"Passeios        : {acess.passeios}")
            print(f"Textura         : {acess.textura_cego}")
            print(f"Escadas         : {acess.escadas}")

            print("\nAMBIENTE")
            print(f"Qualidade do ar : {amb.qualidade_ar}")
            print(f"Poluição sonora : {amb.poluicao_sonora}")
            print(f"Poluição visual : {amb.poluicao_visual}")
            print(f"Nível de pólen  : {amb.nivel_polen}")
            print(f"Iluminação      : {amb.iluminacao}")
            print(f"Sombra          : {amb.sombra}")
            
            print("\nPOPULAÇÃO")
            print(f"Trânsito        : {pop.transito}")
            print(f"Multidão        : {pop.multidao}")
            print(f"\n{'='*50}")     

        elif comando == "ins_cidade":
            try:
                nome = input('Nome da cidade: ').strip()
                if not nome:
                    print('ERRO: O nome da cidade não pode ser vazio!')
                    continue
                
                ficheiro = nome.lower().replace(' ','_')
                diretorio = f'city/grafo_{ficheiro}.json'
                
                if os.path.exists(diretorio):
                    print(f'ERRO: Já existe um ficheiro para {nome}.')
                    continue
 
                # --- Inserção obrigatória de pelo menos um local ---
                print(f"\nPara criar a cidade '{nome}' é necessário adicionar pelo menos um local.")
                print("Podes adicionar mais locais depois com 'ins_local'.\n")
 
                locais_novos = {}   # nome -> (lat, lon)
 
                while True:
                    nome_local = input('Nome do local: ').strip()
                    if not nome_local:
                        print('ERRO: O nome do local não pode ser vazio.')
                        continue
 
                    if nome_local in locais_novos:
                        print(f"ERRO: '{nome_local}' já foi adicionado nesta sessão.")
                        continue
 
                    try:
                        lat = float(input('Latitude : '))
                        lon = float(input('Longitude: '))
                    except ValueError:
                        print('ERRO: Coordenadas inválidas. Insere números decimais.')
                        continue
 
                    locais_novos[nome_local] = (lat, lon)
                    print(f"  ✓ '{nome_local}' adicionado.")
 
                    if len(locais_novos) >= 1:
                        mais = input('\nQueres adicionar mais um local agora? (s/n): ').strip().lower()
                        if mais != 's':
                            break
 
                # Constrói o grafo com os locais recolhidos
                grafo = {
                    'adjacencias': {nome_local: [] for nome_local in locais_novos},
                    'coordenadas': {nome_local: list(coord) for nome_local, coord in locais_novos.items()}
                }
 
                with open(diretorio, 'w', encoding='utf-8') as f:
                    json.dump(grafo, f, indent=2, ensure_ascii=False)
 
                # Atualiza locais.json
                try:
                    with open('locais.json', 'r', encoding='utf-8') as f:
                        db_locais = json.load(f)
                except FileNotFoundError:
                    db_locais = {}
 
                db_locais[nome] = list(locais_novos.keys())
                with open('locais.json', 'w', encoding='utf-8') as f:
                    json.dump(db_locais, f, indent=2, ensure_ascii=False)
 
                # Carrega o novo mapa em memória para estar pronto a usar
                mapa.load_mapa(diretorio)
                caminho_mapa_atual = diretorio
 
                print(f'\nSUCESSO: Cidade "{nome}" criada em {diretorio}')
                print(f'Locais registados: {", ".join(locais_novos.keys())}')
                print("Usa 'ins_percurso' para ligar os locais e 'ins_local' para adicionar mais.")
 
            except Exception as e:
                print(f'ERRO: {e}')  

        elif comando == 'ins_local':
            if not mapa.adjacencias:
                print("ERRO: Nenhum mapa carregado. Use 'carregar_mapa' ou 'ins_cidade' primeiro.")
                continue

            try:
                nome = input('Nome do local: ').strip()
                if not nome:
                    print("ERRO: O nome não pode ser vazio.")
                    continue

                if nome in mapa.adjacencias:
                    print(f"ERRO: '{nome}' já existe no mapa.")
                    continue

                try:
                    x = float(input('Latitude: '))
                    y = float(input('Longitude: '))
                except ValueError:
                    print("ERRO: Coordenadas inválidas. Insere números decimais.")
                    continue

                mapa.add_local(nome, (x, y))
                print(f"{nome} foi adicionado ao mapa com sucesso.")

                # --- Atualiza locais.json ---
                try:
                    with open('locais.json', 'r', encoding='utf-8') as f:
                        db_locais = json.load(f)
                except FileNotFoundError:
                    db_locais = {}

                if cidade_atual is None:
                    print("Aviso: cidade atual desconhecida, locais.json não foi atualizado.")
                elif cidade_atual not in db_locais:
                    print(f"Aviso: '{cidade_atual}' não existe no locais.json. A criar entrada...")
                    db_locais[cidade_atual] = [nome]
                    with open('locais.json', 'w', encoding='utf-8') as f:
                        json.dump(db_locais, f, indent=2, ensure_ascii=False)
                else:
                    if nome not in db_locais[cidade_atual]:
                        db_locais[cidade_atual].append(nome)
                        with open('locais.json', 'w', encoding='utf-8') as f:
                            json.dump(db_locais, f, indent=2, ensure_ascii=False)
                        print(f"'{nome}' adicionado a '{cidade_atual}' em locais.json.")
                    else:
                        print(f"Aviso: '{nome}' já existia em '{cidade_atual}' no locais.json.")

                # --- Guardar mapa: reutiliza o caminho já carregado ---
                guardar = input('Guardar mapa agora? (s/n) ').strip().lower()
                if guardar == 's':
                    if caminho_mapa_atual:
                        mapa.save_mapa(caminho_mapa_atual)
                        
                    else:
                        # fallback: só acontece se o mapa foi criado de raiz sem carregar
                        ficheiro = input("Nome do ficheiro (sem extensão): ").strip()
                        if not ficheiro.endswith(".json"):
                            ficheiro += ".json"
                        if not ficheiro.startswith("city/"):
                            ficheiro = f"city/{ficheiro}"
                        mapa.save_mapa(ficheiro)
                        caminho_mapa_atual = ficheiro
                        print(f'Mapa gravado com sucesso em "{ficheiro}".')

            except Exception as e:
                print(f"ERRO: {e}")

        elif comando == "ins_percurso":
            if not mapa.adjacencias:
                print("ERRO: Nenhum mapa carregado. \nUse 'carregar_mapa' primeiro.")

            print(f"\nLocais disponíveis: {','.join(mapa.get_locais())}")

            origem = input("Origem: ")
            if origem not in list(mapa.adjacencias):
                print("ERRO: A origem não existe nesta cidade.")
                continue

            destino = input("Destino: ")
            if destino not in list(mapa.adjacencias):
                print("ERRO: O destino não existe nesta cidade.")
                continue

            try:
                print("\n -- ACESSIBILIDADE --")
                rug      = float(input("Rugosidade do pavimento (0-100): "))
                dec      = float(input("Inclinação/declive (0-100): "))
                n_passad = int(input("Nº de passadeiras: "))
                passeio  = float(input("Percentagem do percurso com passeio (0-100): "))
                textura  = input("Tem textura tátil para cegos? (s/n): ").strip().lower() == 's'
                escad    = input("Tem escadas? (s/n): ").strip().lower() == 's'

                print("\n -- AMBIENTE --")
                ar     = float(input("Qualidade do ar (0-100, 100=puro): "))
                som    = float(input("Poluição sonora (0-100): "))
                visual = float(input("Poluição visual (0-100): "))
                polen  = float(input("Nível de pólen (0-100): "))
                postes = float(input("Nº de postes de luz: "))
                sombra = float(input("Metros de sombra no percurso: "))

                print("\n -- POPULAÇÃO --")
                transito = input("Tem trânsito intenso? (s/n): ").strip().lower() == 's'
                multidao = input("Tem muita afluência de pessoas? (s/n): ").strip().lower() == 's'

                mapa.add_percurso(
                    origem, destino,
                    rug, dec, n_passad, passeio, textura, escad,
                    ar, som, visual, polen, postes, sombra,
                    transito, multidao
                )
                    
                print(f"SUCESSO: Percurso adicionado de '{origem}' para '{destino}'!")
                print("Use 'gravar_mapa' para guardar as alterações")
                
            except ValueError:
                print("ERRO: Valor inválido. Certifica-te que introduzes números onde pedido.")
            except Exception as e:
                print(f'ERRO: {e}')
            pass

        else:
            print("ERRO: Comando não reconhecido.")
            
if __name__ == '__main__':
    main()