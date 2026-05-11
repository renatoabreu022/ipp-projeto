#_________Teste Biblioteca de Bicicletas_________#
#Lucas-02/05/26#

import random

class GestorBicicletas:
    def __init__(self, locais_mapa):
        self.estacoes={} #aonde podem estar as estações
        locais_com_bike=random.sample(locais_mapa,k=5) #5 locais vão ter bicicletas

        for local in locais_com_bike:
            self.estacoes[local]={"total_vagas":20,
                                  "disponiveis":random.randint(0,20),#cada estação tem entre 1 e 20 bicicletas
                                    "estado":"Operacional"}
            
    
    def verificar_disponibilidade(self,local):
        if local in self.estacoes:
            info = self.estacoes[local]
            return f"{info['disponiveis']} bicicletas disponíveis em {local}."
        return "Não existe estação de bicicletas nesse local." 
    

def bike_mais_proxima(mapa, local_atual, gestor_bikes:GestorBicicletas):
    min_dist=float('inf') #basicamente, a minima distancia é infinitamente positiva, para já, só para inicializar
    melhor_estacao=None

    for estacao, dados in gestor_bikes.estacoes.items():
        if dados["disponiveis"] > 0:
            dist=mapa.dist(mapa.coordenadas[local_atual], mapa.coordenadas[estacao])
            if dist < min_dist:
                min_dist=dist
                melhor_estacao=estacao

        return melhor_estacao, min_dist