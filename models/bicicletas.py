
#------- @Cláudia ----- 11/05
#o objetivo deste ficheiro é criar uma função extra na app para que o utilizador consiga verfificar, na cidade em que se encontra, onde é que pode encontrar bicicletas publicas

import random
class GestorBicicletas:
    def __init__(self):
        self.estacoes = {}
    
    def gerar_estacoes_para_cidade(self, locais_da_cidade):
        self.estacoes = {}
        k_vagas = random.choice([3, 4])
        num_estacoes = min(len(locais_da_cidade), k_vagas)
        locais_sorteados = random.sample(locais_da_cidade, k = num_estacoes)
        
        
        for local in locais_sorteados:
            self.estacoes[local] = {
                "total_vagas" : 5,
                "disponiveis" : random.randint(1,5),
                "estado" : "Operacional"
            }