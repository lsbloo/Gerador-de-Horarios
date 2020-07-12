
# Define as funções de restrições.
from collections import Counter



"""
  -> Disciplinas do mesmo e curso e periodo não podem ter aulas no mesmo horario. 
"""
def R1(disciplines,valor_maximo,valor_minimo):
    disp = []
    periodos = []
    curso = []
    l = set(disciplines)
    for i in l:
        disp.append([i.name,i.curso,i.periodo,i.list_classes])
        periodos.append(i.periodo)
        curso.append(i.curso)

    list_periodos = list(set(periodos))
    list_cursos = list(set(curso))
    d = conclusion(disp,list_periodos,list_cursos)
    if d == True:
        return valor_maximo
    return valor_minimo


def search(dispx,periodo,lenxc,limitador=0):
        q = []
        for i in range(len(dispx)):
            if dispx[i][2] == lenxc[limitador]:
                if dispx[i][1] == periodo:
                        q.append(dispx[i])
        for i in q:
            if i == None:
                q.remove(i)
        return {"dt": q, "l": limitador}

def getter_search(dispx,lenxp,lenxc,limitador):
        d = []
        for i in range(len(lenxp)):
            searchx = search(dispx,lenxp[i],lenxc,limitador)
            if searchx.get("dt") != None:
                d.append(searchx.get("dt"))
        if len(d) != 0 or d != None:
            pacote = []
            for i in d:
                if i != None:
                    pacote.append(i)
            return pacote
    
def counter(k):
    d = [] 
    for i in k:
        for n in i[3]:
            d.append(n.horario.id)
    conclusao = Counter(d)
        
    #print(conclusao)
    if len(conclusao) != 0:
        import pdb; pdb.set_trace()
        print(conclusao)
        for i in conclusao.values():
            #print(i)
            if i>1:
                True
        return False

"""
 -> verifica se aonde há repetição de horario, a repetição do horario é na mesma
 disciplina:
  -> Horario Repetido: QUINTA_13H: 2x
  se for na disciplina de introdução a programação, então é valido
  pois as duas aulas tem o tempo de inicio 13H e pela duplicação vai até 17H
"""
def veryfiyR1(conclusao):
    pass

def conclusion(disp,lenxc,lenxp):
    dispx = disp.copy()
    resposta = []
    for i in range(len(lenxc)):
       pacote = getter_search(dispx,lenxp,lenxc,i)
       for k in pacote:
            if k != None or len(k) != 0:
                #print()
                #print(k)
                #print()
                q =counter(k)
                if q == None:
                    pass
                else:
                    resposta.append(q)
       
    counterx = len(resposta)
    #print(counterx)
    #print(resposta)
    if resposta.count(False) == counterx:
            return True
    else:
        return False