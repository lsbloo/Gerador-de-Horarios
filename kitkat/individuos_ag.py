from sockets.sockets_hand import quickstart
from geradores.geratordata import getInstance
from models.discipline import Discipline
from models.horario import Horario
from models.classes import Classes
from models.enumeration import HorarioE
from random import random as rd
import random
from geratores import salas
from geratores import disciplinas
from geratores import horarios
from geratores import tamanho_salas
from geratores import GeradorObject

class Individuo(object):
    def __init__(self,list_disciplines,limite_restricoes,pai,geracao=0):
        self.list_disciplines = list_disciplines
        self.geracao=geracao
        self.horarios_best=0
        self.cromossomo = []
        self.nota_avaliacao = 0
        if pai == None:
            self.papai = None
        else:
            self.papai = pai
        

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
                        return 100
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
                        return 100
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
            if values_result[i] == 100:
                self.nota_avaliacao = 1
                return False
            else:
                if key_values[i] == 2:
                    self.nota_avaliacao += values_result[i]
                if key_values[i] == 1 and values_result[i] != 100:
                    self.nota_avaliacao += values_result[i]
                if key_values[i] == 3 and values_result[i] != 100:
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
                    self.nota_avaliacao=100
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
        


    # corte de um ponto.
    # cruzamento entre pais e criação de filhos
    def crossover(self,outro_individuo):
        corte = round(rd() * len(self.cromossomo))

        filho_1 = outro_individuo.list_disciplines[0:corte] + self.list_disciplines[corte::]
        filho_2 = self.list_disciplines[0:corte] + outro_individuo.list_disciplines[corte::]

        filhote1 = Individuo(filho_1,3,outro_individuo,self.geracao + 1)
        filhote2 = Individuo(filho_2,3,self,self.geracao + 1)

        list_filhotes = []
        list_filhotes.append(filhote1)
        list_filhotes.append(filhote2)

        return list_filhotes


    def mutacao_genes(self,qnt_aulas_por_disciplina,indice_class):
        salasx = random.sample(salas,len(salas))
        horariosx = random.sample(horarios,len(horarios))
        dlist = GeradorObject.generate_sala_by_discipline(qnt_aulas_por_disciplina,salasx,horariosx)
        kk = dlist[0]
        #print(kk.codigo, kk.horario[0].id, kk.horario[1].id)
        return dlist

    def mutacao(self,taxa_mutacao):
        counter = -1
        for i in range(0,len(self.cromossomo),len(self.list_disciplines[0].list_classes)):
            p=[]
            q =[]
            for k in range(len(self.list_disciplines[0].list_classes)):
                q.append(self.cromossomo[i])
            counter+=1
            p.append({"crome": counter,"dt": q})
            #print(p)
            if len(p[0].get("dt")) != 1:
                xd = p[0].get("dt")
                if rd() < taxa_mutacao:
                    for d in range(len(xd)):
                        if xd[d] == "1":
                            self.list_disciplines[p[0].get("crome")].list_classes[d].cromossomo ="0"
                            self.list_disciplines[p[0].get("crome")].list_classes[d].horario = self.mutacao_genes(len(self.list_disciplines[0].list_classes),d)
                        else:
                            self.list_disciplines[p[0].get("crome")].list_classes[d].cromossomo ="1"
                            self.list_disciplines[p[0].get("crome")].list_classes[d].horario = self.mutacao_genes(len(self.list_disciplines[0].list_classes),d)