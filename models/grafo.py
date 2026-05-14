from models.percursos import ParametrosAcessibilidade, ParametrosAmbiente, ParametrosPopulacao
from models.user import Preferencias
from engine.calculo_percurso import CalculoPeso
import math as m
import json

class Mapa: # Armazena a rede urbana da cidade a criar
    def __init__(self):
        self.adjacencias = {} # Guarda os percursos entre locais
        self.coordenadas = {} # Guarda as coordenadas de cada local
    
    # Calcula a distância entre dois pontos usando as coordenadas
    @staticmethod
    def dist(coord1:tuple,coord2:tuple):
        x1, y1 = coord1
        x2, y2 = coord2
        return m.sqrt((x1-x2)**2 + (y1-y2)**2)

    # Regista um novo local no sistema
    def add_local(self, nome, coord:tuple):
        if nome not in self.adjacencias:
            self.adjacencias[nome] = []
            self.coordenadas[nome] = coord
            print(f'{nome} foi adicionado ao mapa com sucesso.')

        else:
            print(f'ERRO: {nome} já existe no mapa.')
    
    # Devolve a lista de locais disponíveis
    def get_locais(self):
        return list(j for j in self.adjacencias)

    # Cria uma conexão entre dois locais no sentido origem -> destino
    def add_percurso(self, origem, destino, rug:float, dec:float, n_passad:int, passeio:float, textura:bool, escad:bool, ar:float, som:float, visual:float, polen:float, post_luz:float, sombra:float, transito:bool, multidao:bool , hora=12, score=0):
        if origem not in self.adjacencias: # verifica se os locais já estão identificados no mapa
            print(f'ERRO: {origem} não existe no mapa.')
            return
        
        if destino not in self.adjacencias:
            print(f'ERRO: {destino} não existe no mapa.')
            return
        
        # Verifica se o percurso já existe (evita duplicados)
        for perc in self.adjacencias[origem]:
            if perc['destino'] == destino:
                print(f'ERRO: Já existe um percurso de {origem} para {destino}.')
                return
        
        distancia = self.dist(self.coordenadas[origem], self.coordenadas[destino])

        # Define as instâncias dos diversos parâmetros
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

        # Agregação de todos os fatores que englobam o percurso num dicionário
        percurso = { 
            'destino': destino,
            'distancia': distancia,
            'acessibilidade': acess,
            'ambiente': amb,
            'populacao': pop
        }

        # Adição do percurso (dicionário) à sua respetiva origem
        self.adjacencias[origem].append(percurso) 

    # Recupera a informação relativa a um percurso específico
    def get_percurso(self,origem,destino):
        if origem not in self.adjacencias:
            print(f'ERRO: {origem} não existe no mapa.')
            return
        
        for perc in self.adjacencias[origem]:
            if perc['destino'] == destino:
                return perc
        
        print(f'ERRO: Não existe um percurso de {origem} para {destino}.')
        return None
    
    # Lista todos os percursos disponíveis
    def list_percursos(self):
        if not self.adjacencias:
            print('Não existem percursos registados.')
            return
        
        for origem, percs in self.adjacencias.items():
            for perc in percs:
                print(f'{origem} -> {perc['destino']}\n')

    # Algoritmo de recomendação dos k (igual a 3 por omissão) percursos mais favoráveis
    def pesquisa_perc(self, origem, destino, preferencias, hora, k=3):
        if origem not in self.adjacencias:
            print(f'ERRO: {origem} não existe no mapa.')
            return []
        
        if destino not in self.adjacencias:
            print(f'ERRO: {destino} não existe no mapa.')
            return []
        
        candidatos = [(0, [origem])] 
        encontrados = []
        visitados = set()

        while candidatos: 
            if len(encontrados) >= k: 
                melhor_cand = min(c[0] for c in candidatos)
                pior_enc = max(e[0] for e in encontrados)

                if melhor_cand >= pior_enc:
                    break

            melhor = 0 

            for i in range(1, len(candidatos)): 
                if candidatos[i][0] < candidatos[melhor][0]: 
                    melhor = i
            
            score_atual, caminho = candidatos.pop(melhor) 
            local_atual = caminho[-1] 

            if local_atual == destino: 
                caminho_tup = tuple(caminho) 
                if caminho_tup not in visitados: 
                    encontrados.append((score_atual, caminho)) 
                    visitados.add(caminho_tup) 
                continue

            for adj in self.adjacencias[local_atual]: 
                viz = adj['destino'] 

                if viz not in caminho: 
                    acess = adj['acessibilidade']
                    amb = adj['ambiente']
                    pop = adj['populacao']
                    
                    # O score é calculado dinamicamente com base no perfil do utilizador
                    score_increm = CalculoPeso.calcular_score(preferencias,acess,amb,pop,hora) if acess and amb and pop else 0
                    score_new = score_atual + score_increm

                    novo_caminho = caminho + [viz]
                    candidatos.append((score_new, novo_caminho))
                    
        return sorted(encontrados, key=lambda x: x[0])
    
    # Guarda o estado atual do mapa num ficheiro JSON
    def save_mapa(self, ficheiro):
        dados = {
            'adjacencias': {},
            'coordenadas': self.coordenadas
        } 

        for origem, percursos in self.adjacencias.items():
            dados['adjacencias'][origem] = []

            for perc in percursos:
                perc_dict = {
                    'destino': perc['destino'],
                    'distancia': perc['distancia'],
                    'acessibilidade': perc['acessibilidade'].to_dict() if perc['acessibilidade'] else None,
                    'ambiente': perc['ambiente'].to_dict() if perc['ambiente'] else None,
                    'populacao': perc['populacao'].to_dict() if perc['populacao'] else None
                }
                dados['adjacencias'][origem].append(perc_dict) 
                
        with open(ficheiro, 'w', encoding= 'utf-8') as f:
            json.dump(dados,f,indent=4,ensure_ascii=False)

        print(f'Mapa gravado com sucesso em "{ficheiro}".')
    
    # Carrega dados de um mapa existente num ficheiro JSON
    def load_mapa(self, ficheiro):
        try:
            with open(ficheiro, 'r', encoding= 'utf-8') as f:
                dados = json.load(f)

            self.adjacencias = {} 
            self.coordenadas = dados.get('coordenadas', {})
            adjacencias_dados = dados.get('adjacencias', dados)

            for origem, percursos in adjacencias_dados.items():
                self.adjacencias[origem] = []

                for perc_dict in percursos:
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
    
    # Carrega a lista de locais da cidade a partir de um ficheiro JSON.
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
