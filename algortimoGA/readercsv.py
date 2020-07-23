import csv
from settings_global.setting_global import SERVER_DIRECTORY_SAVE
from util import RandomHash
from models import Horario,Discipline,Classes
class ImportCsv(object):
    def __init__(self):
        pass
    def readerHorario(self,name):
        self.path = SERVER_DIRECTORY_SAVE+"/"+name
        list_horarios = []
        with open(self.path,'r') as arquivo_csv:
            reader = csv.reader(arquivo_csv, delimiter=",")
            for coluna in reader:
                if coluna[0] == "id" and coluna[1] == "codigo" and coluna[2]=="sequencia":
                    pass
                else:
                    list_horarios.append(Horario(coluna[0],coluna[1],coluna[2]))
        
        return list_horarios
    
    def readerDisciplina(self,name):
        self.path = SERVER_DIRECTORY_SAVE+"/"+name
        list_disciplinas = []
        with open(self.path, 'r') as arquivo_csv:
            reader = csv.reader(arquivo_csv, delimiter=',')
            for coluna in reader:
                if coluna[0] =="id" and coluna[1] =="periodo" and coluna[2] =="credito" and coluna[3] == "professor" and coluna[4] == "nome" and coluna[5] == "curso":
                    pass
                else:
                    split = coluna[5].split("/")
                    if len(split)>1: #name,curso,periodo,id,credito,professor,list_classes
                        disp1 = Discipline(coluna[4],split[0],coluna[1],coluna[0],coluna[2],coluna[3],None)
                        #print(disp1.name,disp1.curso,disp1.periodo,disp1.credito,disp1.professor)
                        disp2 = Discipline(coluna[4],split[1],coluna[1],coluna[0],coluna[2],coluna[3],None)
                        list_disciplinas.append(disp1)
                        list_disciplinas.append(disp2)
                    else:
                        disp1 = Discipline(coluna[4],coluna[5],coluna[1],coluna[0],coluna[2],coluna[3],None)
                        list_disciplinas.append(disp1)
            return list_disciplinas
    def readerSala(self,name):
        self.path = SERVER_DIRECTORY_SAVE+"/"+name
        lista_salas =[]
        with open(self.path, 'r') as arquivo_csv:
            reader = csv.reader(arquivo_csv, delimiter=',')
            for coluna in reader:
                if coluna[0] =="codigo" and coluna[1] == "capacidade":
                    pass
                else:
                    sala = Classes(RandomHash.gerator_id(), coluna[0], coluna[1])
                    lista_salas.append(sala)
        return lista_salas
