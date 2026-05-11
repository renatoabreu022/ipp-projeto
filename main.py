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
from models.bicicletas2 import GestorBicicletas
import city

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
    print("\n--- COMANDOS DISPONÍVEIS --------------------------------------------------------------------")
    print("signin <nome>                                        -> Regista novo utilizador")
    print("login <nome> <password>                              -> Login")
    print("alterar_password <password_atual> <password_nova>    -> Alterar a password")
    print("quizz                                                -> Altera os parâmetros de preferências")
    print("gravar <arquivo>                                     -> Salva utilizadores")
    print("ler <arquivo>                                        -> Carrega utilizadores")
    print("simular                                              -> Calcula a rota ideal entre dois pontos")
    print("bicicletas                                           -> Mostra as bicicletas disponiveis")
    print("gravar_mapa <ficheiro>                               -> Guarda o mapa atual")
    print("carregar_mapa <ficheiro>                             -> Carrega um mapa guardado")
    print("sair                                                 -> Encerra a aplicação")
    print("----------------------------------------------------------------------------------------------")

# --- LOOP PRINCIPAL ---

def main():
    sistema = Sistema()  # cria a base de dados de utilizadores
    mapa = Mapa()
    user_login = None
    arquivo_db = "utilizadores"
    
    #Tenta carregar os utilizadores logo ao iniciar o programa
    sistema.load_users(arquivo_db)
    gestor_bicicletas = GestorBicicletas()
    print("Bem-vind@! Digite 'help' para comandos.")

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
                else:
                    print("ERRO: Não foi possível criar o utilizador.")
        
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
                    print(f"Login realizado com sucesso. Bem-vindo, {nome}!")

                else:
                    print("Falha no login. Verifique as credenciais.")
        
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
        
        
        elif comando == "quizz":
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
                print("Utilizadores carregados com sucesso.")
        
        elif comando == 'gravar_mapa':
            if not args:
                print('ERRO: Uso indevido do comando.\nDeverá seguir este modelo: gravar_mapa <ficheiro>.')
            else:
                mapa.save_mapa(args[0])
                print("Mapa guardado com sucesso.")
        
        elif comando == 'carregar_mapa':
            if not args:
                print('ERRO: Uso indevido do comando.\nDeverá seguir este modelo: carregar_mapa <ficheiro>.')
            else:
                mapa.load_mapa(args[0])
                print("Mapa carregado com sucesso.")
                
        #novo comando simular com a nova função que está nos grafos
        elif comando == "simular":
            if user_login is None:
                print("ERRO: O processo de login não foi efetuado.")
                continue
            #mapeamento de ficheiros
                # Adicionei o prefixo da pasta 'city_graphs/' antes de cada nome
            cidades_disponiveis = {
                "Aveiro": "city_graphs/city.grafo_aveiro.json",
                "Barcelos": "city_graphs/city.grafo_barcelos.json",
                "Beja": "city_graphs/city.grafo_beja.json",
                "Braga": "city_graphs/city.grafo_braga.json",
                "Caldas Da Rainha": "city_graphs/city.grafo_caldas_da_rainha.json",
                "Coimbra": "city_graphs/city.grafo_coimbra.json",
                "Covilhã": "city_graphs/city.grafo_covilhã.json",
                "Évora": "city_graphs/city.grafo_évora.json",
                "Fafe": "city_graphs/city.grafo_fafe.json",
                "Famalicao": "city_graphs/city.grafo_famalicao.json",
                "Faro": "city_graphs/city.grafo_faro.json",
                "Figueira Da Foz": "city_graphs/city.grafo_figueira_da_foz.json",
                "Guimarães": "city_graphs/city.grafo_guimarães.json",
                "Lagos": "city_graphs/city.grafo_lagos.json",
                "Lisboa": "city_graphs/city.grafo_lisboa.json",
                "Marco De Canaveses": "city_graphs/city.grafo_marco_de_canaveses.json",
                "Portimão": "city_graphs/city.grafo_portimão.json",
                "Porto": "city_graphs/city.grafo_porto.json",
                "Póvoa De Varzim": "city_graphs/city.grafo_póvoa_de_varzim.json",
                "Tomar": "city_graphs/city.grafo_tomar.json",
                "Vila Nova De Gaia": "city_graphs/city.grafo_vila_nova_de_gaia.json",
                "Viseu": "city_graphs/city.grafo_viseu.json"
            }
            print(f"\nCidades disponíveis:{list(cidades_disponiveis.keys(            selecao = input("Escolha a cidade para a simulação:").strip().title()

            if selecao not in cidades_disponiveis:
                print(f"ERRO: A cidade {selecao} não está carregada no sistema.")
                continue
            
            try: #carregar o mapa da Cidade
                mapa.load_mapa(cidades_disponiveis[selecao])
                gestor_bikes = GestorBicicletas(list(mapa.nodes.keys()))

                print(f"\n-- MAPA DE {selecao.upper()} CARREGADO ---")
                print(f"Locais detetados: {','.join(list(mapa.nodes.keys()))}")

                #DEFINIR ROTA
                origem = input("\nDigite o ponto de Partida:").strip()
                destino = input("\nDigite o ponto de Chegada:").strip()
                
                if origem not in mapa.nodes or destino not in mapa.nodes:
                    print("ERRO: Um ou ambos os locais não existem nesta cidade.")
                    continue
                
                #DEFINIR A HORA
                print("\nCoHora Atual Horário:")
                print("[1] Agendardatual")
                print("[2] Simular Hora Específica")
                op_h=input("Opção:")

                if op_h == "2":
                    h_calculo = int(input("Insira a hora pretendida:"))
                else:
                    h_calculo = datetime.now().hour

                print(f"Calculando a melhora rota para as {h_calculo}h...")
                
                #EXECUTAR A SIMULAÇÃO
                resultado = mapa.simular_e_recomendar(user_login.u_preferencias,origem,destino,h_calculo)
        
                if resultado:
                    print("\n" + "="*30)
                    print("RESULTADO DA SIMULAÇÃO")
                    print("="*30)
                    print(f"Caminho Sugerido: {resultado['caminho']}")
                    print(f"Score de Conforto: {resultado['score']:.2f}")
                    print("-"*30)


                    # Verifica se há uma bike perto da origem para ajudar no percurso
                    estacao_proxima, qtd_bikes = gestor_bikes.encontrar_bike_mais_proxima(mapa, origem)
                    if estacao_proxima:
                        print(f"DICA: Existe uma estação de bicicletas em '{estacao_proxima}'")
                        print(f"com {qtd_bikes} unidades disponíveis para a sua partida.")
                    print("="*30)
            
            except Exception as e:
                print(f"ERRO durante a simulação: {e}")
        
        
        elif comando == "bicicletas":
            try:
                with open("locais.json", "r", encoding="utf-8") as f:
                    db_cidades = json.load(f)
            except FileNotFoundError:
                db_cidades = {}
            
            print(f"Cidades disponíveis: {', '.join(db_cidades.keys())}")
            cidade_escolhida = input("Em que cidade se encontra? ").strip()
            
            if cidade_escolhida in db_cidades:
                locais = db_cidades[cidade_escolhida]
                
                gestor_bicicletas.gerar_estacoes_para_cidade(locais)
                
                print(f"Estações de Bicicletas em {cidade_escolhida}")
                for local, info in gestor_bicicletas.estacoes.items():
                    print(f"{local}: {info['disponiveis']} bicicletas disponíveis")

            else:
                print("Cidade não encontrada na base de dados.")              
            

        else:
            print("ERRO: Comando não reconhecido.")
            
if __name__ == '__main__':
    main()
