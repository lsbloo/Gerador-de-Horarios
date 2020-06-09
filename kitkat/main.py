from sockets.sockets_hand import quickstart
from geradores.geratordata import getInstance
from models.discipline import Discipline
from models.horario import Horario
from models.classes import Classes
from models.enumeration import HorarioE
import random
from models.constraint import Constraint



class RandomHash(object):
    
    @staticmethod
    def gerator_id():
        return random.getrandbits(128)

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


dt_discipline = entitys().Gdisciplines()
dt_horario = entitys().Ghorarios()
dt_salas = entitys().GSalas()


salas = dt_salas.get('Tdata')
disciplinas = dt_discipline.get('Tdata')
horarios = dt_horario.get('Tdata')

qnt_aulas_disciplina = 2

tamanho_salas = len(salas)

def generate_horarios_by_sala(qnt_aulas_disciplina,salas,horarios):
    dList=[]
    for i in range(qnt_aulas_disciplina):
        aux = random.randint(0,tamanho_salas)
        dList.append(horarios[aux - 1])
    return dList

def generate_sala_by_discipline(qnt_aulas_disciplina,salas,horarios):
    dList=[]
    horarios_ = generate_horarios_by_sala(qnt_aulas_disciplina,salas,horarios)
    for i in range(qnt_aulas_disciplina):
        aux = random.randint(0,tamanho_salas)
        dList.append(salas[aux - 1])
    
    for i in dList:
        i.horario = horarios_
        
    
    return dList

def generate_disciplines():
    list_set = []
    for i in range(len(disciplinas)):
        disciplinas[i].list_classes = generate_sala_by_discipline(qnt_aulas_disciplina,salas,horarios)
        #print(len(disciplinas[i].list_classes))
        list_set.append(disciplinas[i])
    return list_set

disciplines_dt_1 = generate_disciplines()


class Individuo(object):
    def __init__(self,name,curso,professor,periodo,list_aulas,geracao=0):
        self.name=name
        self.curso = curso
        self.professor = professor
        self.periodo = periodo
        self.list_aulas =list_aulas
        self.cromossomo = []
        self.horarios = []
        self.geracao=geracao

        for i in range(len(self.list_aulas)):
            self.cromossomo.append(list_aulas[i].cromossomo)
            self.horarios.append(list_aulas[i].horario)

    
    def representSala(self):
        q = " "
        for i in self.list_aulas:
            q+= i.codigo
            q+=","
        return q

    def representHorarios(self):
        q = " "
        for i in self.horarios:
            for k in i:
                q += k.toString()
                q+= ","
                
        return q
    def representCromossomo(self):
        q = " "
        for i in self.cromossomo:
            q+= i
            q+=","
        return q
        
    def toString(self):
        return "Nome: {name}, Curso: {curso}, Professor: {professor}, Periodo: {periodo},\n Salas:{salas} \n Horarios Disponiveis:{horarios},\n Cromossomos: {cromossomo}".format(name=self.name,curso=self.curso,professor=self.professor,periodo=self.periodo,horarios=self.representHorarios(),salas=self.representSala(),cromossomo=self.representCromossomo())

    
    def fitness(self,restricoes):
        pass

    def crossover(self,outro_individuo):
        pass

    def mutacao(self,taxa_mutacao):
        pass

discipline_ind = disciplines_dt_1


class AlgoritmoGenetico(object):
    def __init__(self,tamanho_populacao):
        self.tamanho_populacao=tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
    
    """
        -> inicializa uma população de individuos, de acordo com o tamanho da populacao.
        se o tamanho da populacao for 2, logo o numero de individuos criados vai ser
        2x84 -> pois os individuos pre-carregados tem valor default de 84.
    """
    def criar_populacao(self,name,curso,professor,periodo,list_classes):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(name,curso,professor,periodo,list_classes))
    
    def len_populacao(self):
        return len(self.populacao)

    def return_only_individuo(self,index):
        return self.populacao[index]

algoritmoGenetico = AlgoritmoGenetico(2)


for i in discipline_ind:
    algoritmoGenetico.criar_populacao(i.name,i.curso,i.professor,i.periodo,i.list_classes)

algoritmoGenetico.len_populacao()
indv = algoritmoGenetico.return_only_individuo(10)

print(indv.toString())











