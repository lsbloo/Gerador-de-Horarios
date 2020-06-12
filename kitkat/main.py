from sockets.sockets_hand import quickstart
from geradores.geratordata import getInstance
from models.discipline import Discipline
from models.horario import Horario
from models.classes import Classes
from models.enumeration import HorarioE
from random import random as rd
import random
from models.constraint import Constraint
from collections import Counter





def compare(s,t):
    return Counter(s) == Counter(t)

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


qnt_aulas_disciplina = 2
dt_discipline = entitys().Gdisciplines()
dt_horario = entitys().Ghorarios()
dt_salas = entitys().GSalas()



salas = dt_salas.get('Tdata')
disciplinas = dt_discipline.get('Tdata')
horarios = dt_horario.get('Tdata')
tamanho_salas = len(salas)


def generate_horarios_by_sala(qnt_aulas_disciplina,salas,horarios):
    dList=[]
    for i in range(qnt_aulas_disciplina):
        aux = random.randint(0,len(salas)-1)
        dList.append(horarios[aux])
    return dList

def generate_sala_by_discipline(qnt_aulas_disciplina,salas,horarios):
    dList=[]
    horarios_ = generate_horarios_by_sala(qnt_aulas_disciplina,salas,horarios)
    for i in range(qnt_aulas_disciplina):
        aux = random.randint(0,len(salas)-1)
        dList.append(salas[aux])
    
    for i in dList:
        i.horario = horarios_
        
    
    return dList

def generate_disciplines():
    list_set = []
    salasx = random.sample(salas,len(salas))
    disciplinasx = random.sample(disciplinas,len(disciplinas))
    horariosx = random.sample(horarios,len(horarios))
    for i in range(len(disciplinasx)):
        disciplinas[i].list_classes = generate_sala_by_discipline(qnt_aulas_disciplina,salasx,horariosx)
        #print(len(disciplinas[i].list_classes))
        list_set.append(disciplinas[i])
    return random.sample(list_set,len(list_set))
    




