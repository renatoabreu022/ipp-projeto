# ----Dia 30/03/2026 @Renato
# este ficheiro vai servir como o Model no MVC
# ele estará num ciclo infinito à espera de inputs e chama quem os deve processar

from user import Sistema, Utilizador, Perfil
from percursos import Rua, ParametrosAmbiente, ParametrosPopulacao
import json

def help():
    print("\n--- COMANDOS DISPONÍVEIS ---")
    print("ins_utilizador <nome> <perfil>   -> Regista novo utilizador")
    #...
    print("sair                             -> Encerra o programa")
    print("----------------------------")

# --- COMANDOS ---

def cmd_ins_utilizador(args, sist: Sistema):
    if len(args) < 2:
        print('Erro: Comando usado indevidamente. Deve seguir o modelo: ins_utilizador <nome> <perfil>')
        return
    nome, tipo = args[0], args[1] #assumindo que o username é uma só palavra

    if not sist.cria_username(nome):
        return
    
    perfil = Perfil(tipo)
    user = Utilizador(nome, '0000', perfil) #aplica uma password temporária
    sist.add_user(user)
    print(f'Utilizador "{nome}" com o perfil "{perfil}" criado com sucesso.\n')
    print('Por padrão, a sua password está definida como "0000". Por favor, mude-a o mais breve possível.')


def main():
    sist = Sistema() # chamar a base de dados

    print('Seja Bem-vind@! Digite help para esclarecimento de comandos')

    while True:
        entrada = input('\n> ').strip().split() #o programa espera até que haja algum input e, caso haja espaços inuteis, remove-os, não limitando tanto a escrita do utilizador
        if not entrada:
            continue

        comando = entrada[0].lower() # guarda qual o comando feito
        args = entrada[1:] # guarda os argumentos do comando usado

        if comando == 'sair':
            print('A encerrar...')
            break

        elif comando == 'help':
            help()
        
        elif comando == 'ins_utilizador':
            cmd_ins_utilizador(args)