#---29/04/2026----------------#
#---Mi persona Lucas e talvez Cláudia----------#
#_____Reformulação do cálculo de percurso______#

#-----Imports---------#
from models.user import Preferencias
from models.percursos import ParametrosAcessibilidade,ParametrosAmbiente

class CalculoPeso:
    @staticmethod
    
    def calcular_score(preferencias:Preferencias,rua:ParametrosAcessibilidade,ambiente:ParametrosAmbiente):
        score = 0

        match rua.pavimento:
            case "Pavimento Muito Irregular":
                score += preferencias.peso_pavimento*1
            case "Pavimento Irregular":
                score += preferencias.peso_pavimento*0.75
            case "Pavimento Ligeiramente Irregular":
                score +=preferencias.peso_pavimento*0.5
            case  "Pavimento Regular":
                score +=preferencias.peso_pavimento*0.25

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
            case "O percurso não inclui escadas.":
                score += preferencias.peso_escadas

        match ambiente.temp:
            case "Risco Elevado.":
                score += preferencias.peso_temperatura*1
            case "Risco Moderado.":
                score+=preferencias.peso_temperatura*0.75
            case "Desconforto Ligeiro.":
                score+=preferencias.peso_temperatura*0.5
            case "Ideal.":
                score+=preferencias.peso_temperatura*0.25
                
        match ambiente.qualiadade_ar:
            case "Excelente":
                score+=preferencias.peso_ar*0.2
            case "Boa":
                score += preferencias.peso_ar*0.4
            case "Risco Moderado":
                score += preferencias.pesso_ar*0.6
            case 
                
        
        match ambiente.polen:
            case "Ideal. Ar limpo."

selfcore += pref                   

        match ambiente.iluminacao:
            case "Iluminação Elevada":
                score += preferencias.peso_iluminacao*(1/3)
            case "Iluminação Moderada":
                score += preferencias.peso_iluminacao*(2/3)
            case "Fraco (Má visibilidade)":
                score += preferencias.peso_iluminacao*(1)
                
            
        match ambiente.sombra:
            case "Sombra reduzida":
                score += preferencias.peso_sombra*(1/3)
            case "Sombra moderada":
                score += preferencias.peso_sombra*(2/3)
            case "Sombra abrangente":
                score += preferencias.peso_sombra*(1)
                
                
                
