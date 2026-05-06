#-----Dia 30/03/2006--@Lucas@Renato-------#

#----- Dia 29/04/2026---@Claudia
 
#----- Dia 03/05/2026----- @Cláudia
#----------------------------------#
#tipo = string
#alergias = list
#incapacidades = list

#___________imports_______________#
import json
import hashlib
#_________________________________#


#----------------------------------#~
def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest() #encriptação da palavra passe
    

class Utilizador: #--Permite dar login na app, introduz cerednciais e retorna informações---#

    def __init__(self,username,password,preferencias=None):
        self.__username=username
        #if is_hash: # @Renato 3/05 -- não está definido
            #self.__password = password
        #else:
            #self.__password = hash_password(password)
            
        self.__preferencias = preferencias if preferencias else Preferencias()
        self.__preferencias = preferencias if preferencias else Preferencias()

    @property
    def u_username(self):
        return self.__username # devolve o username
    
    @property
    def u_preferencias(self):
        return self.__preferencias

    @property
    def u_password(self):
        return self.__password # devolve password encriptada
    
    def verifica_credenciais(self,In_user,In_pass): #verifica se o input do utilizador coincide com as suas credenciais
        return self.__username == In_user and self.__password == hash_password(In_pass)
    
    def alterar_password(self, nova_password):
        self.__password = hash_password(nova_password)
    
    def __str__(self):
        return f"O utlizador de username {self.__username}."


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

    def save_users(self, file):
        save = {}
        for user in self._users:
            save[user.u_username] = {
                "pass": user.u_password,
                "preferencias": user.u_preferencias.get_dict() #Salva apenas o dicionário de números
            }
        with open(file + ".json", "w", encoding="utf-8") as f:
            json.dump(save, f, indent=4)
            
            
    #def load_users(self, file):
        #try:
            #with open(file + ".json", "r", encoding="utf-8") as f:
                #data = json.load(f)
            
            #self._users = []
            #for username, info in data.items():
                
                #Criamos o objeto Perfil com os dados do JSON
                #u_prefs = Preferencias()
                #if "preferencias" in info:
                    #u_prefs.atualizar_parametros(info["preferencias"]) #este método não está nas preferencias @Renato 3/05

                #Criamos o utilizador com as suas preferências carregadas
                #novo_user = Utilizador(username, "_", u_prefs)
                #Repomos a password encriptada que estava no ficheiro
                #novo_user._Utilizador__password = info["pass"]
                
                #self._users.append(novo_user)

            #print(f"Foram carregados {len(self._users)} utilizadores.")
            #return self._users
        #except FileNotFoundError:
            #print("Ficheiro não encontrado. Começar com a lista vazia.")
            #return []



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
            "iluminacao" : 5,
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
        return self.parametros
        