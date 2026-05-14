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
from models.user import Preferencias
from engine.calculo_percurso import CalculoPeso
import math as m
import json

class Mapa:
    def __init__(self):
        self.adjacencias = {}
        self.coordenadas = {}
    
    @staticmethod
    def dist(coord1:tuple,coord2:tuple):
        x1, y1 = coord1
        x2, y2 = coord2
        return m.sqrt((x1-x2)**2 + (y1-y2)**2)

    def add_local(self, nome, coord:tuple):
        if nome not in self.adjacencias:
            self.adjacencias[nome] = []
            self.coordenadas[nome] = coord
            print(f'{nome} foi adicionado ao mapa com sucesso.')

        else:
            print(f'ERRO: {nome} já existe no mapa.')
    
    def get_locais(self):
        return list(j for j in self.adjacencias)

    def add_percurso(self, origem, destino, rug:float, dec:float, n_passad:int, passeio:float, textura:bool, escad:bool, ar:float, som:float, visual:float, polen:float, post_luz:float, sombra:float, transito:bool, multidao:bool , hora=12, score=0):
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
        
        distancia = self.dist(self.coordenadas[origem], self.coordenadas[destino])

        acess = ParametrosAcessibilidade(origem, destino)
        acess.pavimento_(rug) 
        acess.inclinacao_(dec)
        acess.passadeiras_(n_passad, distancia)
        acess.passeios_(passeio)
        acess.textura_(textura)
        acess.escadas_(escad)

        amb = ParametrosAmbiente(origem, destino)
        amb.percqualidade_ar(ar)
        amb.poluison(som)
        amb.poluivisu(visual)
        amb.nivelpolen(polen)
        amb.ilumina(post_luz, hora, distancia)
        amb.sombra_(sombra, distancia)

        pop = ParametrosPopulacao(origem, destino)
        pop.transito_(transito)
        pop.multidao_(multidao)

        percurso = { # aqui cria-se o percurso caso passe os testes anteriores
            'destino': destino,
            'distancia': distancia,
            'acessibilidade': acess,
            'ambiente': amb,
            'populacao': pop
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

    # esta procura é uma 'mistura' de Custo Uniforme com Dijkstra
    def pesquisa_perc(self, origem, destino, preferencias,hora=12, k=3): # pesquisa pelos k melhores caminhos entre a origem e o destino
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
                    pop = adj['populacao']
                    #adicionar população
                    
                    # calcula o 'custo' do caminho atual
                    score_increm = CalculoPeso.calcular_score(preferencias,acess,amb,pop,hora) if acess and amb and pop else 0
                    score_new = score_atual + score_increm

                    novo_caminho = caminho + [viz]
                    candidatos.append((score_new, novo_caminho))
                    
        return sorted(encontrados, key=lambda x: x[0]) # devolve os caminhos do melhor para o pior
    
    def save_mapa(self, ficheiro):
        dados = {
            'adjacencias': {},
            'coordenadas': self.coordenadas
        } # dicionario que vai replicar a estrutura do grafo para algo que o JSON lê

        for origem, percursos in self.adjacencias.items():
            dados['adjacencias'][origem] = []

            for perc in percursos:
                perc_dict = {
                    'destino': perc['destino'],
                    'distancia': perc['distancia'],
                    # to_dict() converte os objetos dos parametros em dicionarios para JSON
                    # estes if ... else None protegem o codigo no caso de os parametros não existirem por alguma razão
                    'acessibilidade': perc['acessibilidade'].to_dict() if perc['acessibilidade'] else None,
                    'ambiente': perc['ambiente'].to_dict() if perc['ambiente'] else None,
                    'populacao': perc['populacao'].to_dict() if perc['populacao'] else None
                }
                dados['adjacencias'][origem].append(perc_dict) # adiciona-se cada percurso à sua origem
        
        with open(ficheiro, 'w', encoding= 'utf-8') as f:
            json.dump(dados,f,indent=4,ensure_ascii=False) # foi a AI que me mostrou isto, mas ensure_ascii=False garante que coisas como ç,ã,etc. não se percam
        
        print(f'Mapa gravado com sucesso em "{ficheiro}".')
    
    def load_mapa(self, ficheiro):
        try:
            with open(ficheiro, 'r', encoding= 'utf-8') as f:
                dados = json.load(f)

            self.adjacencias = {} # limpa o mapa atual antes de carregar o novo TER CUIDADO DE GUARDAR ANTES DE IMPORTAR
            self.coordenadas = dados.get('coordenadas', {})
            adjacencias_dados = dados.get('adjacencias', dados)

            for origem, percursos in adjacencias_dados.items():
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
    
    def load_locais(self, ficheiro):
        try:
            with open(ficheiro, 'r', encoding= 'utf-8') as f:
                cidades = json.load(f)
            
            for cidade, locais in cidades.items():
                for local in locais:
                    if local not in self.adjacencias:
                        self.adjacencias[local] = []
            
            print(f'Locais carregados com sucesso de "{ficheiro}".')
        
        except FileNotFoundError:
            print(f'ERRO: Ficheiro "{ficheiro}" não encontrado.')
