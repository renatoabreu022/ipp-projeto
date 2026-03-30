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
            if num <= 4:
                self.passadeiras ="Baixo"
            elif 4 < num <= 8:
                self.passadeiras ="Moderado"
            elif 8 < num :
                self.passadeiras ="Elevado"
        elif 1500 <= dist < 2000:
            if num <= 6:
                self.passadeiras ="Baixo"
            elif 6 < num <= 10:
                self.passadeiras ="Moderado"
            elif 10 < num :
                self.passadeiras ="Elevado"
        elif 2000 <= dist < 2500:
            if num <= 8:
                self.passadeiras ="Baixo"
            elif 8 < num <= 12:
                self.passadeiras ="Moderado"
            elif 12 < num :
                self.passadeiras ="Elevado"
        elif 2500 <= dist < 3000:
            if num <= 10:
                self.passadeiras ="Baixo"
            elif 10 < num <= 14:
                self.passadeiras ="Moderado"
            elif 14 < num :
                self.passadeiras ="Elevado"
        elif dist >= 3000:
            if num <= 12:
                self.passadeiras = "Baixo"
            elif num > 12:
                self.passadeiras = "Aceitável"
        elif dist < 0


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

    def temp(self, temperatura):
        if 18<=temperatura<=24:
            self.temperatura

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
        #poluison: 0% (silêncio/natureza), 100% ruído ensurdecedor
        if poluicaosonora<50:
            self.poluicao_sonora= "Terrível"
        elif 50<=poluicaosonora<80:
            self.poluicao_sonora= "Aceitável"
        else:
            self.poluicao_sonora= "Ideal"


    def puluivisu (self, poluicaovisual):
        

        
#parâmetros de população
class ParametrosPopulacao(Percurso):
    def __init__(self, nome, origem, destino):
        super().__init__(nome, origem, destino)
        self.transito = None
        self.multidao = None
        