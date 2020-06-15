
from sockets.sockets_hand import quickstart
from geradores.geratordata import getInstance
from models.discipline import Discipline
from models.horario import Horario
from models.classes import Classes
from models.enumeration import HorarioE
from random import random as rd
import random
from util import RandomHash

class GEntitys(object):
    def __init__(self,data_set_disciplines,data_set_horarios,data_set_salas):
        self.data_set_disciplines=data_set_disciplines
        self.data_set_horarios=data_set_horarios
        self.data_set_salas=data_set_salas
    
    def splitter(self,curso):
        q = curso.split("/")
        if len(q) > 1:
            return q
        return None
    def Gdisciplines(self):
        T = []
        for i in range(len(self.data_set_disciplines)):
            if self.data_set_disciplines[i]["id"] != "":
                q = self.splitter(self.data_set_disciplines[i]["curso"])
                if q!=None:
                    disp1 = Discipline(self.data_set_disciplines[i]["nome"],q[0],self.data_set_disciplines[i]["periodo"],self.data_set_disciplines[i]["id"],self.data_set_disciplines[i]['credito'],self.data_set_disciplines[i]['professor'],None)
                    disp2 = Discipline(self.data_set_disciplines[i]["nome"],q[1],self.data_set_disciplines[i]["periodo"],self.data_set_disciplines[i]["id"],self.data_set_disciplines[i]['credito'],self.data_set_disciplines[i]['professor'],None)
                    T.append(disp1)
                    T.append(disp2)
                else:
                    T.append(Discipline(self.data_set_disciplines[i]["nome"],self.data_set_disciplines[i]["curso"],self.data_set_disciplines[i]["periodo"],self.data_set_disciplines[i]["id"],self.data_set_disciplines[i]['credito'],self.data_set_disciplines[i]['professor'],None))
            else:
                if q!=None:
                    disp1 = Discipline(self.data_set_disciplines[i]["nome"],q[0],self.data_set_disciplines[i]["periodo"],RandomHash.gerator_id(),self.data_set_disciplines[i]['credito'],self.data_set_disciplines[i]['professor'],None)
                    disp2 = Discipline(self.data_set_disciplines[i]["nome"],q[1],self.data_set_disciplines[i]["periodo"],RandomHash.gerator_id(),self.data_set_disciplines[i]['credito'],self.data_set_disciplines[i]['professor'],None)
                    T.append(disp1)
                    T.append(disp2)
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
    
    def GCromosome(self,gDataDiscipline):
        pass

def entitys():
    return GEntitys(getInstance().get_data_disciplines(),getInstance().get_data_horarios(),getInstance().get_data_salas())



qnt_aulas_disciplina = 2

dt_discipline = entitys().Gdisciplines()
dt_horario = entitys().Ghorarios()
dt_salas = entitys().GSalas()



salas = dt_salas.get('Tdata')
disciplinas = dt_discipline.get('Tdata')
horarios = dt_horario.get('Tdata')
tamanho_salas = len(salas)

class GeradorObject(object):

    @staticmethod
    def generate_horarios_by_sala(qnt_aulas_disciplina,salas,horarios):
        dList=[]
        for i in range(qnt_aulas_disciplina):
            aux = random.randint(0,len(salas)-1)
            dList.append(horarios[aux])
        return dList
    
    @staticmethod
    def generate_sala_by_discipline(qnt_aulas_disciplina,salas,horarios):
        dList=[]
        horarios_ = GeradorObject.generate_horarios_by_sala(qnt_aulas_disciplina,salas,horarios)
        for i in range(qnt_aulas_disciplina):
            aux = random.randint(0,len(salas)-1)
            dList.append(salas[aux])
        for i in dList:
            i.horario = horarios_
        return dList

    @staticmethod
    def generate_disciplines():
        list_set = []
        salasx = random.sample(salas,len(salas))
        disciplinasx = random.sample(disciplinas,len(disciplinas))
        horariosx = random.sample(horarios,len(horarios))
        for i in range(len(disciplinasx)):
            disciplinas[i].list_classes = GeradorObject.generate_sala_by_discipline(qnt_aulas_disciplina,salasx,horariosx)
            #print(len(disciplinas[i].list_classes))
            list_set.append(disciplinas[i])
        return random.sample(list_set,len(list_set))


