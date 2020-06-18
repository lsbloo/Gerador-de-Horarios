from sockets.sockets_hand import quickstart
from geradores.geratordata import getInstance
from models.discipline import Discipline
from models.horario import Horario
from models.classes import Classes
from models.enumeration import HorarioE
from random import random as rd
import random
from models.constraint import Constraint
from kitkatGA import AlgoritmoGenetico
from geratores import GEntitys
from geratores import GeradorObject
from util import RandomHash
from util import compare
from individuos_ag import Individuo
import time

#quickstart()

constraint1 = Constraint("R1","disciplinas do mesmo curso e mesmo período não podem ter aulas no mesmo horário","hard",1000,1)

constraint2 = Constraint("R2","o melhor  indivíduo  é  aquele  que  tem  a  menor  repetição  de  uma  disciplina  para um horário.","soft",10,2)

constraint3 = Constraint("R3","disciplinas ministradas pelo mesmo professor não podem ter aulas no mesmo horário.","hard",1000,3)
constraint4 = Constraint("R4","penalizacao","soft",10,4)

restricoes = []
restricoes.append(constraint1)
restricoes.append(constraint2)
restricoes.append(constraint3)
restricoes.append(constraint4)

tamanho_populacao = 1
numero_geracoes = 0
taxa_mutacao = 0.10
qnt_aulas_disciplinas = 2

algoritmoGenetico = AlgoritmoGenetico(tamanho_populacao)

limite_restricoes = 3

melhor_solucao=algoritmoGenetico.resolver(limite_restricoes,numero_geracoes,restricoes,taxa_mutacao)
print("Nota: ", melhor_solucao.nota_avaliacao)
print("Geração:", melhor_solucao.geracao)
print()

## criar quadro de horario gerado;
si_list = []
lcc_list = []
for i in melhor_solucao.list_disciplines:
    if i.curso == "si":
        si_list.append(i)
    else:
        lcc_list.append(i)
q = set(si_list)  
si_list = sorted(q,key=lambda discipline: discipline.periodo,reverse=False)
s = set(lcc_list)
lcc_list = sorted(s,key= lambda discipline: discipline.periodo, reverse=True)

if melhor_solucao.nota_avaliacao > 200:
    for i in lcc_list:
        print(i.toString())

















