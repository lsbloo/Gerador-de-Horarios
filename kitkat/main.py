from sockets.sockets_hand import quickstart
from geradores.geratordata import getInstance
from models.discipline import Discipline
from models.horario import Horario
from models.classes import Classes
from models.enumeration import HorarioE
import random


#quickstart()


class RandomHash(object):
    @staticmethod
    def gerator_id():
        return random.getrandbits(128)

class GEntitys(object):
    def __init__(self,data_set_disciplines,data_set_horarios,data_set_salas):
        self.data_set_disciplines=data_set_disciplines
        self.data_set_horarios=data_set_horarios
        self.data_set_salas=data_set_salas
    
    def Gdisciplines(self):
        T = []
        for i in range(len(self.data_set_disciplines)):
            if self.data_set_disciplines[i]["id"] != "":
                T.append(Discipline(self.data_set_disciplines[i]["nome"],self.data_set_disciplines[i]["curso"],self.data_set_disciplines[i]["periodo"],self.data_set_disciplines[i]["id"],self.data_set_disciplines[i]['credito'],self.data_set_disciplines[i]['professor'],None))
            else:
                T.append(Discipline(self.data_set_disciplines[i]["nome"],self.data_set_disciplines[i]["curso"],self.data_set_disciplines[i]["periodo"],RandomHash.gerator_id(),self.data_set_disciplines[i]['credito'],self.data_set_disciplines[i]['professor'],None))

        return {
            "Tlen" : len(T), "Tdata": T 
        }
    def Ghorarios(self):
        T = []
        for i in range(len(self.data_set_horarios)):
            D = list(HorarioE)
            for name in D:
                if int(self.data_set_horarios[i]["id"]) == name.value:
                    T.append(Horario(name.name,self.data_set_horarios[i]["codigo"],self.data_set_horarios[i]["sequencia"]))
        return {
            "Tlen": len(T) , "Tdata": T
        }
    def GSalas(self):
        T = []
        for i in range(len(self.data_set_salas)):
            T.append(Classes(self.data_set_salas[i]["id"], self.data_set_salas[i]["codigo"], self.data_set_salas[i]["capacidade"]))
        
        return {
            "Tlen": len(T), "Tdata": T
        }

def entitys():
    return GEntitys(getInstance().get_data_disciplines(),getInstance().get_data_horarios(),getInstance().get_data_salas())







