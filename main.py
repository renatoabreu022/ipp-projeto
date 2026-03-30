# ----Dia 30/03/2026 @Renato
# este ficheiro vai servir como o Model no MVC
# ele estará num ciclo infinito à espera de inputs e chama quem os deve processar

from user import Sistema, Utilizador, Perfil
from percursos import Rua

def help():
    print("\n--- COMANDOS DISPONÍVEIS ---")
    print("ins_utilizador <nome> <perfil>   -> Regista novo utilizador")
    print("ins_percurso <nome> <ori> <dest> -> Regista novo segmento de rua")
    print("list percursos                   -> Lista todos os percursos")
    print("gravar <arquivo.json>            -> Guarda os dados em ficheiro")
    print("ler <arquivo.json>               -> Carrega dados guardados")
    print("sair                             -> Encerra o programa")
    print("----------------------------")

def main():
    sist = Sistema() # chamar a base de dados

    print('Seja Bem-vind@! Digite 'help' para esclarecimento de comandos')

    while True:
        entrada = input('\n> ').strip().split() #o programa espera até que haja algum input e, caso haja espaços inuteis, remove-os, não limitando tanto a escrita do utilizador
        if not entrada:
            continue

        comando = entrada[0].lower() # guarda qual o comando feito
        args = entrada[1:] # guarda os argumentos do comando usado


