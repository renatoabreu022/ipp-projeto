#------------31/03/2026-------@Lucas@Inês------------------#

#____________imports______________#
from models.user import Perfil
from models.percursos import ParametrosAcessibilidade, ParametrosAmbiente

class MotorCalculo:

    @staticmethod
    def calcular_IC(perfil:Perfil,rua:ParametrosAcessibilidade,ambiente:ParametrosAmbiente): #IC-> Indice de conforto, serve para calcular o conforto do percurso, quanto maior pior o percurso, maior o IC, ou seja, mais stressante é o percurso
        score = 0
        tipo_user=perfil.get_tipo().lower()
#__________________________________________Penalização de acessibilidade__________________________________________________#

#---Inclinação---#
        if perfil.need_acessibilidade() and "inclui_escadas" in rua.escadas:
            score+=40

        if perfil.need_acessibilidade() and "Nível Muito Elevado" in rua.inclinacao:
            score+=30
        
        elif perfil.need_acessibilidade() and "Nível Elevado" in rua.inclinacao:
            score+=20

        elif perfil.need_acessibilidade() and "Nível Moderado" in rua.inclinacao:
            score+=5

#-----Passeioss-----#

        match rua.passeios:
            case "Reduzido. Risco elevado":
                score +=20
            case "Moderado. Risco ligeiro":
                score+=10

#-----Passadeiras---#
        passadeira=rua.passadeiras.split(".")
        match passadeira[0]:
            case "Baixo":
                score+=15

            case "Moderado":
                score+=5
                            
#_____________________________________Classificação especial- Cegos____________________________________________________________#
        if "cego" in [inc.lower() for inc in perfil.get_incapacidades()]:
            if "O percurso não inclui pavimento acessível a pessoas com incapacidade visual que usam bengala." in rua.textura_cego:
                score+=50
                
        
        
#_________________Alergias I guess____________________________________________________________#
        if perfil.has_alergia("pólen"):
            if "Risco Elevado" in ambiente.nivel_polen:
                score+=30

            elif "Risco Moderado" in ambiente.nivel_polen:
                score+=15

            elif "Risco Ligeiro" in ambiente.nivel_polen:
                score+=5


#_________________Penalização de Parametros do ambiente???????____________________________________________________________#


#_______________Temperatura____________#
        
        pvulneraveis=["idoso","criança"]

        if ambiente.temp=="Risco Elevado.":
            if tipo_user in pvulneraveis and perfil.need_acessibilidade():
                score+=40
            elif tipo_user in pvulneraveis:
                score+=25
            elif perfil.need_acessibilidade():
                score+=15
            else:
                score+=10
            
        elif ambiente.temp=="Risco Moderado.":
            if tipo_user in pvulneraveis and perfil.need_acessibilidade():
                score+=20
            elif tipo_user in pvulneraveis:
                score+=15
            elif perfil.need_acessibilidade():
                score+=5
            else:
                score-=0
                
        elif ambiente.temp=="Risco Ligeiro.":
            if tipo_user in pvulneraveis and perfil.need_acessibilidade():
                score+=15
            elif tipo_user in pvulneraveis:
                score+=10
            elif perfil.need_acessibilidade():
                score+=5
            else:
                score-=0


#____________Qualidade Ar____________________#

        if ambiente.qualidade_ar=="Risco Elevado":
            if tipo_user in pvulneraveis  and "problemas respiratórios" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=30
            elif tipo_user in pvulneraveis:
                score+=20
            elif "problemas respiratórios" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=25
            else:
                score+=10
                
        elif ambiente.qualidade_ar=="Risco Moderado":
            if tipo_user in pvulneraveis  and "problemas respiratórios" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=20
            elif tipo_user in pvulneraveis:
                score+=10
            elif "problemas respiratórios" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=15
            else:
                score+=5
                
        elif ambiente.qualidade_ar=="Boa":
            if tipo_user in pvulneraveis  and "problemas respiratórios" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=10
            elif tipo_user in pvulneraveis:
                score-=0
            elif "problemas respiratórios" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=5
            else:
                score-=0

#-------poluicao sonora---------------#
        if tipo_user in pvulneraveis and"Desconfortável" in ambiente.poluicao_sonora:
            score+=10

        elif "Desconfortàvel" in ambiente.poluicao_sonora:
            score+=5

        elif tipo_user in pvulneraveis and "Aceitável" in ambiente.poluicao_sonora:
            score+=5

        #Assumi que se o ambiente for aceitável e a pessoa for um adulto, não há stress
        
    
