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

def generate_individual():
    individual = []
    for disciplina in disciplines:
        for aulas in disciplina.list_classes:
            individual.append([aulas.id, random.randint(0,1)])
    print(len(individual))

    return individual


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
    
    disp = GeradorObject.recreateDisciplines(disciplines,dList,individual,QUANTIDADE_AULAS_POR_DISCIPLINA)
    #print()
    print(disp[0].list_classes[0].horario.id, disp[0].list_classes[1].horario.id)

    #ativacoes = lista_ativacoes
    result = R1(disciplines,100,10)
    #import pdb; pdb.set_trace()
    #print()
    return  result / 1000,0

# registra a função de ativação
toolbox.register("evaluate", fitness_function)

def crossOverIndividual(ind1,ind2):
    size = min(len(ind1), len(ind2))
    cxpoint = random.randint(1, size - 1)
    ind1[cxpoint:], ind2[cxpoint:] = ind2[cxpoint:], ind1[cxpoint:]
    return ind1,ind2

# realiza o processo de cross over de 1 ponto
toolbox.register("mate", tools.cxOnePoint)

# função de mutação;
toolbox.register("mutate",tools.mutFlipBit, indpb=0.04)

# seleciona o melhor individuo da geração pelo metodo da roleta
# individuo com maior nota tem maior probabilidade de ser escolhido
toolbox.register("select", tools.selRoulette)

random.seed(1)

populacao = toolbox.population(n=1)
probabilidade_crossver = 1.0
probabilidade_mutacao = 0.10
numero_geracoes=0

estatisticas = tools.Statistics(key=lambda individuo: individuo.fitness.values)
estatisticas.register("max", numpy.max)
estatisticas.register("avg", numpy.mean, axis=0)
estatisticas.register("std", numpy.std, axis=0)
estatisticas.register("min", numpy.min, axis=0)
populacao, info = algorithms.eaSimple(populacao,toolbox,
                    probabilidade_crossver,probabilidade_mutacao,
                    numero_geracoes,estatisticas)

melhores = tools.selBest(populacao,1)

#valores_grafico = info.select("max")
#plt.plot(valores_grafico)
#plt.title('Acompanhamento dos valores')
#plt.show()