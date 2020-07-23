
from readerJson import getInstance
from models import Discipline
from models import Horario
from models import Classes
from enumeration import HorarioE
from random import random as rd
import random
from util import RandomHash
import json
from collections import Counter
from helper import helpy
class GEntitys(object):
    def __init__(self,data_set_disciplines,data_set_horarios,data_set_salas):
        if data_set_disciplines != None and data_set_horarios != None and data_set_salas != None:
            self.data_set_disciplines=data_set_disciplines
            self.data_set_horarios=data_set_horarios
            self.data_set_salas=data_set_salas
        else:
            print()
            print('Realize a importação dos arquivos')
            print()
            helpy()
            quit()
    
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
                q = self.splitter(self.data_set_disciplines[i]["curso"])
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
            T.append(Classes(RandomHash.gerator_id(), self.data_set_salas[i]["codigo"], self.data_set_salas[i]["capacidade"]))
        return {
            "Tlen": len(T), "Tdata": T
        }
    
    def GCromosome(self,gDataDiscipline):
        pass

def entitys():
    return GEntitys(getInstance().get_data_disciplines(),getInstance().get_data_horarios(),getInstance().get_data_salas())



dt_discipline = entitys().Gdisciplines()
dt_horario = entitys().Ghorarios()

dt_salas = entitys().GSalas()



salas = dt_salas.get('Tdata')
disciplinas = dt_discipline.get('Tdata')
horarios = dt_horario.get('Tdata')
tamanho_salas = len(salas)

from copy import deepcopy
variavel_global = []