#------poluicao visual--------------#
        if "cego" in [inc.lower() for inc in perfil.get_incapacidades()] and ("Desconfortável" in ambiente.poluicao_visual or "Aceitável" in ambiente.poluicao_visual):
            pass # os cegos não se importam com poluição visual

        elif tipo_user in pvulneraveis and "Desconfortável" in ambiente.poluicao_visual:
            score+=10
        elif "Desconfortável" in ambiente.poluicao_visual:
            score+=5
        elif tipo_user in pvulneraveis and "Aceitável" in ambiente.poluicao_visual:
            score+=5
            #mesma coisa que na pol sonora

        
#----------Iluminação------------

        if ambiente.iluminacao=="Sem iluminação.":
            if tipo_user in pvulneraveis  and "cegos" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=20
            elif tipo_user in pvulneraveis:
                score+=15
            elif "cegos" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=15
            else:
                score+=10
                
        elif ambiente.iluminacao=="Fraco (Má visibilidade)":
            if tipo_user in pvulneraveis  and "cegos" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=15
            elif tipo_user in pvulneraveis:
                score+=10
            elif "cegos" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=10
            else:
                score+=5

                
        elif ambiente.iluminacao=="Iluminação Moderada":
            if tipo_user in pvulneraveis  and "cegos" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=10
            elif tipo_user in pvulneraveis:
                score+=5
            elif "cegos" in [inc.lower() for inc in perfil.get_incapacidades()]:
                score+=5
            else:
                score-=0
                
        
        
#------------sombra---------------#
#IMPORTANTE!!!!!!!
#@Renato
#não quero estar a mexer muito no que não fui eu a fazer, mas aqui vocês usaram coisas como ambiente.sombra1
#como se fossem variaveis, mas isso são métodos
#isto também está em outras partes do ficheiro, mas notei mais aqui

        if ambiente.sombra=="Sombra Reduzida":
            if ambiente.temp=="Risco Elevado." and tipo_user in pvulneraveis and perfil.need_acessibilidade():
                score+=35
            elif ambiente.temp=="Risco Elevado." and perfil.need_acessibilidade():
                score+=20 
            elif ambiente.temp=="Risco Elevado." and tipo_user in pvulneraveis :
                score+=25 
                
            elif ambiente.temp=="Risco Moderado." and tipo_user in pvulneraveis and perfil.need_acessibilidade():
                score+=25
            elif ambiente.temp=="Risco Moderado." and perfil.need_acessibilidade():
                score+=15
            elif ambiente.temp=="Risco Moderado." and tipo_user in pvulneraveis:
                score+=20
                 
            elif ambiente.temp=="Risco Ligeiro." and tipo_user in pvulneraveis and perfil.need_acessibilidade():
                score+=15
            elif ambiente.temp=="Risco Ligeiro." and perfil.need_acessibilidade():
                score+=10   
            elif ambiente.temp=="Risco Ligeiro." and tipo_user in pvulneraveis:
                score+=15
                
            else:
                score+=10
         
            
        
        elif ambiente.sombra=="Sombra Moderada":
            if ambiente.temp=="Risco Elevado." and tipo_user in pvulneraveis and perfil.need_acessibilidade():
                score+=25 
            elif ambiente.temp=="Risco Elevado." and perfil.need_acessibilidade():
                score+=15
            elif ambiente.temp=="Risco Elevado." and tipo_user in pvulneraveis :
                score+=20 
                
            elif ambiente.temp=="Risco Moderado." and tipo_user in pvulneraveis and perfil.need_acessibilidade():
                score+=20
            elif ambiente.temp=="Risco Moderado." and perfil.need_acessibilidade():
                score+=10
            elif ambiente.temp=="Risco Moderado." and tipo_user in pvulneraveis:
                score+=15
                 
            elif ambiente.temp=="Risco Ligeiro." and tipo_user in pvulneraveis and perfil.need_acessibilidade():
                score+=15
            elif ambiente.temp=="Risco Ligeiro." and perfil.need_acessibilidade():
                score+=5    
            elif ambiente.temp=="Risco Ligeiro." and tipo_user in pvulneraveis:
                score+=10
                
            else:
                score+=5
        
        
        return score 
