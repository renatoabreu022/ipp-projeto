#-----Dia 30/03/2006--@Lucas@Renato-------#

#----- Dia 29/04/2026---@Claudia
 
#----------------------------------#
#tipo = string
#alergias = list
#incapacidades = list

#___________imports_______________#
import json
import hashlib
#_________________________________#

class Perfil:
    
    def __init__(self,tipo,alergias=None,incapacidades=None):
        self.__tipo = tipo #idoso,adulto,jovem,...
        self.__alergias = alergias if alergias is not None else []
        self.__incapacidades = incapacidades if incapacidades is not None else []
    
    # ---METODOS GET---
    
    def get_tipo(self):
        return self.__tipo
    
    def get_alergias(self):
        return list(self.__alergias)
    
    def get_incapacidades(self):
        return list(self.__incapacidades)
    
    # ---METODOS DE MANIPULAÇÃO---

    def add_alergia(self,alergia):
        if alergia not in self.__alergias:
            self.__alergias.append(alergia)
        
    def remove_alergia(self,alergia):
        if alergia in self.__alergias:
            self.__alergias.remove(alergia)
    
    def add_incapacidade(self,incapacidade):
        if incapacidade not in self.__incapacidades:
            self.__incapacidades.append(incapacidade)
    
    def remove_incapacidade(self,incapacidade):
        if incapacidade in self.__incapacidades:
            self.__incapacidades.remove(incapacidade)
    
    # ---METODOS DE VERIFICAÇÃO---
    
    def has_alergia(self,alergia):
        return alergia in self.__alergias
    
    def has_incapacidade(self,incapacidade):
        return incapacidade in self.__incapacidades
    
    def need_acessibilidade(self):
        # verifica se a pessoa necessita de meios mais acessiveis
        return 'mobilidade' in self.__tipo or 'cadeira' in self.__tipo or 'muletas' in self.__tipo
    
    def not_ruido(self):
        # verifica se a pessoa quer evitar ruido
        return 'hipersensibilidade' in self.__incapacidades
    
    # ---REPRESENTAÇÃO---
    
    def __str__(self):
        alergias = ", ".join(self.__alergias) if self.__alergias else "Nenhuma"
        incapacidades = ", ".join(self.__incapacidades) if self.__incapacidades else "Nenhuma"

        return (
            f"Perfil do utilizador:\n"
            f"- Tipo: {self.__tipo}\n"
            f"- Alergias: {alergias}\n"
            f"- Incapacidades: {incapacidades}"
        )

#----------------------------------#~
def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest() #encriptação da palavra passe

class Utilizador: #--Permite dar login na app, introduz cerednciais e retorna informações---#

    def __init__(self,username,password,perfil: Perfil):
        self.__username=username
        self.__password=hash_password(password)
        self.__perfil=perfil

    @property
    def u_username(self):
        return self.__username # devolve o username

    @property
    def u_perfil(self): #devolve perfil do utilizador
        return self.__perfil
    
    @property
    def u_password(self):
        return self.__password # devolve password encriptada
    
    def verifica_credenciais(self,In_user,In_pass): #verifica se o input do utilizador coincide com as suas credenciais
        return self.__username == In_user and self.__password == hash_password(In_pass)
    
    def __str__(self):
        return f"O utlizador de username {self.__username} tem o seguinte perfil: {self.__perfil}"


#--------------------------------------------------------#

