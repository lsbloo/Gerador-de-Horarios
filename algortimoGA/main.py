# BIBLIOTECAS CIENTIFICAS
import random
import numpy
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import matplotlib.pyplot as plt
from ativacoes import R1


# GERATOR DE OBJETOS
from geratores import GeradorObject

QUANTIDADE_AULAS_POR_DISCIPLINA = 2

disciplines = GeradorObject.generate_disciplines(QUANTIDADE_AULAS_POR_DISCIPLINA)

QUANTIDADE_DISCIPLINAS = len(disciplines)

QUANTIDADE_AULAS = QUANTIDADE_DISCIPLINAS * QUANTIDADE_AULAS_POR_DISCIPLINA



toolbox = base.Toolbox()
# define a função de avaliação com os pesos 1 (solução otima) , 0 (solução pessima)
creator.create("Fitness", base.Fitness, weights=(1.0,))


# define a criação do individuo passando passando a função fitness e os pesos base e o tipo
# de representação do individuo que neste caso é um array 
creator.create("Individual", list, fitness=creator.Fitness)
# define o array do individuo com valores aleatorios
# 

toolbox.register("attr_item", random.randrange, GeradorObject.get_len_horarios_enumeration())


# Criação do objeto individuo, parametro tools -> Forma de inicialização, creator -> Classe Invididuo
# toolbox -> attr_bool, n -> tamanho quantidade de aulas N*2 = N quantidade de disciplinas e N*2 quantidade de aulas
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, n=QUANTIDADE_AULAS)

#Definição da populacao
toolbox.register("population", tools.initRepeat, list, toolbox.individual)




def fitness_function(individual):
    #print(individual)
    dList = GeradorObject.get_list_horarios_by_enum()
    # recria as disciplinas de acordo com a representação de horarios do individuo
    disp = GeradorObject.recreateDisciplines(disciplines,dList,individual,QUANTIDADE_AULAS_POR_DISCIPLINA)
    #print(disp[0].list_classes[0].horario.id,disp[0].list_classes[1].horario.id)
    #print(disp[0].list_classes[0].horario.id)
    #ativacoes = lista_ativacoes
    result = R1(disp,100,10)
    #import pdb; pdb.set_trace()
    #print()
    return  result / 1000,0

# registra a função de ativação
toolbox.register("evaluate", fitness_function)


# realiza o processo de cross over de 1 ponto
toolbox.register("mate", tools.cxOnePoint)

# função de mutação;
toolbox.register("mutate",tools.mutUniformInt,low=0,up=GeradorObject.get_len_horarios_enumeration()-1,indpb=0.10)



# seleciona o melhor individuo da geração pelo metodo da roleta
# individuo com maior nota tem maior probabilidade de ser escolhido
toolbox.register("select", tools.selRoulette)


populacao = toolbox.population(n=100)
probabilidade_crossver = 1.0
probabilidade_mutacao = 0.10
numero_geracoes=200

estatisticas = tools.Statistics(key=lambda individuo: individuo.fitness.values)
estatisticas.register("max", numpy.max)
estatisticas.register("avg", numpy.mean, axis=0)
estatisticas.register("std", numpy.std, axis=0)
estatisticas.register("min", numpy.min, axis=0)

populacao, info = algorithms.eaSimple(populacao,toolbox,
                    probabilidade_crossver,probabilidade_mutacao,
                    numero_geracoes,estatisticas)


melhor = tools.selBest(populacao,1)

"""
valores_grafico = info.select("max")
plt.plot(valores_grafico)
plt.title('Acompanhamento dos valores')
plt.show()
"""


print(melhor[0])

print()
dList = GeradorObject.get_list_horarios_by_enum()
melhor = GeradorObject.recreateDisciplines(disciplines,dList,melhor[0],QUANTIDADE_AULAS_POR_DISCIPLINA)

lcc_list = []

for i in melhor:
    if i.curso == "lcc":
        lcc_list.append(i)
s = lcc_list
lcc_list = sorted(s,key=lambda discipline: discipline.periodo, reverse=True)
for d in lcc_list:
    print(d.toString())
