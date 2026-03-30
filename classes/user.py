#-----Dia 30/03/2006--@Lucas@Renato-------#

#----------------------------------#
#tipo = string
#alergias = list
#incapacidades = list
import json

class Perfil:
    
    def __init__(self,tipo,alergias=[],incapacidades=[]):
        self.__tipo = tipo #idoso,adulto,jovem,...
        self.__alergias = alergias
        self.__incapacidades = incapacidades
    
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

#----------------------------------#
class Utilizador: #--Permite dar login na app, introduz cerednciais e retorna informações---#

    def __init__(self,username,password,perfil: Perfil):
        self.__username=username
        self.__password=password
        self.__perfil=perfil

    @property
    def username(self):
        return self.__username
    
    @property
    def password(self):
        return self.__password
    
    def verifica_credenciais(self,In_user,In_pass): #verifica se o input do utilizador coincide com as suas credenciais
        return self.__username == In_user and self.__password == In_pass
    
    def get_perfil(self): #devolve perfil do utilizador
        return self.__perfil
    
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
            if self._users[i].get_username == new_username:
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

                if self._users[i].u_password==Inpassword: # verifica password
                    permission = True

            i += 1

        if not found:
            print("Username não encontrado.")

        if not permission:
            print("Password inválida.")
            
        return permission # Dá a ordem de seguir se as credenciais estiverem corretas

    def save_users(self):
        save = {}
        for user in self._users:
            if user.u_username not in save:
                save[user.u_username] = {"pass"=user.u_password,"perfil"=user.u_perfil}

        json.load(save)