from models.grafo import Mapa
mapa = Mapa()
mapa.add_local('Casa',(1,2))
mapa.add_local('Escola',(7,9))
mapa.add_local('Padaria',(19,11))
mapa.add_percurso('Casa','Padaria',2.8,3,3,5.6,1,6,7,3,6,7,9,6,8,5)
mapa.save_mapa('123.json')