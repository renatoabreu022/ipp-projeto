#----------Para criar gráficos----------#

from models.percursos import ParametrosAcessibilidade,ParametrosAmbiente,ParametrosPopulacao
import matplotlib.pyplot as plt
import numpy as np

class AnalisadorVisual:

    @staticmethod
    def ajustes_horario(hora):
        ajustes = {
            "sombra":1,
            "iluminacao":1,
            "poluicao_visual":1,
            "transito":1,
            "multidao":1,
            "temperatura":1
        }

        if hora >=0 or hora <= 6:  #MADRUGADA
            ajustes["sombra"] = 0
            ajustes["iluminacao"] = 2
            ajustes["poluicao_visual"] = 1.5
            ajustes["transito"] = 0.5
            ajustes["multidao"]=0.5
            ajustes["temperatura"] = 0.75

        #MANHÃ NÃO AGRAVA NADA
        elif hora >11 or hora <= 16:  # PICO CALOR
            ajustes["sombra"] = 2
            ajustes["multidao"]=1.25
            ajustes["temeratura"] = 1.75

        elif hora > 16 or hora <= 19: #FINAL TARDE
            ajustes["transito"] = 2
            ajustes["multidao"]= 2
            ajustes["sombra"] = 0.75
        
        elif hora > 19 or hora <= 24: #NOITE
            ajustes["sombra"] = 0
            ajustes["iluminacao"] = 1.25
            ajustes["poluicao_visual"] = 1.25
            ajustes["transito"] = 0.75
            ajustes["multidao"]=0.75

        return ajustes

    @staticmethod

    def mapear_acessibilidade(acess:ParametrosAcessibilidade):
        nota = 3

        if acess.pavimento == "Pavimento Regular": nota = 5
        elif acess.pavimento == "Pavimento Ligeiramente Irregular": nota = 4
        elif acess.pavimento == "Pavimento Irregular": nota = 2
        elif acess.pavimento == "Pavimento Muito Irregular": nota = 1

        # INCLINAÇÃO (Ajusta a média)
        if acess.inclinacao == "Nível Baixo": nota = (nota + 5) / 2
        elif acess.inclinacao == "Nível Moderado": nota = (nota + 4) / 2
        elif acess.inclinacao == "Nível Elevado": nota = (nota + 2) / 2
        elif acess.inclinacao == "Nível Muito Elevado": nota = (nota + 1) / 2
        
        return nota
    
    @staticmethod

    def mapear_seguranca_rodoviaria(acess:ParametrosAcessibilidade,amb:ParametrosAmbiente,hora):
        ajustes = AnalisadorVisual.ajustes_horario(hora)
        
        nota_ilu = 3

        match amb.iluminacao:
            case "Ótima":
                nota_ilu = 5
            case "Iluminação Elevada":
                nota_ilu=4
            case "Iluminação Moderada":
                nota_ilu = 3
            case "Fraco (Má visibilidade)":
                nota_ilu = 2
            case "Sem iluminação.":
                nota_ilu = 1

        nota_pass=3
        match acess.passadeiras:
            case "Elevado":
                nota_pass = 5
            case "Baixo":
                nota_pass = 1

        nota_passeios=3

        match acess.passeios:
            case "Elevado. Risco reduzido.":
                nota_passeios = 5

            case "Reduzido. Risco elevado.":
                nota_passeios = 1

        return ((nota_ilu*ajustes["iluminacao"])+nota_pass+nota_passeios)/3
    
    @staticmethod
    def mapear_comf_amb(amb:ParametrosAmbiente,hora):

        ajustes = AnalisadorVisual.ajustes_horario(hora)

        nota_qual_ar=3

        match amb.qualidade_ar:
            case "Excelente":
                nota_qual_ar=5
            case "Boa":
                nota_qual_ar=4
            case "Risco Moderado":
                nota_qual_ar=2
            case "Risco Elevado":
                nota_qual_ar=1

        nota_polen=3
        match amb.nivel_polen:
            case "Ideal. Ar limpo.":
                nota_polen = 5

            case "Risco Ligeiro":
                nota_polen = 4

            case "Risco Moderado":
                nota_polen = 2

            case "Risco Elevado":
                nota_polen = 1

        nota_temp = 3

        match amb.temp:
            case "Ideal.":
                nota_temp = 5

            case "Desconforto Ligeiro.":
                nota_temp = 4

            case "Risco Moderado.":
                nota_temp = 2

            case "Risco Elevado.":
                nota_temp = 1

        nota_sombra = 3

        match amb.sombra:
            case "Sombra abragente":
                nota_sombra = 5

            case "Sombra reduzida":
                nota_sombra = 1

        return (nota_qual_ar+nota_polen+(nota_temp*ajustes["temperatura"])+(nota_sombra*ajustes["sombra"]))/4
    
    @staticmethod
    def mapear_sossego(amb:ParametrosAmbiente,pop:ParametrosPopulacao,hora):

        ajustes = AnalisadorVisual.ajustes_horario(hora)

        nota_polui_visual=3

        match amb.poluicao_visual:
            case "Ideal":
                nota_polui_visual = 5
            case "Desconfortável":
                nota_polui_visual = 1

        nota_ruido=3

        match amb.poluicao_sonora:
            case "Ideal":
                nota_ruido = 5

            case "Desconfortável":
                nota_ruido = 1

        nota_multidao=3

        match pop.multidao:
            case "Zona de elevada afluência de peões.":
                nota_multidao = 2

            case "Zona de reduzida afluência de peões.":
                nota_multidao = 5

        return ((nota_multidao*ajustes["multidao"]) + (nota_polui_visual*ajustes["poluicao_visual"]) + nota_ruido)/3
    
    @staticmethod
    def mapear_transito(pop:ParametrosPopulacao,hora):

        ajustes = AnalisadorVisual.ajustes_horario(hora)

        nota_transito = 3

        match pop.transito:
            case "No percurso selecionado, a probabilidade de interseção com tráfego automóvel é elevada.":
                nota_transito= 2

            case "No percurso selecionado, a probabilidade de interseção com tráfego automóvel é reduzida.":
                nota_transito = 5

        nota_multidao=3

        match pop.multidao:
            case "Zona de elevada afluência de peões.":
                nota_multidao = 2

            case "Zona de reduzida afluência de peões.":
                nota_multidao = 5

        return ((nota_multidao*ajustes["multidao"])+(nota_transito*ajustes["transito"]))/2
    
    @staticmethod
    def calcular_medias(caminho, mapa_obj,hora):
        """Função auxiliar para calcular as médias de um caminho."""
        if not caminho:
            return None
            
        somas = [0] * 5
        ruas_encontradas = 0
        
        for i in range(len(caminho) - 1):
            origem, destino = caminho[i], caminho[i+1]
            if origem in mapa_obj.adjacencias:
                for adj in mapa_obj.adjacencias[origem]:
                    if adj['destino'] == destino:
                        ruas_encontradas += 1
                        # Mapeamento (Ajusta os índices conforme a tua preferência)
                        somas[0] += AnalisadorVisual.mapear_acessibilidade(adj['acessibilidade'])
                        somas[1] += AnalisadorVisual.mapear_seguranca_rodoviaria(adj["acessibilidade"],adj["ambiente"],hora)
                        somas[2] += AnalisadorVisual.mapear_comf_amb(adj["ambiente"],hora)
                        somas[3] += AnalisadorVisual.mapear_sossego(adj["ambiente"],adj["populacao"],hora)
                        somas[4] += AnalisadorVisual.mapear_transito(adj['populacao'],hora)
                        break
        
        return [s / ruas_encontradas for s in somas] if ruas_encontradas > 0 else [0]*5

    @staticmethod
    def radar(caminho_atual, caminho_anterior, mapa_obj,hora):
        """Gera o radar comparando o percurso atual com o anterior."""
        
        # 1. INICIALIZAÇÃO OBRIGATÓRIA (Evita o erro de "não definido")
        medias_prev = None 
        medias_atual = None
        categorias = ['Pavimento', 'Segurança', 'Ambiente', 'Multidão', 'Trânsito']
        
        # 2. CÁLCULO DOS DADOS
        medias_atual = AnalisadorVisual.calcular_medias(caminho_atual, mapa_obj,hora)
        
        if caminho_anterior is not None:
            medias_prev = AnalisadorVisual.calcular_medias(caminho_anterior, mapa_obj,hora)

        # 3. CONFIGURAÇÃO DO GRÁFICO
        N = len(categorias)
        angulos = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angulos += angulos[:1] # Fechar o círculo

        fig, ax = plt.subplots(figsize=(8, 10), subplot_kw=dict(polar=True))

        # 4. DESENHO DO GRÁFICO ANTERIOR (A "Sombra")
        # Só desenha se medias_prev tiver valores (não for None)
        if medias_prev is not None:
            v_prev = medias_prev + medias_prev[:1]
            ax.plot(angulos, v_prev, color='black', linestyle='--', alpha=0.5, label='Caminho Anterior')
            ax.fill(angulos, v_prev, color='black', alpha=0.1)

        # 5. DESENHO DO GRÁFICO ATUAL (O Destaque)
        if medias_atual is not None:
            v_atual = medias_atual + medias_atual[:1]
            ax.plot(angulos, v_atual, color='teal', linewidth=2, label='Caminho Atual')
            ax.fill(angulos, v_atual, color='teal', alpha=0.3)

        # Ajustes Visuais
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias)
        ax.set_ylim(0, 5)
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.title("Comparação Visual de Conforto", size=15, y=1.1)
        
        plt.show()