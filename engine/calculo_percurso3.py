#---02/05/2026----------------#
#--- @Lucas  ------#
#_____Reformulação do cálculo de percurso com hora do dia_____#

#-----Imports---------#

from models.user import Preferencias
from models.percursos import ParametrosAcessibilidade,ParametrosAmbiente,ParametrosPopulacao
#--------------------------# 

# Diferença: Parãmetros de poluição visual, sombra, temperatura e iluminação agora têm um ajuste baseado na hora do dia, refletindo a percepção de segurança e conforto em ambientes noturnos. Por exemplo, a poluição visual tem um ajuste maior à noite, enquanto a sombra tem um ajuste reduzido, já que a falta de luz natural torna a sombra menos relevante. A temperatura também tem um ajuste para refletir o desconforto adicional que pode ocorrer à noite. A iluminação tem um ajuste significativo para refletir a importância crítica da iluminação adequada durante a noite para a segurança e conforto dos pedestres t~em ajustes dependendo de ser noite ou não
class CalculoPeso:
    @staticmethod
    
    def calcular_score(preferencias:Preferencias,acess:ParametrosAcessibilidade,amb:ParametrosAmbiente,pop:ParametrosPopulacao,hora):
        score = 0.0

        ajustes = {
            "sombra":1,
            "iluminacao":1,
            "poluicao_visual":1,
            "transito":1,
            "multidao":1,
            "temperatura":1
        }

        if hora >=0 and hora <= 6:  #MADRUGADA
            ajustes["sombra"] = 0
            ajustes["iluminacao"] = 2
            ajustes["poluicao_visual"] = 1.5
            ajustes["transito"] = 0.5
            ajustes["multidao"]=0.5
            ajustes["temperatura"] = 0.75

        #MANHÃ NÃO AGRAVA NADA
        elif hora >11 and hora <= 16:  # PICO CALOR
            ajustes["sombra"] = 2
            ajustes["multidao"]=1.25
            ajustes["temeratura"] = 1.75

        elif hora > 16 and hora <= 19: #FINAL TARDE
            ajustes["transito"] = 2
            ajustes["multidao"]= 2
            ajustes["sombra"] = 0.75
        
        elif hora > 19 and hora <= 24: #NOITE
            ajustes["sombra"] = 0
            ajustes["iluminacao"] = 1.25
            ajustes["poluicao_visual"] = 1.25
            ajustes["transito"] = 0.75
            ajustes["multidao"]=0.75


        match acess.pavimento:
            case "Pavimento Muito Irregular":
                score += preferencias.peso_pavimento*1
            case "Pavimento Irregular":
                score += preferencias.peso_pavimento*0.75
            case "Pavimento Ligeiramente Irregular":
                score +=preferencias.peso_pavimento*0.5
            case "Pavimento Regular":
                score += preferencias.peso_pavimento*0.25

        match acess.inclinacao:
            case "Nível Muito Elevado" :
                score += preferencias.peso_inclinacao*1
            case "Nível Elevado":
                score+=preferencias.peso_inclinacao*0.75
            case "Nível Moderado":
                score+=preferencias.peso_inclinacao*0.5
            case "Nível Baixo":
                score+=preferencias.peso_inclinacao*0.25

        match acess.passadeiras:
            case "Baixo":
                score+=preferencias.peso_passadeiras*1
            case "Moderado":
                score += preferencias.peso_passadeiras*(2/3)
            case "Elevado":
                score+=preferencias.peso_passadeiras*(1/3)

        match acess.passeios:
            case "Reduzido. Risco elevado.":
                score+=preferencias.peso_passeios*1
            case "Moderado. Risco ligeiro.":
                score +=preferencias.peso_passeios*(2/3)
            case "Elevado. Risco reduzido.":
                score+=preferencias.peso_passeios*(1/3)

        match acess.textura_cego:
            case "O percurso não inclui pavimento acessível a pessoas com incapacidade visual que usam bengala.":
                score += preferencias.peso_textura_cego
        
        match acess.escadas:
            case "O percurso inclui escadas.":
                score += preferencias.peso_escadas

        match amb.temp:
            case "Risco Elevado.":
                score += preferencias.peso_temperatura*1*ajustes["temperatura"]
            case "Risco Moderado.":
                score+=preferencias.peso_temperatura*0.75*ajustes["temperatura"]
            case "Desconforto Ligeiro.":
                score+=preferencias.peso_temperatura*0.5*ajustes["temperatura"]
            case "Ideal.":
                score+=preferencias.peso_temperatura*0.25*ajustes["temperatura"]
                
        match amb.qualidade_ar:
            case "Excelente":
                score+=preferencias.peso_ar*0.25
            case "Boa":
                score += preferencias.peso_ar*0.5
            case "Risco Moderado":
                score += preferencias.peso_ar*0.75
            case "Risco Elevado":
                score += preferencias.peso_ar*1
                
        match amb.poluicao_sonora:
            case "Ideal":
                score += preferencias.peso_ruido*(1/3)
            case "Aceitável":
                score += preferencias.peso_ruido*(2/3)
            case "Desconfortável":
                score += preferencias.peso_ruido*1
        
        match amb.poluicao_visual:
            case "Ideal":
                score += preferencias.peso_visual*(1/3)*ajustes["poluicao_visual"]
            case "Aceitável":
                score += preferencias.peso_visual*(2/3)*ajustes["poluicao_visual"]
            case "Desconfortável":
                score += preferencias.peso_visual*1*ajustes["poluicao_visual"]
        
        
        match amb.nivel_polen:
            case "Ideal. Ar limpo.":
                score += preferencias.peso_polen*0.25
            case "Risco Ligeiro":
                score += preferencias.peso_polen*0.50
            case "Risco Moderado":
                score += preferencias.peso_polen*0.75
            case "Risco Elevado":
                score += preferencias.peso_polen*1
                
                
        match amb.iluminacao:
            case "Iluminação Elevada":
                score += preferencias.peso_iluminacao*(1/3) * ajustes["iluminacao"]
            case "Iluminação Moderada":
                score += preferencias.peso_iluminacao*(2/3)*ajustes["iluminacao"]
            case "Fraco (Má visibilidade)":
                score += preferencias.peso_iluminacao*(1)*ajustes["iluminacao"]
                
        
        match amb.sombra:
            case "Sombra reduzida":
                score += preferencias.peso_sombra*(1)*ajustes["sombra"]
            case "Sombra moderada":
                score += preferencias.peso_sombra*(2/3)*ajustes["sombra"]
            case "Sombra abrangente":
                score += preferencias.peso_sombra*(1/3)*ajustes["sombra"]

        match pop.transito:
            case "No percurso selecionado, a probabilidade de interseção com tráfego automóvel é elevada.":
                score += preferencias.peso_transito*(1)*ajustes["transito"]
            case "No percurso selecionado, a probabilidade de interseção com tráfego automóvel é reduzida.":
                score += preferencias.peso_transito*(1/2)*ajustes["transito"]
        

        match pop.multidao:
            case "Zona de elevada afluência de peões.":
                score += preferencias.peso_multidao*(1)*ajustes["multidao"]
            case "Zona de reduzida afluência de peões.":
                score += preferencias.peso_multidao*(1/2)*ajustes["multidao"]
                
                
        return score


                
                
