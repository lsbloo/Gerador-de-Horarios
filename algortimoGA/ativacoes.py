
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
    
"""
    Para avaliar o cromossomo é levado em consideração o seguinte: 
    uma disciplina não pode ter mais de duas aulas no mesmo dia.
"""
def R3(disciplines,dList):
    l = set(disciplines)
    disp=[]
    for i in l:
        disp.append([i.name,i.professor,i.list_classes])
    violation = counter_disp_horarios_equals(disp,dList)
    if violation == 0:
        return {"violations": 0}
    return {"violations": violation}

def getDiaHorarios(dList):
    q = []
    for horario_id in dList:
        splitter = horario_id.split("_")
        q.append(splitter[0])
    d = list(set(q))
    return d
def splitter_counter(horario_id):
    return horario_id.split("_")[0]

def counter_disp_horarios_equals(disp,dList):
    violation=0
    dias_horarios = getDiaHorarios(dList)
    for i in range(len(disp)):
        aulas=[]
        for horario_index in range(len(disp[i][2])):
            aulas.append(disp[i][2][horario_index].horario.id)
        xd = []
        for aula in aulas:
            cont=0
            re = splitter_counter(aula)
            xd.append(re)
        if xd.count(re) >=2:
            violation+=1
    return violation

###################################################################################################################


    
"""
    Para avaliar o cromossomo é levado em consideração o seguinte: 
    disciplinas que tem horario igual as 15H serão penalizadas.
"""
def R4(disciplines,dList):
    l = set(disciplines)
    disp=[]
    param= "15H"
    for i in l:
        disp.append([i.list_classes])
    horarios_15H = get_horarios_15H(dList,param)
    violations = search_ocorrencia_15h(disp,horarios_15H)
    if violations == 0:
        return {"violations": 0}
    return {"violations": violations}

def get_horarios_15H(dList,param):
    result=[]
    for horario in dList:
        if horario.find(param) != -1:
            result.append(horario)
    return result

def search_ocorrencia_15h(disp,horarios_15H):
    violations=0
    for i in range(len(disp)):
        for n in range(len(disp[i])):
            for z in range(len(disp[i][n])):
                if disp[i][n][z].horario.id in horarios_15H:
                    violations+=1
    return violations

###################################################################################################################


"""
    Para avaliar o cromossomo é levado em consideração o seguinte: 
    professores que dão aula em 1 dia serão penalizados,
    professores que dão aula em mais de 3 dias serão penalizados.

"""
def R5(disciplines):
    l = set(disciplines)
    disp=[]
    distinct_professor=[]
    for i in l:
        disp.append([i.professor,i.list_classes])
        distinct_professor.append(i.professor)
    
    dd = list(set(distinct_professor))
    packets_aula = packets_aulas_professor(disp)
    violations = counter_aulas_na_semana_por_professor(dd,packets_aula)

    if violations == 0:
        return {"violations": 0}
    return {"violations": violations}

def find_aulas_by_professor(professor,packets_aulas_professor):
    find=[]
    for packets in packets_aulas_professor:
        if professor == packets[0]:
            find.append(packets[1])
    
    return find

def counter_aulas_na_semana_por_professor(list_professores,packets_aulas_professor):
    violations=0
    for professor in list_professores:
        q = find_aulas_by_professor(professor,packets_aulas_professor)
        res = list(set(q))
        if len(res) == 1 or len(res) >=3:
            violations+=1     
    return violations

def packets_aulas_professor(disp):
    packets_aula=[]
    for i in range(len(disp)):
        for k in range(len(disp[i])):
            packets_aula.append([disp[i][0],splitter_counter(disp[i][1][k].horario.id)])
    return packets_aula
    
##############################################################################################


"""
    Para avaliar o cromossomo:
        Aulas as 13H serão penalizadas.
"""
def R6(disciplines,dList):
    l = set(disciplines)
    disp=[]
    param= "13H"
    for i in l:
        disp.append([i.list_classes])
    horarios_13H = get_horarios_13H(dList,param)
    violations = search_ocorrencia_13h(disp,horarios_13H)
    if violations == 0:
        return {"violations": 0}
    return {"violations": violations}

def get_horarios_13H(dList,param):
    result=[]
    for horario in dList:
        if horario.find(param) != -1:
            result.append(horario)
    return result

def search_ocorrencia_13h(disp,horarios_13H):
    violations=0
    for i in range(len(disp)):
        for n in range(len(disp[i])):
            for z in range(len(disp[i][n])):
                if disp[i][n][z].horario.id in horarios_13H:
                    violations+=1
    return violations