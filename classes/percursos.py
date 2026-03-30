class Percurso:
    def __init__(self, nome, origem, destino):
        self.nome = nome
        self.origem = origem
        self.destino = destino

#-----------------------------------------------------------------------------------------
class Rua(Percurso):
    def __init__(self, nome, origem, destino):
        super().__init__(nome, origem, destino)
        #parâmetros de rua
        self.pavimento = None
        self.inclinacao = None
        self.passadeiras = None
        self.passeios = None
        self.textura_cego = None #ruas com textura no chão para guia de pessoas cegas
        self.escadas = None
        
    
    def pavimento(self,rugosidade):
        #em termos de percentagem
        if 0 <= rugosidade < 30:
            self.pavimento = "Pavimento Regular"
        elif 30 <= rugosidade < 50:
            self.pavimento = "Pavimento Ligeiramente Irregular"
        elif 50 <= rugosidade < 70:
            self.pavimento = "Pavimento Irregular"
        elif 70 <= rugosidade <= 100:
            self.pavimento = "Pavimento Muito Irregular"
        else: 
            print("Erro: A rugosidade do percurso é um índice. Deve estar em percnetagem (0-100)")

    def inclinacao(self, declive):
        #o declive é um valor entre 0 e 1. 1 corresponde a um declive muito acentuado. 0 correspinde a um declive nulo, ou seja, rua plana.
        if 0 <= declive < 0.3:
            self.inclinacao = "Nível Baixo" #rua plana
        elif 0.3 <= declive < 0.5:
            self.inclinacao = "Nível Moderado"
        elif 0.5 <= declive < 0.7:
            self.inclinacao = "Nível Elevado"
        elif 0.7 <= declive <= 1:
            self.inclinacao = "Nível Muito Elevado" #rua muito inclinada
        else:
            print("O declive deve tomar valores entre 0 e 1.")


    def passadeiras(self, num, dist):
        #o mesmo número de passadeiras pode ser ótimo num percuso menor e péssimo num percurso maior
        #por isso, a distância (dist) vai dizer se o número de passadeiras (num) é aceitável, baixo ou elevado
        #distância está em metros
        if dist < 500:
            if num == 0:
                self.passadeiras ="Baixo"
            elif 0 < num <= 2:
                self.passadeiras ="Moderado"
            elif 2 < num :
                self.passadeiras ="Elevado"
        elif 500 <= dist < 1000:
            if num <= 2:
                self.passadeiras ="Baixo"
            elif 2 < num <= 5:
                self.passadeiras ="Moderado"
            elif 5 < num :
                self.passadeiras ="Elevado"
        elif 1000 <= dist < 1500:
            if num <= 2:
                self.passadeiras ="Baixo"
            elif 2 < num <= 5:
                self.passadeiras ="Moderado"
            elif 5 < num :
                self.passadeiras ="Elevado"


#--------------------------------------------------------------------------------

#parâmetros de ambiente
class ParametrosAmbiente(Percurso):
    def __init__(self,nome, origem, destino):
        super().__init__(nome, origem, destino)
        self.temperatura= None
        self.qualidade_ar= None
        self.poluicao_sonora= None
        self.poluicao_visual= None
        self.nivel_polen= None       #Pode ser em percentagem ou em True or False
        self.iluminacao= None

    def percqualidade_ar(self, perc_qualidade_ar):
        #perc_qualidade_ar: 100% é ar puro,_ 0% é ar extremamente poluído.
        if perc_qualidade_ar >=80:
            self.qualidade_ar= "Excelente"
        elif 50<=perc_qualidade_ar<80:
            self.qualidade_ar= "Bom"
        elif 20<=perc_qualidade_ar<50:
            self.qualidade_ar= "Mau"
        else:
            self.qualidade_ar= "Péssimo"
        
    def poluison(self, poluicaosonora):
        

        if poluicaosonora<=50:
            self.poluicao_sonora= "Terrível"
        elif 50<poluicao_sonora


    
#parâmetros de população
class ParametrosPopulacao(Percurso):
    def __init__(self, nome, origem, destino):
        super().__init__(nome, origem, destino)
        self.transito = None
        self.multidao = None
        