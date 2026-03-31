#------- 30/03/2026 ------ @Cláudia e @Inês ------------


# ----Dia 31/03/2026 @Inês --- Mensagens d

class Percurso:
    def __init__(self, nome, origem, destino):
        self.nome = nome
        self.origem = origem
        self.destino = destino

#-------------------------------------------------------------------------------------------------

#parâmetros de rua

class Rua(Percurso):
    def __init__(self, nome, origem, destino):
        super().__init__(nome, origem, destino)
        self.pavimento = None
        self.inclinacao = None
        self.passadeiras = None
        self.passeios = None
        self.textura_cego = None #ruas com textura no chão para guia de pessoas cegas
        self.escadas = None
        
    #as funções têm todas um underscore no seu nome para que não sejam baralhadas com o nome do atributo
    
    def pavimento_(self,rugosidade):
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
            print("Erro! Percentagens assumem valores entre 0 e 100.")


    def inclinacao_(self, declive):
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
            print("Erro! O declive deve tomar valores entre 0 e 1.")


    def passadeiras_(self, num, dist):
        #o mesmo número de passadeiras pode ser ótimo num percuso menor e péssimo num percurso maior
        #por isso, a distância (dist) vai dizer se o número de passadeiras (num) é aceitável, baixo ou elevado
        #distância está em metros
        if dist < 0 or num < 0:
            print("Erro. Distância negativa ou número de passadeiras negativo.")
        elif dist < 500:
            if num == 0:
                self.passadeiras = f"Baixo. {num} passadeiras."
            elif 0 < num <= 2:
                self.passadeiras = f"Moderado. {num} passadeiras."
            elif 2 < num :
                self.passadeiras =f"Elevado. {num} passadeiras."
        elif 500 <= dist < 1000:
            if num <= 2:
                self.passadeiras = f"Baixo. {num} passadeiras."
            elif 2 < num <= 5:
                self.passadeiras = f"Moderado. {num} passadeiras."
            elif 5 < num :
                self.passadeiras =f"Elevado. {num} passadeiras."
        elif 1000 <= dist < 1500:
            if num <= 4:
                self.passadeiras = f"Baixo. {num} passadeiras."
            elif 4 < num <= 8:
                self.passadeiras =f"Moderado. {num} passadeiras."
            elif 8 < num :
                self.passadeiras =f"Elevado. {num} passadeiras."
        elif 1500 <= dist < 2000:
            if num <= 6:
                self.passadeiras = f"Baixo. {num} passadeiras."
            elif 6 < num <= 10:
                self.passadeiras =f"Moderado. {num} passadeiras."
            elif 10 < num :
                self.passadeiras =f"Elevado. {num} passadeiras."
        elif 2000 <= dist < 2500:
            if num <= 8:
                self.passadeiras = f"Baixo. {num} passadeiras."
            elif 8 < num <= 12:
                self.passadeiras =f"Moderado. {num} passadeiras."
            elif 12 < num :
                self.passadeiras =f"Elevado. {num} passadeiras."
        elif 2500 <= dist < 3000:
            if num <= 10:
                self.passadeiras = f"Baixo. {num} passadeiras."
            elif 10 < num <= 14:
                self.passadeiras =f"Moderado. {num} passadeiras."
            elif 14 < num :
                self.passadeiras =f"Elevado. {num} passadeiras."
        elif dist >= 3000:
            if num <= 12:
                self.passadeiras = f"Baixo. {num} passadeiras."
            elif num > 12:
                self.passadeiras = f"Moderado. {num} passadeiras."
                
                
    def passeios_(self, perc):
        #a perc indica a percentagem do percurso que tem passeio ou local reservado a peões 
        #quanto mais alta a percentagem, mais passeio tem, melhor. 
        if 0 <= perc < 30:
            self.passeios = "Reduzido. Risco elevado."
        elif 30 <= perc < 60:
            self.passeios = "Moderado. Risco ligeiro."
        elif 60 <= perc <= 100:
            self.passeios = "Elevado. Risco reduzido."
        else:
            print("Erro! Percentagens assumem valores entre 0 e 100.")
            
            
    def textura_(self, tex):
        if tex == True:
            self.textura_cego = "O percurso dispõe de pavimento tátil, garantindo a orientação e segurança de pessoas com deficiência visual que utilizam bengala."
        else:
            self.textura_cego = "O percurso não inclui pavimento acessível a pessoas com incapacidade visual que usam bengala."
            
        
    def escadas_(self,esc):
        if esc == True:
            self.escadas = "O percurso inclui escadas."
        else:
            self.escadas = "O percurso não inclui escadas."
            
            