class Individuo(object):
    def __init__(self,list_disciplines,limite_restricoes,geracao=0):
        self.list_disciplines = list_disciplines
        self.geracao=geracao
        self.horarios_best=0
        self.cromossomo = []
        self.nota_avaliacao = 0

        for i in range(len(self.list_disciplines)):
            for k in range(len(list_disciplines[i].list_classes)):
                self.cromossomo.append(list_disciplines[i].list_classes[k].cromossomo)
        
    
    """
     -> retorna uma funcao de avalicao de acordo com a restrição selecionada pelo usuario.
    """
    def switcher(self,id_funcao):
        did= {
            1:self.disciplinas_mesmo_curso_periodo(),
            2:self.choque_disciplinas(),
            3:self.disciplinas_mesmo_professor(),
            4:self.penalizacao_disciplinas_dia()
        }
        return did.get(int(id_funcao))
    

    def check(self,horario,curso,disciplina,ocorrencias):
        cont = 0
        for k in ocorrencias:
            if k.get("Horario") == horario and k.get("Curso:") != curso and k.get("Disciplina:") == disciplina:
                cont+=1
        return cont

    """
    Para  avaliar  o  cromossomo,  é  levado  em  consideração  o  seguinte:  
    o melhor  indivíduo  é  aquele  que  tem  a  menor  repetição  de  uma  disciplina  para um horário. 
    
    Para isto é criada uma lista de ocorrências, onde são colocados o horário,  
    
    a  disciplina  e  a  quantidade  de  ocorrências  desta  disciplina  neste horário.

    soft constraint 10
    """
    def choque_disciplinas(self,id=2):
        disp = []
        aux = 0
        for i in self.list_disciplines:
            for k in i.list_classes:
                aux = k.horario
            disp.append([i.name,i.curso,aux])
        
        list_horarios = random.sample(horarios.copy(),len(horarios))
        ocorrencias = []
        for i in range(len(disp)):
            result =0
            for k in list_horarios:
                for z in range(len(disp[i][2])):
                    if disp[i][2][z].codigo == k.codigo:
                        result += 1
                        if result >= 2:
                            ocorrencias.append({"Horario": k.codigo, "Disciplina:": disp[i][0], "Curso:": disp[i][1], "Qnt:" :result})
        
        disciplines_choque_counter= 0
        for i in ocorrencias:
            horario = i.get("Horario")
            curso = i.get("Curso:")
            disciplina = i.get("Disciplina:")
            disciplines_choque = self.check(horario,curso,disciplina,ocorrencias.copy())
            if disciplines_choque != 0:
                disciplines_choque_counter += disciplines_choque
        return disciplines_choque_counter

    """
     Para  avaliar  o  cromossomo,  é  levado  em  consideração  o  seguinte:  
     disciplinas do mesmo curso e mesmo período não podem ter aulas no mesmo horário.
     tipo hard constraint 1000
    """
    def check_disciplinas_mesmo_curso_periodo(self,horario,curso,disciplina,periodo,ocorrencias):
        cont = 0
        for i in ocorrencias:
            if i.get("Horario") == horario and i.get("Disciplina") == disciplina and i.get("Curso") == curso and i.get("Periodo") == periodo:
                 cont+=1
        return cont


    def disciplinas_mesmo_curso_periodo(self,id=1):
        disp = []
        aux = 0
        for i in self.list_disciplines:
            for k in i.list_classes:
                aux = k.horario
            disp.append([i.name,i.curso,i.periodo,aux])
        list_horarios = random.sample(horarios.copy(),len(horarios))

        
        q = []
        ocorrencias = []
        for i in range(len(disp)):
            
            horarios_temp=[]
            for k in range(len(disp[0][3])):
                horarios_temp.append(disp[i][3][k].codigo)
            
            
            q.append([disp[i][0],disp[i][1],disp[1][2],horarios_temp[:]])
        d = q[0]
        cont=0
        q.remove(d)
        for k in range(len(q)):
            cont = 0
            if q[k][1] == d[1]:
                if q[k][2] == d[2]:
                    if q[k][3] == d[3]:
                        #print("search: ", q[k][0],q[k][1], q[k][2],q[k][3])
                        #print("DSerach: ", d[0], d[1],d[2],d[3])
                        return 1000
                    else:
                        d = q[k]
                        #print("D: ", d[0], d[3], d[4])
        return 10


    """
     Para  avaliar  o  cromossomo,  é  levado  em  consideração  o  seguinte:  
     disciplinas ministradas pelo mesmo professor não podem ter aulas no mesmo horário.
     tipo hard constraint 1000
    """
    def disciplinas_mesmo_professor(self,id=3):
        disp = []
        aux = 0
        for i in self.list_disciplines:
            for k in i.list_classes:
                aux = k.horario
            disp.append([i.name,i.professor,i.periodo,aux])
        

        q = []
        for i in range(len(disp)):
            
            horarios_temp=[]
            for k in range(len(disp[0][3])):
                horarios_temp.append(disp[i][3][k].codigo)
            
            
            q.append([disp[i][0],disp[i][1],disp[1][2],horarios_temp[:]])
        d = q[0]
        cont=0
        q.remove(d)
        for k in range(len(q)):
            cont = 0
            if q[k][1] == d[1] and q[k][0] == d[0]:
                for n in range(len(q[k][3])):
                    if q[k][3].count(q[k][3][n]) >= 2:
                        #print(q[k][3])
                        return 1000
                    else:
                        d = q[k]
                        #print("D: ", d[0], d[3], d[4])
        return 10

    """
     Para  avaliar  o  cromossomo,  é  levado  em  consideração  o  seguinte:  
     disciplinas que estão subdivididas em blocos de 2 ou 3 horários seguidos.
     Estes blocos não podem estar na grade horária em um mesmo dia, por isso devemos penalizá-los. 
     tipo soft constraint 
    """
    def penalizacao_disciplinas_dia(self,id=4):
        disp = []
        aux = 0
        agrupamentos = 0

        for i in self.list_disciplines:
            for k in i.list_classes:
                aux = k.horario
            disp.append([i.name,i.professor,i.periodo,aux])
        

        q = []
        for i in range(len(disp)):
            
            horarios_temp=[]
            for k in range(len(disp[0][3])):
                horarios_temp.append(disp[i][3][k].codigo)
            
            
            q.append([disp[i][0],disp[i][1],disp[1][2],horarios_temp[:]])
        d = q[0]

        cont=0
        q.remove(d)
        for k in range(len(q)):
            cont = 0
            if q[k][0] == d[0]:
                for n in range(len(q[k][3])):
                    if q[k][3].count(q[k][3][n]) >= 2:
                        #print(q[k][3])
                        agrupamentos+=1
        
        penalizacao_ = agrupamentos
        return penalizacao_

    def comparator(self,key_values,values_result):
        qnt_de_restricoes = len(key_values)
        for i in range(qnt_de_restricoes):
            if values_result[i] == 1000:
                self.nota_avaliacao = 1
                return False
            else:
                if key_values[i] == 2:
                    self.nota_avaliacao += values_result[i]
                if key_values[i] == 1 and values_result[i] != 1000:
                    self.nota_avaliacao += values_result[i]
                if key_values[i] == 3 and values_result[i] != 1000:
                    self.nota_avaliacao += values_result[i]
                if key_values[i] == 4:
                    return {"penalizacao": True, "result": values_result[i]}
        return False 



    def fitness(self,restricoes):
        restricoes_actived_result = []
        
        if len(restricoes) == 0:
            self.nota_avaliacao = random.randint(1,100)
        
        for k in range(len(restricoes)):
            disp = restricoes[k].id_funcao
            restricoes_actived_result.append({"id_f": disp,"result": self.switcher(disp)})
        try:
            key_values=[]
            values_result=[]
            list_key=[]
            print(restricoes_actived_result)
            for i in restricoes_actived_result:
                keys = i.keys()
                for k in keys:
                    if k == "id_f":
                        list_key.append(k)
            
            for i in range(len(list_key)):
                key_values.append(restricoes_actived_result[i].get(list_key[i]))
                values_result.append(restricoes_actived_result[i].get("result"))
            
            result = self.comparator(key_values,values_result)
            if type(result) == bool:
                if self.nota_avaliacao == 1:
                    self.nota_avaliacao=1000
            else:
                # apply penalização
                if result.get("penalizacao") and self.nota_avaliacao != 1:
                    if result.get("result") != 0:
                        if self.nota_avaliacao != 1:
                            if self.nota_avaliacao == 0:
                                self.nota_avaliacao = random.randint(1,100)
                            else:
                                self.nota_avaliacao = self.nota_avaliacao + result.get("result") #penalizacao
            

            if self.nota_avaliacao == 0:
                self.nota_avaliacao = random.randint(1,100)
        except KeyError as e:
            pass
    
    def restricao(self):
        return self.restricoes

    def representSala(self):
        q = " "
        for i in self.list_aulas:
            q+= i.codigo
            q+=","
        return q

    def representHorarios(self,horarios):
        q = " "
        for i in horarios:
            for k in i.horario:
                q += k.toString()
                q+= ","
                
        return q
    def representCromossomo(self,cromossomos):
        q = " "
        for i in cromossomos:
            q+= i.cromossomo
            q+=","
        return q
        
    def toString(self):
        for i in self.list_disciplines:
            if i != None:
                print("Nome: {name}, Curso: {curso}, Professor: {professor}, Periodo: {periodo}, \n Cromossomos: {cromossomos} \n Horarios: {horarios}".format(name=i.name,curso=i.curso,professor=i.professor,periodo=i.periodo,cromossomos=self.representCromossomo(i.list_classes),horarios=self.representHorarios(i.list_classes)))
        


    def crossover(self,outro_individuo):
        pass

    def mutacao(self,taxa_mutacao):
        pass

