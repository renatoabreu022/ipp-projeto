# -- Dia 31/03/2026 @Renato
# -- Dia 02/04/2026 @Renato
# -- Dia 18/04/2026 @Cláudia

# um grafo é um meio de representar conexões entre coisas e é constituído por 2 componentes:
# Nós - o nosso caso, locais dass cidades
# Arestas - percursos entre locais com os devidos parâmetros associados

#   [Castelo] —— percurso ——> [Hospital]
#                    ^
# (pavimento, inclinação, temperatura, etc.)

# ainda, ir do hospital para o parque pode não ser o mesmo que ir do parque para o hospital
# isto é, numa direção pode ser subida, fazendo com que na oura seja uma descida
# não sei se isto não seria interessante de utilizar

# grafo = {origem: [{"destino": destino,"acessibilidade": ParametrosAcessibilidade,"ambiente": ParametrosAmbiente,"populacao": ParametrosPopulacao}]}

# para nós, um grafo é o mapa da cidade

from models.percursos import ParametrosAcessibilidade, ParametrosAmbiente, ParametrosPopulacao
from engine.calculo_percurso import MotorCalculo
import json
import random

class Mapa:
    def __init__(self):
        self.adjacencias = {}
    
    def add_local(self, nome):
        if nome not in self.adjacencias:
            self.adjacencias[nome] = []
            print(f'{nome} foi adicionado ao mapa com sucesso.')

        else:
            print(f'ERRO: {nome} já existe no mapa.')
    
    def get_locais(self):
        return list(j for j in self.adjacencias)

    def add_percurso(self, origem, destino, distancia:float, parAcess=None, parAmb=None, parPop=None):
        if origem not in self.adjacencias: # verifica se os locais já estão identificados no mapa
            print(f'ERRO: {origem} não existe no mapa.')
            return
        
        if destino not in self.adjacencias:
            print(f'ERRO: {destino} não existe no mapa.')
            return
        
        for perc in self.adjacencias[origem]: # verifica se o caminho já existe do ponto 1 para o 2
            if perc['destino'] == destino:
                print(f'ERRO: Já existe um percurso de {origem} para {destino}.')
                return

        percurso = { # aqui cria-se o percurso caso passe os testes anteriores
            'destino': destino,
            'distancia': distancia,
            'acessibilidade': parAcess,
            'ambiente': parAmb,
            'populacao': parPop
        }
        self.adjacencias[origem].append(percurso) # após estar criado, o percurso é adicionado à sua origem

    def get_percurso(self,origem,destino):
        if origem not in self.adjacencias:
            print(f'ERRO: {origem} não existe no mapa.')
            return
        
        for perc in self.adjacencias[origem]: # retorna o percurso entre a origem e o destino, caso exista
            if perc['destino'] == destino:
                return perc
        
        print(f'ERRO: Não existe um percurso de {origem} para {destino}.')
        return None
    
    def list_percursos(self):
        if not self.adjacencias:
            print('Não existem percursos registados.')
            return
        
        for origem, percs in self.adjacencias.items(): # divide o dicionário em origem e percursos, depois pega em cada percurso dessa origem e devolve o destino
            for perc in percs:
                print(f'{origem} -> {perc['destino']}\n')
    
    #@Renato -- ACHO QUE ESTE TIPO DE PESQUISA É POUCO EFICIENTE, É MELHOR TROCAR POR OUTRO TIPO ~~done

    def pesquisa_perc(self,origem,destino,perfil,k=3): # pesquisa pelos k melhores caminhos entre a origem e o destino
        if origem not in self.adjacencias:
            print(f'ERRO: {origem} não existe no mapa.')
            return []
        
        if destino not in self.adjacencias:
            print(f'ERRO: {destino} não existe no mapa.')
            return []
        
        candidatos = [(0, [origem])] # cada caminho é definido como (score acumulado, [locais ordenados])
        encontrados = [] # lista dos k melhores caminhos já encontrados
        visitados = set() # caminhos completos pelos quais já se passou

        while candidatos: # enquanto houver candidatos para explorar
            if len(encontrados) >= k: # se já se tiver encontrado k caminhos
                melhor_cand = min(c[0] for c in candidatos) # verifica o score do candidato com menor score
                pior_enc = max(e[0] for e in encontrados) # verifica o score do pior entre os k encontrados

                # se o pior dos encontrados tiver score maior que o melhor dos candidatos, o ciclo termina
                if melhor_cand >= pior_enc:
                    break

            melhor = 0 # índice do melhor candidato, assume que o primeiro é melhor no início

            for i in range(1, len(candidatos)): # percorre os restantes candidatos
                if candidatos[i][0] < candidatos[melhor][0]: # se encontrar algum melhor, atualiza qual é o melhor
                    melhor = i
            
            score_atual, caminho = candidatos.pop(melhor) # remove e obtém o melhor candidato
            local_atual = caminho[-1] # o local atual é o último do caminho

            if local_atual == destino: # caso o caminho termine no destino
                caminho_tup = tuple(caminho) # converte o caminho em tuplo para ser usado no set
                if caminho_tup not in visitados: # verifica se este ainda não foi encontrado antes
                    encontrados.append((score_atual, caminho)) # guarda como um dos k melhores
                    visitados.add(caminho_tup) # atualiza os visitados para não haver repetição
                continue

            for adj in self.adjacencias[local_atual]: # para cada percurso que sai do local em que estamos
                viz = adj['destino'] # o 'vizinho' é o destino desse percurso

                if viz not in caminho: # para evitar ciclos, verifica se esse vizinho não está já no nosso caminho
                    # extrai parâmetros
                    acess = adj['acessibilidade']
                    amb = adj['ambiente']
                    #adicionar população
                    
                    # calcula o 'custo' do caminho atual
                    score_increm = MotorCalculo.calcular_IC(perfil,acess,amb) if acess and amb else 0
                    score_new = score_atual + score_increm

                    novo_caminho = caminho + [viz]
                    candidatos.append((score_new, novo_caminho))
        return sorted(encontrados, key=lambda x: x[0]) # devolve os caminhos do melhor para o pior


    def recomendar(self, origem, destino, perfil):
        percursos_todos = self.pesquisa_perc(origem, destino)
        
        if not percursos_todos:
            return None, 0
        
        melhor_perc = None
        melhor_score = float('inf') #começamos com "infinito" para qualquer score ser menor que este
        
        for perc in percursos_todos:
            score_atual = 0
            #vamos percorrer os percursos entre pontos, ou seja, se quero ir de A a D vou de A-B, B-C, C-D...
            for i in range(len(perc) - 1):
                de = perc[i]
                para = perc[i+1]
            
                #no nosso grafo, cada item em self.adjacencias[de] é um dic
                #procura a ligação certa no grafo
                for ligacao in self.adjacencias[de]: #percorre todas as ruas que saem do "de" para ver qual delas vai para "para".
                    if ligacao['destino'] == para:
                        acess = ligacao['acessibilidade']
                        amb = ligacao['ambiente']
                    #chama o motor de pontuação
                        score_atual += MotorCalculo.calcular_IC(perfil, acess, amb)
        
            if score_atual < melhor_score:
                melhor_score = score_atual #o melhor score é o mais pequeno, certo?
                melhor_perc = perc
                
        return melhor_perc, melhor_score

    
    def save_mapa(self, ficheiro):
        dados = {} # dicionario que vai replicar a estrutura do grafo para algo que o JSON lê

        for origem, percursos in self.adjacencias.items():
            dados[origem] = []

            for perc in percursos:
                perc_dict = {
                    'destino': perc['destino'],
                    'distancia':perc['distancia'],
                    # to_dict() converte os objetos dos parametros em dicionarios para JSON
                    # estes if ... else None protegem o codigo no caso de os parametros não existirem por alguma razão
                    'acessibilidade': perc['acessibilidade'].to_dict() if perc['acessibilidade'] else None,
                    'ambiente': perc['ambiente'].to_dict() if perc['ambiente'] else None,
                    'populacao': perc['populacao'].to_dict() if perc['populacao'] else None
                }
                dados[origem].append(perc_dict) # adiciona-se cada percurso à sua origem
        
        with open(ficheiro, 'w', encoding= 'utf-8') as f:
            json.dump(dados,f,indent=4,ensure_ascii=False) # foi a AI que me mostrou isto, mas ensure_ascii=False garante que coisas como ç,ã,etc. não se percam
        
        print(f'Mapa gravado com sucesso em "{ficheiro}.json".')
    
    def load_mapa(self, ficheiro):
        try:
            with open(ficheiro, 'r', encoding= 'utf-8') as f:
                dados = json.load(f)

            self.adjacencias = {} # limpa o mapa atual antes de carregar o novo TER CUIDADO DE GUARDAR ANTES DE IMPORTAR

            for origem, percursos in dados.items():
                self.adjacencias[origem] = []

                for perc_dict in percursos:
                    # from_dict() é o inverso de to_dict(). este retorna os dados ao seu estado original
                    acess = ParametrosAcessibilidade.from_dict(perc_dict['acessibilidade']) if perc_dict['acessibilidade'] else None
                    amb = ParametrosAmbiente.from_dict(perc_dict['ambiente']) if perc_dict['ambiente'] else None
                    pop = ParametrosPopulacao.from_dict(perc_dict['populacao']) if perc_dict['populacao'] else None

                    percurso = {
                        'destino': perc_dict['destino'],
                        'distancia': perc_dict['distancia'],
                        'acessibilidade': acess,
                        'ambiente': amb,
                        'populacao': pop
                    }
                    self.adjacencias[origem].append(percurso)
            print(f'Mapa carregado com sucesso de "{ficheiro}".')

        except FileNotFoundError:
            print(f'ERRO: Ficheiro "{ficheiro}" não encontrado.')
    
    def load_locais(self, ficheiro): # ter cuidado, pois isto carrega todos os locais de uma vez sem separar por cidade, depois vemos como queremos implementar cidades
        try:
            with open(ficheiro, 'r', encoding= 'utf-8') as f:
                cidades = json.load(f)
            
            for cidade, locais in cidades.items():
                for local in locais:
                    if local not in self.adjacencias():
                        self.adjacencias[local] = []
            
            print(f'Locais carregados com sucesso de "{ficheiro}".')
        
        except FileNotFoundError:
            print(f'ERRO: Ficheiro "{ficheiro}" não encontrado.')


