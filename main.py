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
from models.user import Sistema, Utilizador, Perfil
from models.percursos import ParametrosAcessibilidade, ParametrosAmbiente, ParametrosPopulacao
import json
import random


def help():
    print("\n--- COMANDOS DISPONÍVEIS ---")
    print("ins_utilizador <nome> <perfil>   -> Regista novo utilizador")
    print("login <nome> <password>          -> Login")
    print("gravar <arquivo.json>            -> Salva utilizadores")
    print("ler <arquivo.json>               -> Carrega utilizadores")
    print("sair                             -> Encerra a aplicação")
    print("----------------------------")

# --- LOOP PRINCIPAL ---

def main():
    sistema = Sistema()  # cria a base de dados de utilizadores
    mapa = Mapa()
    user_login = None
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

        elif comando == "ins_utilizador":
            if len(args) != 2:
                print("ERRO: Uso indevido do comando.\nDeverá seguir este modelo: ins_utilizador <nome> <perfil>.")

            else:
                nome, perfil = args
                u = Utilizador(nome, "0000", Perfil(perfil))  # atribui uma password predifinida, deverá ser trocada pelo utilizador
                sistema.add_user(u)
                print(f'Utilizador {nome} criado com o perfil {perfil}.\n Note que lhe foi atribuida a password 0000, por favor, modifique-a.')
        
        elif comando == 'login':
            if len(args) != 2:
                print("ERRO: Uso indevido do comando.\nDeverá seguir este modelo: login <nome> <password>.")
            
            else:
                nome, password = args
                user_login = sistema.login(nome,password)
                if user_login:
                    print('Login realizado com sucesso.')

                else:
                    print('Falha no login.')
        
        elif comando == 'gravar':
            if not args:
                print("ERRO: Uso indevido do comando.\nDeverá seguir este modelo: gravar <arquivo.json>.")
            
            else:
                sistema.save_users(args[0])
                print("Utilizadores gravados com sucesso.")

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
        
        elif comando == 'carregar_mapa':
            if not args:
                print('ERRO: Uso indevido do comando.\nDeverá seguir este modelo: carregar_mapa <ficheiro>.')
            else:
                mapa.load_mapa(args[0])
                
        #novo comando simular com a nova função que está nos grafos
        elif comando == "simular":
            if sistema.utilizador_atual is None:
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
                        grafos.simular_e_recomendar(mapa, sistema.utilizador_atual.u_perfil, origem, destino)
                    else:
                        print("ERRO: Um dos locais não pertence à cidade ou não existe.")
                else:
                    print("ERRO: Cidade não reconhecida.")

        else:
            print("ERRO: Comando não reconhecido.")
            
if __name__ == '__main__':
    main()