#-----------------------------------------------------------------------------------------

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
        self.sombra= None

    def temp(self, temperatura):
        if 0 <= temperatura <15:
            self.temperatura = "Desconforto Ligeiro."
        elif 15<=temperatura<=24:
            self.temperatura= "Ideal."
        elif 25<=temperatura<=30 or 10<=temperatura<=17:
            self.temperatura= "Desconforto Ligeiro."
        elif temperatura<=10 or 30<=temperatura:
            self.temperatura= "Risco Moderado."
        else:
            self.temperatura= "Risco Elevado."


    def percqualidade_ar(self, perc_qualidade_ar):
        #perc_qualidade_ar: 100% é ar puro,_ 0% é ar extremamente poluído.
        if 100>=perc_qualidade_ar >=80:
            self.qualidade_ar= "Excelente"
        elif 50<=perc_qualidade_ar<80:
            self.qualidade_ar= "Boa"
        elif 20<=perc_qualidade_ar<50:
            self.qualidade_ar= "Risco Moderado"
        elif 0<=perc_qualidade_ar<20:
            self.qualidade_ar= "Risco Elevado"
        else:
            print("Erro! Percentagens assumem valores entre 0 e 100.")
        
    def poluison(self, poluicaosonora):
        #poluison: 0% (silêncio/natureza), 100% ruído ensurdecedor
        if 0<=poluicaosonora<30:
            self.poluicao_sonora= "Ideal"
        elif 30<=poluicaosonora<70:
            self.poluicao_sonora= "Aceitável"
        elif 70<=poluicaosonora<=100:
            self.poluicao_sonora= "Desconfortável"
        else:
            print("Erro! Percentagens assumem valores entre 0 e 100.")


    def puluivisu(self, poluicaovisual):
        if poluicaovisual<30:
            self.poluicao_visual= "Ideal"
        elif 30<=poluicaovisual<60:
            self.poluicao_visual= "Aceitável"
        elif 60<=poluicaovisual<=100:
            self.poluicao_visual= "Desconfortável"
        else:
            print("Erro! Percentagens assumem valores entre 0 e 100.")
        
        
    def nivelpolen(self, polen):
        #ar limpo (sem polen) 0%, ar com polen 100%
        if 0<polen<=15:
            self.nivel_polen= "Ideal. Ar limpo."
        elif 15<polen<=40:
            self.nivel_polen= "Risco Ligeiro"
        elif 40<polen<=70:
            self.nivel_polen= "Risco Moderado"
        elif 70<polen<=100:
            self.nivel_polen= "Risco Elevado"
        else:
            print("Erro! Percentagens assumem valores entre 0 e 100.")
            

    
    def ilumina(self, numpostes, hora, dist):
        
        dia = hora <= 20 or hora >= 7
        if dia:
            self.iluminacao= "Ótima"
        else:
            if numpostes==0:
                self.iluminacao= "Iluminação reduzida."
            else:
                metros_por_poste= dist/numpostes

            if 0<metros_por_poste<=30:
                self.iluminacao="Excelente"
            elif 30< metros_por_poste<= 60:
                self.iluminacao= "Iluminação Moderada"
            elif 60< metros_por_poste<= 100:
                self.iluminacaoo="Fraco (Má visibilidade)"
            else:
                print("Erro! Percentagens assumem valores entre 0 e 100.")
                
    
    def sombra1(self, nsombra):
        if 0<=nsombra<30:
            self.sombra= "Sombra reduzida"
        elif 30<=nsombra<60:
            self.sombra= "Sombra moderada"
        elif 60<=nsombra<100:
            self.sombra= "Sombra abragente"
        else:
            print("Erro! Percentagens assumem valores entre 0 e 100.")
    
    def sombra2(self, nsombra, dist):
        perc_cobertura= (nsombra/dist)*100
        if 0<=perc_cobertura<30:
            self.sombra= " Sombra reduzida"
        elif 30<=perc_cobertura<60:
            self.sombra= "Sombra moderada"
        elif 60<=perc_cobertura<=100:
            self.sombra= "Sombra abragente"
        else:
            print("Erro! Percentagens assumem valores entre 0 e 100.")
    
    
#-------------------------------------------------------------------------------------------

#parâmetros de população

class ParametrosPopulacao(Percurso):
    def __init__(self, nome, origem, destino):
        super().__init__(nome, origem, destino)
        self.transito = None
        self.multidao = None
        
    #nestas funções a condiçaõ de True ou False vai atualizar o atributo. Se há trânsito ou não, se há multidão ou não...
    def transito_(self,res):
        if res == True:
            self.transito = "No percurso selecionado, a probabilidade de interseção com tráfego automóvel é elevada."
        else:
            self.transito = "No percurso selecionado, a probabilidade de interseção com tráfego automóvel é reduzida."
    
    def multidao_(self,res):
        if res == True:
            self.multidao = "Zona de elevada afluência de peões."
        else:
            self.multidao = "Zona de reduzida afluência de peões."


                


                
