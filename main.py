# ----Dia 30/03/2026 @Renato
# este ficheiro vai servir como o Controller no MVC
# ele estará num ciclo infinito à espera de inputs e chama quem os deve processar

# ----Dia 31/03/2026 @Renato @Claudia

# ----Dia 02/04/2026 @Renato

from grafo import Mapa
from user import Sistema, Utilizador, Perfil
from percursos import ParametrosAcessibilidade, ParametrosAmbiente, ParametrosPopulacao
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

                origem = input("Ponto de partida: ")
                destino = input("Ponto de chegada: ")

                if origem in estabelecimentos and destino in estabelecimentos:
                    opcoes_percurso = []
                    distancia_percurso = random.randint(5, 3500)
                    #as distâncias entre locais para diferentes percursos são geradas aleatorimente. um número entre 5m e 3500m     

                #no máximo, 2 localizações podem ter 4 percursos possíveis
                for i in range(4):
                    nome_percurso = f"Opção {i+1}: {origem} - {destino}"
                    #aqui se depois formos dar nomes aos percursos, ao invés de "opção", escrevemos a rua

                    #--gerador de parâmetros de pavimento--
                    rua = ParametrosAcessibilidade(nome_percurso, origem, destino)

                    pav = rua.pavimento_(random.randint(0,100))

                    inc =rua.inclinacao_(round(random.random(),2)) #o random.random() gera valores decimais entre 0 e 1

                    passad = rua.passadeiras_(random.randint(0,15), distancia_percurso)

                    passei = rua.passeios_(random.randint(0,100))

                    textu = rua.textura_(random.choice([True, False]))

                    escad = rua.escadas_(random.choice([True, False]))


                    #--gerado de parâmetros ambientais--
                    ambiente = ParametrosAmbiente(nome_percurso, origem, destino)

                    temper = ambiente.temp(random.randint(-5, 35))

                    qualar = ambiente.percqualidade_ar(random.randint(0,100))

                    pol_som = ambiente.poluison(random.randint(0,100))

                    pol_visual = ambiente.puluivisu(random.randint(0,100))

                    polen = ambiente.nivelpolen(random.randint(0,100))

                    #esta ambiente.ilumina() vai depender depois da hora do dia mas para já vou meter como se a hora não fosse levada em conta (=None)
                    #ambiente.ilumina(random.randint(0,15), None, distancia_percurso)
                    #não usei o sombra1 que a Inês definiu usei só o sombra 2
                    somb = ambiente.sombra2(random.randint(0,100), distancia_percurso)


                    #--gerador de parâmetros populacionais
                    popul = ParametrosPopulacao(nome_percurso, origem, destino)

                    trans = popul.transito_(random.choice([True, False]))

                    mult = popul.multidao_(random.choice([True, False]))
                    
                    
                    #no final do ciclo for, guardamos o conjunto de objetos num dicionário
                    percurso_completo = {"Parâmetros de Pavimento": f"Irregularidade do Pavimento: {pav}\n Inclinação: {inc}\n Passadeiras: {passad}\n Passeios: {passei}\n Textura: {textu}\n Escadas: {escad}\n" , 
                                         "Parâmetros ambientais": f"Temperatura: {temper}\n Qualidade do ar:{qualar}\n Poluição Sonora:{pol_som}\n Poluição Visual:{pol_visual}\n Nível de pólen:{polen}\n",
                                         "Parâmetros Populacionais": f"Trânsito:{trans}\n Multidão:{mult}\n"}
                    
                    opcoes_percurso.append(percurso_completo)
                    
                print(opcoes_percurso)
        else:
            print("ERRO: Comando não reconhecido.")
            
if __name__ == '__main__':
    main()
