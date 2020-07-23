
# Define as funções de restrições.
from collections import Counter


##################################################################################################################
"""
  -> Disciplinas do mesmo e curso e periodo não podem ter aulas no mesmo horario. 
  R1;
"""
def R1(disciplines):
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
    violations = conclusion(disp,list_periodos,list_cursos)
    if violations == 0:
        return {"violations": 0}
    return {"violations": violations}


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
    if len(conclusao) != 0:
        for i in conclusao.values():
            if i>=2:
                return True
        return False

def conclusion(disp,lenxc,lenxp):
    dispx = disp.copy()
    resposta = []
    for i in range(len(lenxc)):
       pacote = getter_search(dispx,lenxp,lenxc,i)
       for k in pacote:
            if k != None or len(k) != 0:
                q =counter(k)
                if q == None:
                    pass
                else:
                    resposta.append(q)
       
    counterx = len(resposta)
    violations = resposta.count(True)
    return violations
###################################################################################################################


###################################################################################################################
"""
    Para avaliar o cromossomo é levado em consideração o seguinte: 
    disciplinas ministradas pelo mesmo professor não podem ter aulas no mesmo horario.
"""
def R2(disciplines):
    professores = []
    l = set(disciplines)
    disp=[]
    for i in l:
        professores.append(i.professor)
        disp.append([i.name,i.professor,i.periodo,i.list_classes])

    violations = get_violations_R2(disp, set(professores))
    if violations == 0:
        return {"violations": 0}
    return {"violations": violations}

def search_disp(disp,professor):
    dd = []
    for i in range(len(disp)):
        cont = 0
        q = []
        if disp[i][1] == professor:
            dd.append([disp[i][0], disp[i][3]])
    return dd
def violation_R2(aulas):
    counter_validation_genes = Counter(aulas)
    cont_violation=0
    for key in counter_validation_genes.keys():
        value = counter_validation_genes.get(key)
        if value>=2:
            cont_violation+=1
    return cont_violation

def get_violations_R2(disp,list_professores):
    violations = []
    for professor in list_professores:
        response_search = search_disp(disp,professor)
        if len(response_search) >=2:
            aulas=[]
            for result_parsed in response_search:
                for aula in result_parsed[1]:
                    aulas.append(aula.horario.id)
            re = violation_R2(aulas)
            if re!=0:
                violations.append(re)
    total_violation=0
    for violation_individual in violations:
        total_violation+=violation_individual
    
    return total_violation
###################################################################################################################
    

           
        

