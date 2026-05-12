#----------Para criar gráficos----------#

from models.percursos import ParametrosAcessibilidade,ParametrosAmbiente,ParametrosPopulacao
import matplotlib as plt
import numpy as np

class AnalisadorVisual:

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

    def mapear_seguranca_rodoviaria(acess:ParametrosAcessibilidade,amb:ParametrosAmbiente):
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
        passadeira=acess.passadeiras.split(".")
        match acess.passadeira[0]:
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

        return (nota_ilu+nota_pass+nota_passeios)/3
    
    @static_method
    def mapear_comf_amb(amb:ParametrosAmbiente):

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

            case " Sombra reduzida":
                nota_sombra = 1

        return (nota_qual_ar+nota_polen+nota_sombra+nota_sombra)/4
    
    @staticmethod

    def mapear_sossego(amb:ParametrosAmbiente,pop:ParametrosPopulacao):

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

        return (nota_multidao+nota_polui_visual+nota_ruido)/3
    
    @staticmethod
    def mapear_transito(pop:ParametrosPopulacao):
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

        return (nota_multidao+nota_transito)/2
    
    @staticmethod
    def radar(caminho,mapa_obj):

        categorias = ["Pavimento","Sgurança","Ambiente","Afluência e Sossego","Trânsito"]

        somas = [0]*5

        num_ruas = len(caminho)-1

        for i in range(num_ruas):
            p = mapa_obj.get_percurso(caminho[i],caminho[i+1])  #Encontra a rua entre 2 vértices do percurso

            n_pav = AnalisadorVisual.mapear_acessibilidade(p["acessibilidade"])
            n_seg = AnalisadorVisual.mapear_seguranca_rodoviaria(p["acessibilidade"],p["ambiente"])  #Calculas as notas dos parâmetros
            n_amb = AnalisadorVisual.mapear_comf_amb(p["ambiente"])
            n_soss = AnalisadorVisual.mapear_sossego(p["ambiente"],p["populacao"])
            n_tran = AnalisadorVisual.mapear_transito(p["populacao"])

            somas[0] += n_pav  # soma as notas
            somas[1] += n_seg
            somas[2] += n_amb
            somas[3] += n_soss
            somas[4] += n_tran

        medias = [s/num_ruas for s in somas]  # lista em compressão que calcula as médias


        # CRIAÇÃO DO GRÁFICO

        angulos = np.linspace(0,2*np.pi, len(categorias),endpoint=False).tolist()
        medias += medias[:1]
        angulos += angulos[:1]

        fig,ax = plt.subplots(figsize=(6,6),subplot_kw=dict(polar=True))
        ax.fill(angulos, medias, color='teal', alpha=0.25)
        ax.plot(angulos, medias, color='teal', linewidth=2)
        ax.set_yticklabels([])
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias)
        
        plt.title("Análise de Conforto da Rota", size=15, y=1.1)
        plt.show()