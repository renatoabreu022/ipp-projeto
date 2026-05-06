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
    #sistema.load_users(arquivo_db)
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
                    # Criamos um utilizador com a password padrão e preferências padrão (tudo a 5)
                    novo_user = Utilizador(nome, "0000", Preferencias())
                    sistema.add_user(novo_user)
                    
                    # Guardamos logo na base de dados
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
            else:
                #carregar base de dados
                try:
                    with open("locais.json", "r", encoding="utf-8") as f:
                        cidades = json.load(f)
                except FileNotFoundError:
                    print("ERRO: Base de dados 'locais.json' não encontrada.")
                    continue

                print(f"Cidades disponíveis: {list(cidades.keys())}")
                cid_selecionada = input("Insira a cidade: ")

                if cid_selecionada in cidades:
                    estabelecimentos = cidades[cid_selecionada]
                    print(f"Locais em {cid_selecionada}: {estabelecimentos}")

                    origem = input("Ponto de partida: ")
                    destino = input("Ponto de chegada: ")

                    if origem in estabelecimentos and destino in estabelecimentos:
                        #CHAMA A FUNÇÃO QUE LIGA TUDO que está no file dos grafos
                        mapa.simular_e_recomendar(mapa, sistema.login.u_perfil, origem, destino)
                    else:
                        print("ERRO: Um dos locais não pertence à cidade ou não existe.")
                else:
                    print("ERRO: Cidade não reconhecida.")

        else:
            print("ERRO: Comando não reconhecido.")
            
if __name__ == '__main__':
    main()
