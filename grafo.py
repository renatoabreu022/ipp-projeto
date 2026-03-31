# -- Dia 31/03/2026 @Renato

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

from Model_calculopercurso import MotorCalculo

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

    def add_percurso(self, origem, destino, parAcess=None, parAmb=None, parPop=None):
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
            'acessibilidade': parAcess,
            'ambiente': parAmb,
            'população': parPop
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
    
    def pesquisa_perc(self,origem,destino): # pesquisa o grafo inteiro por todos os caminhos possíveis entre os dois pontos
        if origem not in self.adjacencias or destino not in self.adjacencias:
            print('ERRO: O ínicio ou o fim do percurso não estão presentes no mapa.')
            return [] # este return de lista vazia protege o código caso alguém tente gerar uma recomendação dando erro aqui, pois fará com que a recomendação tenha algo em que pegar
        
        queue = [[origem]] # aqui vai-se listar os caminhos a explorar, iniciamos somente com a origem, depois os caminhos expandem até se chegar a todos os caminhos que levam ao destino
        visitados = set() # conjunto de locais já explorados, permite que o método não fique em loop infinito, é um set pq a pesquisa nele é O(1), mas é melhor perguntar à stora se podemos usar
        caminhos = [] # lista de caminhos entre a origem e o destino já encontrados

        while queue:
            cam_atual = queue.pop(0) # retira o caminho mais antigo da fila
            local_atual = cam_atual[-1] # o local em que estamos é sempre o último do caminho

            if local_atual == destino: # caminho completo encontrado
                caminhos.append(cam_atual)
                continue

            if local_atual in visitados: # já estivemos cá, vamos evitar loops infinitos
                continue

            visitados.add(local_atual)

            for perc in self.adjacencias[local_atual]:
                vizinho = perc['destino'] # vai buscar um local ligado ao que estamos agora
                if vizinho not in cam_atual: # evita que se volte para trás
                    cam_novo = cam_atual + [vizinho] # cria um novo caminho com esse local ligado ao atual como local seguinte
                    queue.append(cam_novo) # adiciona esse caminho à fila de caminhos para ser explorado
        
        return caminhos #NOTA: não havendo locais ligados ao atual ainda não visitados, não se cria novo caminho, logo, não há caminhos na fila, estando a fila vazia, o loop acaba
    
    def recomendar(self,):
        pass # isto vai ter que se ligar ao ficheiro do motor de calculo, ainda não o vi direito, por isso não me vou atrever a trabalhar com ele hahahaha