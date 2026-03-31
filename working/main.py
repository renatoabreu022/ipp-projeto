# ----Dia 30/03/2026 @Renato
# este ficheiro vai servir como o Controller no MVC
# ele estará num ciclo infinito à espera de inputs e chama quem os deve processar

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
                print("ERRO: uso indevido do comando.\nDeverá seguir este modelo: ins_utilizador <nome> <perfil>.")

            else:
                nome, perfil = args
                u = Utilizador(nome, "1234", Perfil(perfil))  # atribui uma password predifinida, deverá ser trocada pelo utilizador
                sistema.add_user(u)
                print(f'Utilizador {nome} criado com o perfil {perfil}.\n Note que lhe foi atribuida a password 0000, por favor, modifique-a.')
        
        elif comando == 'login':
            if len(args) != 2:
                print("ERRO: uso indevido do comando.\nDeverá seguir este modelo: login <nome> <password>.")
            
            else:
                nome, password = args
                if sistema.login(nome,password):
                    print('Login realizado com sucesso.')

                else:
                    print('Falha no login.')
        
        elif comando == 'gravar':
            pass
