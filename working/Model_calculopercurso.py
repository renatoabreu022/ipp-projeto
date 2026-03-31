#------------31/03/2026-------@Lucas@Inês------------------#

#____________imports______________#
from user.py import Perfil
from percursos.py import Rua, ParametrosAmbiente

class MotorCalculo:

    @staticmethod
    def calcular_IC(perfil:Perfil,rua:Rua,ambiente:ParametrosAmbiente): #IC-> Indice de conforto, serve para calcular o conforto do percurso, quanto mais próximo de 1 melhor
        score = 100

        if perfil.need_acessibilidade() and "inclui_escadas" in rua.escadas:
            score-=50

        elif perfil.need_acessibilidade() and ""


    
        

















    
    