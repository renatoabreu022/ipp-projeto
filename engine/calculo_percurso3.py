#---02/05/2026----------------#
#--- @Lucas  ------#
#_____Reformulação do cálculo de percurso com hora do dia_____#

#-----Imports---------#

from models.user import Preferencias
from models.percursos import ParametrosAcessibilidade,ParametrosAmbiente
#--------------------------# 

# Diferença: Parãmetros de poluição visual, sombra, temperatura e iluminação agora têm um ajuste baseado na hora do dia, refletindo a percepção de segurança e conforto em ambientes noturnos. Por exemplo, a poluição visual tem um ajuste maior à noite, enquanto a sombra tem um ajuste reduzido, já que a falta de luz natural torna a sombra menos relevante. A temperatura também tem um ajuste para refletir o desconforto adicional que pode ocorrer à noite. A iluminação tem um ajuste significativo para refletir a importância crítica da iluminação adequada durante a noite para a segurança e conforto dos pedestres t~em ajustes dependendo de ser noite ou não
class CalculoPeso:
    @staticmethod
    
    def calcular_score(preferencias:Preferencias,rua:ParametrosAcessibilidade,ambiente:ParametrosAmbiente,hora):
        score = 0.0

        e_noite = hora >=18 or hora < 7

        match rua.pavimento:
            case "Pavimento Muito Irregular":
                score += preferencias.peso_pavimento*1
            case "Pavimento Irregular":
                score += preferencias.peso_pavimento*0.75
            case "Pavimento Ligeiramente Irregular":
                score +=preferencias.peso_pavimento*0.5
            case  "Pavimento Regular":
                score += preferencias.peso_pavimento*0.25

        match rua.inclinacao:
            case "Nível Muito Elevado" :
                score += preferencias.peso_inclinacao*1
            case "Nível Elevado":
                score+=preferencias.peso_inclinacao*0.75
            case "Nível Moderado":
                score+=preferencias.peso_inclinacao*0.5
            case "Nível Baixo":
                score+=preferencias.peso_inclinacao*0.25

        passadeira=rua.passadeiras.split(".")
        match passadeira[0]:
            case "Baixo":
                score+=preferencias.peso_passadeiras*1
            case "Moderado":
                score += preferencias.peso_passadeiras*(2/3)
            case "Elevado":
                score+=preferencias.peso_passadeiras*(1/3)

        match rua.passeios:
            case "Reduzido. Risco elevado.":
                score+=preferencias.peso_passeios*1
            case "Moderado. Risco ligeiro.":
                score +=preferencias.peso_passeios*(2/3)
            case "Elevado. Risco reduzido.":
                score+=preferencias.peso_passeios*(1/3)

        match rua.textura_cego:
            case "O percurso não inclui pavimento acessível a pessoas com incapacidade visual que usam bengala.":
                score += preferencias.peso_textura_cego
        
        match rua.escadas:
            case "O percurso inclui escadas.":
                score += preferencias.peso_escadas

        match ambiente.temp:
            case "Risco Elevado.":
                ajuste = 0.8 if e_noite else 1
                score += preferencias.peso_temperatura*1*ajuste
            case "Risco Moderado.":
                ajuste = 0.7 if e_noite else 1
                score+=preferencias.peso_temperatura*0.75*ajuste
            case "Desconforto Ligeiro.":
                ajuste = 0.65 if e_noite else 1
                score+=preferencias.peso_temperatura*0.5*ajuste
            case "Ideal.":
                ajuste = 0.5 if e_noite else 1
                score+=preferencias.peso_temperatura*0.25*ajuste
                
        match ambiente.qualidade_ar:
            case "Excelente":
                score+=preferencias.peso_ar*0.25
            case "Boa":
                score += preferencias.peso_ar*0.5
            case "Risco Moderado":
                score += preferencias.peso_ar*0.75
            case "Risco Elevado":
                score += preferencias.peso_ar*1
                
        match ambiente.poluicao_sonora:
            case "Ideal":
                score += preferencias.peso_ruido*(1/3)
            case "Aceitável":
                score += preferencias.peso_ruido*(2/3)
            case "Desconfortável":
                score += preferencias.peso_ruido*1
        
        match ambiente.poluicao_visual:
            case "Ideal":
                ajuste = 1.5 if e_noite else 1
                score += preferencias.peso_visual*(1/3)*ajuste
            case "Aceitável":
                ajuste = 1.25 if e_noite else 1
                score += preferencias.peso_visual*(2/3)*ajuste
            case "Desconfortável":
                score += preferencias.peso_visual*1
        
        
        match ambiente.nivelpolen:
            case "Ideal. Ar limpo.":
                score += preferencias.peso_polen*0.25
            case "Risco Ligeiro":
                score += preferencias.peso_polen*0.50
            case "Risco Moderado":
                score += preferencias.peso_polen*0.75
            case "Risco Elevado":
                score += preferencias.peso_polen*1
                
                
        match ambiente.iluminacao:
            case "Iluminação Elevada":
                ajuste = 1.25 if e_noite else 1
                score += preferencias.peso_iluminacao*(1/3) * ajuste
            case "Iluminação Moderada":
                ajuste = 1.5 if e_noite else 1
                score += preferencias.peso_iluminacao*(2/3)*ajuste
            case "Fraco (Má visibilidade)":
                ajuste = 2 if e_noite else 1
                score += preferencias.peso_iluminacao*(1)*ajuste
                
        
        match ambiente.sombra:
            case "Sombra reduzida":
                ajuste = 0.3 if e_noite else 1
                score += preferencias.peso_sombra*(1)*ajuste
            case "Sombra moderada":
                ajuste = 0 if e_noite else 1
                score += preferencias.peso_sombra*(2/3)*ajuste
            case "Sombra abrangente":
                ajuste = 0 if e_noite else 1
                score += preferencias.peso_sombra*(1/3)*ajuste
                
                
        return score

                
                
                
