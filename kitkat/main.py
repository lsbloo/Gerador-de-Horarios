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


constraint1 = Constraint("R1","disciplinas do mesmo curso e mesmo período não podem ter aulas no mesmo horário","hard",1000,1)

constraint2 = Constraint("R2","o melhor  indivíduo  é  aquele  que  tem  a  menor  repetição  de  uma  disciplina  para um horário.","soft",10,2)

constraint3 = Constraint("R3","disciplinas ministradas pelo mesmo professor não podem ter aulas no mesmo horário.","hard",1000,3)
constraint4 = Constraint("R4","penalizacao","soft",10,4)


algoritmoGenetico = AlgoritmoGenetico(1)

limite_restricoes = 3

algoritmoGenetico.criar_populacao(limite_restricoes)

print(algoritmoGenetico.len_populacao())

restricoes = []
restricoes.append(constraint1)
restricoes.append(constraint2)
restricoes.append(constraint3)
restricoes.append(constraint4)

for individuo in algoritmoGenetico.return_populacao():
    #individuo.toString()
    individuo.fitness(restricoes)
    res = individuo.crossover(individuo)
    individuo.mutacao(0.5)

algoritmoGenetico.ordena_populacao()

for i in range(algoritmoGenetico.len_populacao()):

    r = algoritmoGenetico.melhor_individuo(algoritmoGenetico.populacao[i])
print("melhor", r.melhor_solucao.nota_avaliacao)


"""
soma = r.soma_avaliacoes()
 
for individuo_criados in range(0,algoritmoGenetico.len_populacao(), 2):
    pai1 = algoritmoGenetico.seleciona_pai(soma)
    pai2 = algoritmoGenetico.seleciona_pai(soma)


print(pai1)
print(pai2)
"""