class Sistema:
    def __init__(self):
        self._users=[]

    def cria_username(self,new_username): # Verifica se já há um username existente
        valido = True
        i = 0
        while valido and i < len(self._users):
            if self._users[i].u_username == new_username:
                print("Username já existente. Por favor, crie um novo.")
                valido = False                                          # Se já existir um username igual, retorna falso
            i +=1
        if valido:
            print("Username válido")
        return valido        #Se valido for True, dá para usar o username. Se for falso, não está válido
        
            
    def add_user(self,user:Utilizador): # Adiciona um novo utilizador ao sistem
        self._users.append(user)

    def login(self,Inusername,Inpassword):
        found = False
        i = 0
        permission = False

        while not found and i <len(self._users):
            if self._users[i].u_username == Inusername:
                found = True                       #verifica username

                if self._users[i].verifica_credenciais(Inusername,Inpassword):  # verifica password
                    permission = True

            i += 1

        if not found:
            print("Username não encontrado.")

        elif not permission: # @Renato - coloquei elif porque quando não encontra o user, basta mostrar 1 mensagem de erro
            print("Password inválida.")
            
        return permission # Dá a ordem de seguir se as credenciais estiverem corretas
    
    def remove_user(self,user):
        for u in self._users:
            if u.u_username == user.u_username:  # retira um usuário já logado da aplicação da lista de users se quiser apagar o perfil
                self._users.remove(u)

        return self._users

    def save_users(self,file):
        save = {}
        for user in self._users:
            perfil = user.u_perfil
            save[user.u_username] ={"pass":user.u_password,"perfil":{"tipo":perfil.get_tipo(),"alergias":perfil.get_alergias(),"incapacidades":perfil.get_incapacidades()}}
        with open(file + ".json","w", encoding="utf-8") as f:
            json.dump(save,f,indent = 4)

    def load_users(self, file):
        try:
            with open(file + ".json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self._users = []
            for username, info in data.items():
                dados_p = info["perfil"]
                #Criamos o objeto Perfil com os dados do JSON
                u_perfil = Perfil(dados_p["tipo"], dados_p["alergias"], dados_p["incapacidades"])

                #Criamos o Utilizador. 
                novo_user = Utilizador(username, "_", u_perfil)

                #Substituímos a password placeholder pelo hash real que estava no ficheiro
                novo_user._Utilizador__password = info["pass"]

                self._users.append(novo_user)

            print(f"Foram carregados {len(self._users)} utilizadores")
            return self._users
        except FileNotFoundError:
            print("Ficheiro não encontrado. Começar com a lista vazia")
            return [] # Retornar lista vazia em vez de dicionário para manter a consistência
        

    def select_incapacidades(self, user):
        incapacidades = ["respiratória","cego","surdo","mobilidade reduzida","cadeira de rodas","grávida","hipersensibilidade","outro"]
        lista_select={num:inc for num,inc in list(enumerate(incapacidades))}
        
        select=input("Selecione as incapacidades do utilizador (separadas por vírgula):\n" + "\n".join([f"{num}: {inc}" for num, inc in lista_select.items()]) + "\n")
        select = select.split(",")
        for num in select:
            num = num.strip()
            if num.isdigit() and int(num) in lista_select:
                user.u_perfil.add_incapacidade(lista_select[int(num)])
            else:
                print(f"Seleção inválida: {num}")


    def select_alergias(self, user):
        alergias = ["pólen"]
        lista_selct={num:al for num,al in list(enumerate(alergias))}

        selct=input("Selecione as alergias do utilizador (separadas por vírgula):\n" + "\n".join([f"{num}: {al}" for num, al in lista_selct.items()]) + "\n")
        selct = selct.split(",")
        for num in selct:
            num = num.strip()
            if num.isdigit() and int(num) in lista_selct:
                user.u_perfil.add_alergia(lista_selct[int(num)])
            else:
                print(f"Seleção inválida: {num}")
                

#-------- nova maneira de "perfil"----------
class Preferencias:
    def __init__(self):
        self.parametros={
            #parâmetros de acessibilidade
            "pavimento" : 5,
            "inclinacao" : 5,
            "passadeiras" : 5,
            "passeios" : 5,
            "textura_cego" : 5,
            "escadas" : 5,
            #parâmetros de ambiente
            "temperatura" : 5, 
            "qualidade_ar" : 5,
            "poluicao_sonora" : 5,
            "poluicao_visual" : 5,
            "nivel_polen" : 5,
            "iluminação" : 5,
            "sombra" : 5, 
            #parâmetros de população
            "transito" : 5,
            "multidao" : 5
        }
        
    #escolher o peso de cada parâmetro
    #ACESSIBILIDADE
    @property
    def peso_pavimento(self):
        return self.parametros["pavimento"]

    @property
    def peso_inclinacao(self):
        return self.parametros["inclinacao"]

    @property
    def peso_passadeiras(self):
        return self.parametros["passadeiras"]

    @property
    def peso_passeios(self):
        return self.parametros["passeios"]

    @property
    def peso_textura_cego(self):
        return self.parametros["textura_cego"]

    @property
    def peso_escadas(self):
        return self.parametros["escadas"]

    #AMBIENTE
    @property
    def peso_temperatura(self):
        return self.parametros["temperatura"]

    @property
    def peso_ar(self):
        return self.parametros["qualidade_ar"]

    @property
    def peso_ruido(self):
        return self.parametros["poluicao_sonora"]

    @property
    def peso_visual(self):
        return self.parametros["poluicao_visual"]

    @property
    def peso_polen(self):
        return self.parametros["nivel_polen"]

    @property
    def peso_iluminacao(self):
        return self.parametros["iluminacao"]

    @property
    def peso_sombra(self):
        return self.parametros["sombra"]

    #POPULAÇÃO
    @property
    def peso_transito(self):
        return self.parametros["transito"]

    @property
    def peso_multidao(self):
        return self.parametros["multidao"]
    
    def forms_pref(self):
        print("""De maneira a optimizarmos o processo de escolha do melhor percurso, 
            responda ao seguinte questionário sobre a relevância que dá aos parâmetros. """)
        print("""As respostas devem ser entre 0 e 10. Sendo 0 : Pouco Relevante e 10 : Muito Relevante""")
        
        for chave in self.parametros.keys():
            while True:
                try:
                    valor = int(input(f"Qual a relevância de {chave.replace('_', ' ')}? "))
                    if 0 <= valor <= 10:
                        self.parametros[chave] = valor
                        break
                    print("Por favor, insira um valor entre 0 e 10.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")
                    
    def get_dict(self):
        return self._parametros
        