class AlgoritmoGenetico(object):
    def __init__(self,tamanho_populacao):
        self.tamanho_populacao=tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
    
   
    def criar_populacao(self,limite_restricoes):
        for i in range(self.tamanho_populacao):
            dt = random.sample(generate_disciplines(),len(generate_disciplines()))
            self.populacao.append(Individuo(dt,limite_restricoes))

        self.melhor_solucao = self.populacao[0]
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,key=lambda populacao: populacao.nota_avaliacao,reverse=True)
    
    def selecao(self):
        lista_melhores_individuos=[]
        
             
    def melhor_individuo(self,individuo):
        if individuo.nota_avaliacao < self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
        return self
    
    def len_populacao(self):
        return len(self.populacao)

    def return_only_individuo(self,index):
        return self.populacao[index]
    def return_populacao(self):
        return self.populacao

algoritmoGenetico = AlgoritmoGenetico(1)

limite_restricoes = 3

algoritmoGenetico.criar_populacao(limite_restricoes)

print(algoritmoGenetico.len_populacao())

constraint1 = Constraint("R1","disciplinas do mesmo curso e mesmo período não podem ter aulas no mesmo horário","hard",1000,1)

constraint2 = Constraint("R2","o melhor  indivíduo  é  aquele  que  tem  a  menor  repetição  de  uma  disciplina  para um horário.","soft",10,2)

constraint3 = Constraint("R3","disciplinas ministradas pelo mesmo professor não podem ter aulas no mesmo horário.","hard",1000,3)
constraint4 = Constraint("R4","penalizacao","soft",10,4)


restricoes = []
restricoes.append(constraint1)
restricoes.append(constraint2)
restricoes.append(constraint3)
restricoes.append(constraint4)

for individuo in algoritmoGenetico.return_populacao():
    #individuo.toString()
    individuo.fitness(restricoes)


algoritmoGenetico.ordena_populacao()

for i in range(algoritmoGenetico.len_populacao()):

    r = algoritmoGenetico.melhor_individuo(algoritmoGenetico.populacao[i])
print("melhor", r.melhor_solucao.nota_avaliacao)















