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
from collections import Counter
import time


class Individuo(object):
    def __init__(self,list_disciplines,limite_restricoes,pai,geracao=0):
        self.list_disciplines = list_disciplines
        self.geracao=geracao
        self.horarios_best=0
        self.cromossomo = []
        self.nota_avaliacao = 0
        self.qnt_aulas_por_disciplina=2
        if pai == None:
            self.papai = None
        else:
            self.papai = pai
        

        for i in range(len(self.list_disciplines)):
            for k in range(len(list_disciplines[i].list_classes)):
                self.cromossomo.append(list_disciplines[i].list_classes[k].cromossomo)
        
        self.re()


    def get_discipline_by_id(self,idx):
        for i in range(len(self.list_disciplines)):
            if self.list_disciplines[i].id == idx:
                return i

    def search_packet(self,dispx,periodo,lenxc,limitador=0):
        q = []
        for i in range(len(dispx)):
            if dispx[i][2] == lenxc[limitador]:
                if dispx[i][3] == periodo:
                        q.append(dispx[i])
        
        for i in q:
            if i == None:
                q.remove(i)
        
        return {"dt": q, "l": limitador}
    
    def get_packet(self,dispx,lenxp,lenxc,limitador):
        d = []
        for i in range(len(lenxp)):
            search = self.search_packet(dispx,lenxp[i],lenxc,limitador)
            if search.get("dt") != None:
                d.append(search.get("dt"))
        if len(d) != 0 or d != None:
            pacote = []
            for i in d:
                if i != None:
                    pacote.append(i)
            return pacote
    
    def transpost(self,k,key,repeticoes,lista_horarios):
        k = k.copy()
        #print("KEY", key)
        indices = []
        novos = []
        for elements in k:
            for horario in elements[4]:
                if key in horario.codigo:
                    #print(horario.codigo)
                    novos = GeradorObject.generate_chave_especific(lista_horarios,k,repeticoes)
                    indices.append({key : novos})
        keys = indices[0].keys()
        q=[]
        for key in keys:
            q = indices[0].get(key)
        
        #print("chaves encontradas: ",len(q), "numero de repeticoes:", repeticoes)
        return q


    def search_transport(self,item_parse,k,delimiter):
        dList = []
        position = -1
        for i in k:
            for d in i[4]:
                if item_parse == d.codigo:
                    position+=1
                    dList.append([i[0], position,d.codigo])
        
        if delimiter < len(dList):
            paff =[]
            for i in range(delimiter):
                paff.append(dList[i])
                if i >= len(dList):
                    break
            
            return paff
        return dList

    def change(self,disciplina_id,horario_novo,chave):
        disciplina = self.list_disciplines[self.get_discipline_by_id(disciplina_id)]
        horarios = disciplina.list_classes[0].horario
        for i in range(len(horarios)):
            if horarios[i].codigo == chave:
                print("velho", self.list_disciplines[self.get_discipline_by_id(disciplina_id)].list_classes[0].horario[i].codigo)
                self.list_disciplines[self.get_discipline_by_id(disciplina_id)].list_classes[0].horario[i] = horario_novo
                print("novo", self.list_disciplines[self.get_discipline_by_id(disciplina_id)].list_classes[0].horario[i].codigo)
                return True
        return False

    def system_dir(self,k):
        d = [] 
        for i in k:
            for n in i[4]:
                d.append(n.codigo)
        conclusao = Counter(d)
        lista_horarios = GeradorObject.get_horarios()
        chaves_repetidas = []
        #print(conclusao)
        if len(conclusao) != 0:
            #print("1",conclusao)
            keys = conclusao.keys()
            for key in keys:
                propos = []
                if conclusao.get(key) >= 2:
                    chaves_repetidas.append([key,conclusao.get(key)])
        result = []
        for chave in range(len(chaves_repetidas)): 
            result.append([ chaves_repetidas[chave], self.transpost(k,chaves_repetidas[chave][0],chaves_repetidas[chave][1],lista_horarios) ])
        parse=[]    
        for i in result:
            parse.append([i[0][0], i[1]])
        
        for i in parse:
            if len(i) != 0 and i!=None:
                fd = []
                s= len(i[1])
                index_ = self.search_transport(i[0],k,s)
                fd = i[1]
                print(index_)
                print(fd)
                print()           
                for d in range(len(index_)):
                    disciplina_id = index_[d][0]
                    horario_novo = fd[d]
                    chave = index_[d][2]  
                    resultado = self.change(disciplina_id,horario_novo,chave)
                    if resultado:
                        print("mudou")

        
    """
     -> re organiza os horarios de cada periodo do curso
     aplica um sistema de peso pra cada horario repetido e faz a re-organização.
    """    
    def re(self):
        disp = []
        periodos = []
        curso = []
        l = self.list_disciplines
        for i in l:
            disp.append([i.id,i.name,i.curso,i.periodo,i.list_classes[0].horario])
            periodos.append(i.periodo)
            curso.append(i.curso)

        list_periodos = list(set(periodos))
        list_cursos = list(set(curso))
        resposta=[]
        
        for i in range(len(list_cursos)):
            packets = self.get_packet(disp,list_periodos,list_cursos,i)
            for packet in packets:
                pass
            self.system_dir(packets[0])                    
        
    """
     -> retorna uma funcao de avalicao de acordo com a restrição selecionada pelo usuario.
    """
    def switcher(self,id_funcao):
        if id_funcao == 1:
            return self.disciplinas_mesmo_curso_periodo()
        elif id_funcao==2:
            return self.choque_disciplinas()
        elif id_funcao==3:
            return self.disciplinas_mesmo_professor()
        elif id_funcao==4:
            return self.penalizacao_disciplinas_dia()
       
    

    def check(self,horario,curso,disciplina,ocorrencias):
        cont = 0
        for k in ocorrencias:
            if k.get("Horario") == horario and k.get("Curso:") != curso and k.get("Disciplina:") == disciplina:
                cont+=1
        return cont

    """
    Para  avaliar  o  cromossomo,  é  levado  em  consideração  o  seguinte: 
    
     E é criada uma lista de ocorrências, onde são colocados o horário,  
    
    a  disciplina  e  a  quantidade  de  ocorrências  desta  disciplina  neste horário.

    se a quantidade de ocorrencias for maior que 2 retorna a nota de 30
    se nao retorna 50

    soft constraint 
    """
    def choque_disciplinas(self,id=2):
        disp = []
        aux = 0
        for i in self.list_disciplines:
            disp.append([i.name,i.curso,i.list_classes])

        list_horarios = horarios.copy()
        

        ocorrencias = []
        for i in range(len(disp)):
            result =0
            for k in list_horarios:
                for z in range(len(disp[i][2])):
                    for f in range(len(disp[i][2][z].horario)):
                        if disp[i][2][z].horario[f].codigo == k.codigo:
                            result += 1
                            if result >= 2:
                                ocorrencias.append({"Horario": k.codigo, "Disciplina:": disp[i][0], "Curso:": disp[i][1], "Qnt:" :result})
        
        disciplines_choque_counter= 0

        #print(ocorrencias)
        for i in ocorrencias:
            horario = i.get("Horario")
            curso = i.get("Curso:")
            disciplina = i.get("Disciplina:")
            disciplines_choque = self.check(horario,curso,disciplina,ocorrencias.copy())
            if disciplines_choque != 0:
                disciplines_choque_counter += disciplines_choque
        if disciplines_choque_counter > 2:
            return 30
        else:
            return 50
        return disciplines_choque_counter

    """
     Para  avaliar  o  cromossomo,  é  levado  em  consideração  o  seguinte:  
     disciplinas do mesmo curso e mesmo período não podem ter aulas no mesmo horário.
     tipo hard constraint
    """
    def search(self,dispx,periodo,lenxc,limitador=0):
        q = []

        for i in range(len(dispx)):
            if dispx[i][1] == lenxc[limitador]:
                if dispx[i][2] == periodo:
                        q.append(dispx[i])
        
        for i in q:
            if i == None:
                q.remove(i)
        
        return {"dt": q, "l": limitador}
    
    def getter_search(self,dispx,lenxp,lenxc,limitador):
        d = []
        for i in range(len(lenxp)):
            search = self.search(dispx,lenxp[i],lenxc,limitador)
            if search.get("dt") != None:
                d.append(search.get("dt"))
        if len(d) != 0 or d != None:
            pacote = []
            for i in d:
                if i != None:
                    pacote.append(i)
            return pacote

    def counter(self,k):
        d = [] 
        for i in k:
            for n in i[3]:
                d.append(n.codigo)
        conclusao = Counter(d)
        
        #print(conclusao)
        if len(conclusao) != 0:
            #print()
            print(conclusao)
            #print()
            for i in conclusao.values():
                #print(i)
                if i >=2:
                    return True
            return False

    def conclusion(self,disp,lenxp,lenxc):
        dispx = disp.copy()
        resposta = []
        for i in range(len(lenxc)):
            pacote = self.getter_search(dispx,lenxp,lenxc,i)
            for k in pacote:
                if k != None or len(k) != 0:
                    #print()
                    #print(k)
                    #print()
                    q = self.counter(k)
                    resposta.append(q)

        indices=[]
        cont=0
        
        for i in range(len(resposta)-1):
            if resposta[i] == None:
                cont+=1
        
                    
        counter = len(resposta) - cont
        #print(counter)
        #print(resposta)
        if resposta.count(False) == counter:
            
            return True
        else:
            return False
             

    def disciplinas_mesmo_curso_periodo(self,id=1):
        disp = []
        periodos = []
        curso = []
        l = set(self.list_disciplines)
        for i in l:
            disp.append([i.name,i.curso,i.periodo,i.list_classes[0].horario])
            periodos.append(i.periodo)
            curso.append(i.curso)

        list_periodos = list(set(periodos))
        list_cursos = list(set(curso))

        d = self.conclusion(disp,list_periodos,list_cursos)
        if d == True:
            return 100
        return 10


    """
     Para  avaliar  o  cromossomo,  é  levado  em  consideração  o  seguinte:  
     disciplinas ministradas pelo mesmo professor não podem ter aulas no mesmo horário.
     tipo hard constraint
    """
    def disciplinas_mesmo_professor(self,id=3):
        disp = []
        aux = 0
        for i in self.list_disciplines:
            disp.append([i.name,i.professor,i.periodo,i.list_classes])
        d = disp[0]
        disp.remove(d)
        for k in range(len(disp)):
            cont = 0
            if disp[k][1] == d[1] and disp[k][0] == d[0]:
                 for z in range(len(disp[k][3])):
                    for f in range(len(disp[k][3][z].horario)):
                        if disp[k][3][z].horario.count(disp[k][3][z].horario[f]) >=2:
                            return 10
                        else:
                            d = disp[k]
            else:
                d = disp[k]
                #import pdb; pdb.set_trace()
        return 100

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
                        
            else:
                d = q[k]
                #import pdb; pdb.set_trace()
        penalizacao_ = agrupamentos
        return penalizacao_

    def E(self,key_values,values_result):
        qnt_de_restricoes = len(key_values)
        for i in range(qnt_de_restricoes):
            if key_values[i] == 2:
                self.nota_avaliacao += values_result[i]
            if key_values[i] == 1:
                self.nota_avaliacao += values_result[i]
            if key_values[i] == 3:
                self.nota_avaliacao += values_result[i]
            if key_values[i] == 4: 
                self.nota_avaliacao += values_result[i]

    def fitness(self,restricoes):
        restricoes_actived_result = []
        
        if len(restricoes) == 0:
            self.nota_avaliacao = random.randint(1,100)
        
        for k in range(len(restricoes)):
            restricoes_actived_result.append({"id_f": restricoes[k].id_funcao,
            "result": self.switcher(restricoes[k].id_funcao)})
        
        try:
            key_values=[]
            values_result=[]
            list_key=[]
            #print(restricoes_actived_result)
            for i in restricoes_actived_result:
                keys = i.keys()
                for k in keys:
                    if k == "id_f":
                        list_key.append(k)
            
            for i in range(len(list_key)):
                key_values.append(int(restricoes_actived_result[i].get(list_key[i])))
                values_result.append(restricoes_actived_result[i].get("result"))
            
            self.E(key_values,values_result)
           
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

    def representCromossomo(self,cromossomos):
        q = " "
        for i in cromossomos:
            q+= i.cromossomo
            q+=","
        return q
        
    def toString(self):
        for i in self.list_disciplines:
            if i != None:
                print("Nome: {name}, Curso: {curso}, Professor: {professor}, Periodo: {periodo}".format(name=i.name,curso=i.curso,professor=i.professor,periodo=i.periodo))
        


    # corte de um ponto.
    # cruzamento entre pais e criação de filhos
    def crossover(self,outro_individuo):
        corte = round(rd() * len(self.list_disciplines))

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
        dlist = GeradorObject.generate_horarios_by_sala(qnt_aulas_por_disciplina,salasx,horariosx)
        kk = dlist[0]
        #print(kk.codigo, kk.horario[0].id, kk.horario[1].id)
        return dlist

    def mutacao(self,taxa_mutacao):
        counter = -1
        for i in range(0,len(self.cromossomo)):
            p=[]
            q =[]
            for k in range(len(self.list_disciplines[0].list_classes[0].horario)):
                q.append(self.cromossomo[i])
            counter+=1
            p.append({"crome": counter,"dt": q})
            
            if len(p[0].get("dt")) != 1:
                xd = p[0].get("dt")
                if rd() < taxa_mutacao:
                    for d in range(len(xd)):
                        if xd[d] == "1":
                            self.list_disciplines[p[0].get("crome")].list_classes[0].cromossomo="0"
                            self.list_disciplines[p[0].get("crome")].list_classes[0].horario[d] = self.list_disciplines[p[0].get("crome")].list_classes[0].horario[d]
                        else:
                            self.list_disciplines[p[0].get("crome")].list_classes[0].cromossomo="1"
                            self.list_disciplines[p[0].get("crome")].list_classes[0].horario[d] = self.list_disciplines[p[0].get("crome")].list_classes[0].horario[d]
        
        return self