class GeradorObject(object):

    """
        Realiza o processo de recriação das disciplinas de acordo com o array de individuos.(solução)
        esta função recupera o array de individuos e o desfragmenta em sub-pacotes de horarios.
        Utiliza metodos auxiliares para fazer a recriação dos horarios e atribui-los novamente
        em uma disciplina especificada aqui pelo indice. Exemplo:
        Disciplina[Introdução a programação] indice = 0 List Disciplines
        contém duas aulas se a variavel QUANTIDADE_AULAS_POR_DISCIPLINA FOR IGUAL = 2
        desta forma, o indice zero do sub-pacote de horarios corresponde a o indice 0 da disciplina em questão,
        os elementos do sub pacote são os indices da minha enumeration de horarios, no qual é feito uma troca.

        Esta operação de troca de horarios denominados aqui de gene é feita recursivamente até que a condição de parada seja satisfeita.
    """
    @staticmethod
    def recreateDisciplines(disciplines, dList, individual,QUANTIDADE_AULAS_POR_DISCIPLINA):
        horarios_depois_da_recriacao = []
        counter = -1
        horarios_antes_da_recriacao = []
        for disciplina in disciplines:
            for aulas in disciplina.list_classes:
                counter+=1
                horarios_antes_da_recriacao.append(aulas.horario.id)
                horarios_depois_da_recriacao.append(dList[individual[counter]])
        new_disp =[]
        #print(horarios_depois_da_recriacao)
        dt = deepcopy(disciplines)
        for i in range(len(dt)):
            disciplina = Discipline(dt[i].name,dt[i].curso,dt[i].periodo,dt[i].id,
            dt[i].credito,dt[i].professor,[0]*QUANTIDADE_AULAS_POR_DISCIPLINA)
            new_disp.append(disciplina)
        fragments_new_recriacao = GeradorObject.unzipy(QUANTIDADE_AULAS_POR_DISCIPLINA,individual)
        
        variavel_global.clear()
        counter=0
        #print(horarios_depois_da_recriacao)
        GeradorObject.activateRecreate(0,len(new_disp),deepcopy(new_disp),salas,dList,fragments_new_recriacao,QUANTIDADE_AULAS_POR_DISCIPLINA)
        #print()
        count=0
        for i in variavel_global:
            for d in range(QUANTIDADE_AULAS_POR_DISCIPLINA):
                h = Horario(dList[i.list_classes[d]],0,0)
                sala = Classes(RandomHash.gerator_id(),RandomHash.gerator_id(),60)
                sala.horario = h
                i.list_classes[d] = sala
            count+=1
        
        
        return variavel_global
    @staticmethod
    def activateRecreate(counter,total,new_disp,salas,dList,fragments_new_recriacao,QUANTIDADE_AULAS_POR_DISCIPLINA):
        if counter < total:
            f = GeradorObject.getDiscipline(new_disp,counter,salas,dList,fragments_new_recriacao,QUANTIDADE_AULAS_POR_DISCIPLINA)
            variavel_global.append(f)
            GeradorObject.activateRecreate(counter+1,total,new_disp,salas,dList,fragments_new_recriacao,QUANTIDADE_AULAS_POR_DISCIPLINA)
        else:
            for i in range(len(variavel_global)):
                GeradorObject.validate(variavel_global,i,salas,dList,fragments_new_recriacao,QUANTIDADE_AULAS_POR_DISCIPLINA)

    @staticmethod
    def validate(disciplineList,index,salas,dList,fragments_new_recriacao,QUANTIDADE_AULAS_POR_DISCIPLINA):
        variavel_global[index].list_classes=None
        variavel_global[index].list_classes =fragments_new_recriacao[index]
    @staticmethod
    def getDiscipline(new_disp,position,salas,dList,fragments_new_recriacao,QUANTIDADE_AULAS_POR_DISCIPLINA):
        new_disp[position].list_classes = GeradorObject.recreateClasse(salas,dList,fragments_new_recriacao[position],QUANTIDADE_AULAS_POR_DISCIPLINA,position)
        return new_disp[position]          
    @staticmethod
    def unzipy(splice,individual):
        q = []
        for i in range(0,len(individual), splice):
            q.append( individual[i:i + splice] )
        return q
    @staticmethod
    def recreatedClasseValidated(salas):
        aux = random.randint(0,len(salas)-1)
        sala = (salas[aux])
        return sala
    @staticmethod
    def recreateClasse(salas,dList,horarios_recriados,QUANTIDADE_AULAS_POR_DISCIPLINA,position):
        result=[]
        counter=0
        while counter < QUANTIDADE_AULAS_POR_DISCIPLINA:
            aux = random.randint(0,len(salas)-1)
            sala = (salas[aux])
            sala.horario=None
            sala.horario = Horario(dList[horarios_recriados[counter]],0,0)
            result.insert(counter,sala)
            counter+=1
            sala=None
            aux=None
        anomalia = Counter(result)
        for x in anomalia.values():
            if x == QUANTIDADE_AULAS_POR_DISCIPLINA:
                aux = random.randint(0,len(salas)-1)
                sala = (salas[aux])
                sala.horario = Horario(dList[horarios_recriados[0]],0,0)
                result[0] = sala
        
        return result
        
    @staticmethod
    def get_len_horarios_enumeration():
        return len(HorarioE)
    @staticmethod
    def get_list_horarios_by_enum():
        aux = list(HorarioE)
        list_horarios =[]
        for horario_enum in aux:
            list_horarios.append(horario_enum.name)
        
        return list_horarios
    @staticmethod
    def generate_chave_especific(horarios,k,repeticoes):
        f = random.choices(horarios,k=repeticoes)
        horarios_list= []
        for element in k:
            for horario in element[4]:
                horarios_list.append(horario.codigo)
        
        for i in range(len(f)):
            while f[i].codigo in horarios_list:
                f = random.choices(horarios,k=repeticoes)   
        return f
    @staticmethod
    def generate_horarios_by_sala_pesos(qnt_aulas_disciplina,pesos,horarios):
        return random.choices(horarios,weights=pesos,k=qnt_aulas_disciplina)

    @staticmethod
    def get_horarios():
        return horarios
    @staticmethod
    def get_salas():
        return salas

    @staticmethod
    def generate_horarios_by_sala(salas,horarios):
        pesos = [0]*len(horarios)
        for n in range(len(horarios)):
            pesos[n] = 1
        return random.choices(horarios,weights=pesos)[0]
    
    @staticmethod
    def generate_aula_by_discipline(salas,horarios):
        dList=[]
        horarios_ = GeradorObject.generate_horarios_by_sala(salas,horarios)
        aux = random.randint(0,len(salas)-1)
        dList.append(salas[aux])
        for i in dList:
            i.horario = horarios_
        return dList

    @staticmethod
    def generate_disciplines(qnt_aulas_disciplina):
        list_set = []
        salasx = random.sample(salas,len(salas))
        disciplinasx = random.sample(disciplinas,len(disciplinas))
        horariosx = random.sample(horarios,len(horarios))
        for i in range(len(disciplinasx)):
            disciplinas[i].list_classes = []
            for k in range(qnt_aulas_disciplina):
                disciplinas[i].list_classes.append(GeradorObject.generate_aula_by_discipline(salasx,horariosx)[0])
            list_set.append(disciplinas[i])
        return list_set

    