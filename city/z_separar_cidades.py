import json
import os

# 1. Carregar os dados originais (Grafo Completo)
with open('Base_Dados_Parametros_arestas.json', 'r', encoding='utf-8') as f:
    grafo_total = json.load(f)

# 2. Carregar o mapeamento de cidades (Ficheiro novo)
with open('locais.json', 'r', encoding='utf-8') as f:
    cidades_map = json.load(f)

# Criar pasta para os resultados se não existir
if not os.path.exists('cidades_separadas'):
    os.makedirs('cidades_separadas')

# 3. Processar cada cidade
for cidade, locais in cidades_map.items():
    # Estrutura para o novo ficheiro da cidade
    dados_cidade = {
        "cidade": cidade,
        "nodes": {},
        "edges": []
    }
    
    # Extrair os Nós (Nodes) que pertencem a esta cidade
    for local in locais:
        if local in grafo_total['nodes']:
            dados_cidade['nodes'][local] = grafo_total['nodes'][local]
    
    # Extrair as Arestas (Edges) internas desta cidade
    # (Apenas ligações onde a origem e o destino estão na mesma cidade)
    for edge in grafo_total['edges']:
        destino = edge['destino']
        
        # Identificar nome da origem pelas coordenadas
        ox, oy = edge['origem_coord']['x'], edge['origem_coord']['y']
        origem_nome = next((name for name, c in grafo_total['nodes'].items() 
                           if c['x'] == ox and c['y'] == oy), None)
        
        if origem_nome in locais and destino in locais:
            dados_cidade['edges'].append(edge)
    
    # 4. Guardar o ficheiro individual
    file_name = f"cidades_separadas/grafo_{cidade.lower().replace(' ', '_')}.json"
    with open(file_name, 'w', encoding='utf-8') as out_f:
        json.dump(dados_cidade, out_f, indent=2, ensure_ascii=False)

print("Processamento concluído. Ficheiros gerados na pasta 'cidades_separadas'.")