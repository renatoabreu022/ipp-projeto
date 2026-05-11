import json
import matplotlib.pyplot as plt
import networkx as nx

# 1. Carregar os dados do ficheiro JSON
file_path = 'grafo_famalicao.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Criar o objeto do Grafo (Direcionado)
G = nx.DiGraph()

# 3. Extrair coordenadas e adicionar nós
pos = {}
for nome, coords in data['nodes'].items():
    G.add_node(nome)
    # No JSON, x e y são as coordenadas geográficas relativas
    pos[nome] = (coords['x'], coords['y'])

# 4. Adicionar arestas (ligações)
for edge in data['edges']:
    origem = None
    # Como as arestas no teu JSON usam coordenadas de origem, 
    # precisamos de encontrar o nome do nó correspondente a essa coordenada
    ox, oy = edge['origem_coord']['x'], edge['origem_coord']['y']
    
    for nome, coords in data['nodes'].items():
        if coords['x'] == ox and coords['y'] == oy:
            origem = nome
            break
    
    if origem:
        G.add_edge(origem, edge['destino'])

# 5. Configurar a visualização
plt.figure(figsize=(15, 12))
plt.title("Mapa de Grafo: Organização Geográfica dos Nós", fontsize=15)

# Desenhar os nós e as etiquetas
nx.draw_networkx_nodes(G, pos, node_size=30, node_color='red', alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=7, verticalalignment='bottom', font_family='sans-serif')

# Desenhar as arestas com setas para indicar a direção
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=10, alpha=0.4)

# Ajustar e mostrar
plt.axis('off') # Remove os eixos para focar no grafo
plt.tight_layout()
plt.show()

#O GRAFO ESTÁ UM POUCO CONFUSO, ESTÁ A UNIR AS CIDADES TODAS