# ----Dia 30/03/2026 @Renato
# este ficheiro vai servir como o Controller no MVC
# ele estará num ciclo infinito à espera de inputs e chama quem os deve processar

# ----Dia 31/03/2026 @Renato @Claudia

from user import Sistema, Utilizador, Perfil
from percursos import Rua, ParametrosAmbiente, ParametrosPopulacao
import json


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
                user_login = sistema.login(nome)
                if sistema.login(nome,password):
                    print('Login realizado com sucesso.')

                else:
                    print('Falha no login.')
        
        elif comando == 'gravar':
            if not args:
                print("ERRO: Uso indevido do comando.\nDeverá seguir este modelo: gravar <arquivo.json>.")
            
            else:
                sistema.save_users(args[1])
                print("Utilizadores gravados com sucesso.")

        elif comando == 'ler':
            if not args:
                print("ERRO: Uso indevido do comando.\nDeverá seguir este modelo: ler <arquivo.json>.")
            else:
                sistema.load_users(args[1])
                print("Utilizadores carregados com sucesso.")
                
                
        elif comando == 'simular':
            if not user_login:
                print("ERRO: O processo de login não foi efetuado.")
                
            #se já tiver feito login, carrega a base de dados dos locais
            else: 
                try:
                    with open("locais.json", "r") as f:
                        cidades = json.load(f)
                
                except FileNotFoundError:
                    print("ERRO: Base de dados 'locais.json' não encontrada.")
                    continue
                
            #aceder às cidades na base de dados
            cid = cidades.keys()
            print(f"Cidades disponíveis: {cid}")
            cid_selecionada = input("Insira a cidade: ")
            
            if cid_selecionada in cidades:
                estabelecimentos = cidades[cid_selecionada]
                print(f"Locais na cidade selecionada: {estabelecimentos}")
                
            
        
        else:
            print("ERRO: Comando não reconhecido.")
            
if __name__ == '__main__':
    main()