#----- sinto que esta função está meio deslocada 

#função que supostamente une tudo, a geração de percurso e a recomendação
#aqui reaproveitei aquilo que antes estava no main em "simular" para criar parâmetros aleatórios

def simular_e_recomendar(mapa, perfil, origem, destino):
    #gerar 4 ou menos opções de percurso entre a origem e o destino
    #(Isto garante que o grafo tem dados para trabalhar)
    distancia_base = random.randint(500, 2000) #os percursos podem ser de 500 a 2000 metros
    
    for i in range(4):
        nome_rua = f"Opção {i+1} de {origem} para {destino}"
        
        #parâmetros de pavimemto
        rua = ParametrosAcessibilidade(nome_rua, origem, destino)
        rua.pavimento_(random.randint(0, 100))
        rua.inclinacao_(random.random(0, 100))
        rua.passadeiras_(random.randint(0, 5), distancia_base)
        rua.passeios_(random.randint(0, 100))
        rua.textura_(random.choice([True, False]))
        rua.escadas_(random.choice([True, False]))

        #parâmetros ambientais 
        amb = ParametrosAmbiente(nome_rua, origem, destino)
        amb.temp(random.randint(-5, 35)) 
        amb.percqualidade_ar(random.randint(0, 100))
        amb.poluison(random.randint(0, 100))
        amb.puluivisu(random.randint(0, 100))
        amb.nivelpolen(random.randint(0, 100))
        amb.sombra2(random.randint(0, 100), distancia_base)

        #parâmetros populacionais
        pop = ParametrosPopulacao(nome_rua, origem, destino)
        pop.transito_(random.choice([True, False]))
        pop.multidao_(random.choice([True, False]))

        #adicionar ao grafo 
        mapa.add_percurso(origem, destino, distancia_base, rua, amb, pop)

    #pedimos a recomendação
    percurso, score = mapa.recomendar(origem, destino, perfil)

    if percurso:
        print(f" De acordo com as suas preferância, sugerimos o seguinte percurso: ")
        print(f" {' -> '.join(percurso)}")
        print(f" Índice de Desconforto (IC): {score:.2f}")
    else:
        print("ERRO: Não foi possível calcular um percurso.")
