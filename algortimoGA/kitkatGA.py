from settings_global.setting_global import SERVER_PORT,SERVER_HOST,URL_HORARIO,URL_DISCIPLINA,URL_SALA,SERVER_DIRECTORY_SAVE
import subprocess
import os
import random
import numpy
import json
import pickle
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import matplotlib.pyplot as plt
import sys
import time
from ativacoes import R1,R2
from geratores import GeradorObject
from exports.exports import Export

def kitkatGA(populacao,numero_geracoes,taxa_mutacao,crossover):
    numero_individuos = populacao

    QUANTIDADE_AULAS_POR_DISCIPLINA = 2
    
    disciplines = GeradorObject.generate_disciplines(QUANTIDADE_AULAS_POR_DISCIPLINA)
    
    QUANTIDADE_DISCIPLINAS = len(disciplines)
    
    QUANTIDADE_AULAS = QUANTIDADE_DISCIPLINAS * QUANTIDADE_AULAS_POR_DISCIPLINA

    pesos = [1000,1000]

    toolbox = base.Toolbox()
    # define a função de avaliação com os pesos 1 (solução otima) , 0 (solução pessima)
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))


    # define a criação do individuo passando passando a função fitness e os pesos base e o tipo
    # de representação do individuo que neste caso é um array 
    creator.create("Individual", list, fitness=creator.FitnessMin)
    # define o array do individuo com valores aleatorios
    # 

    toolbox.register("attr_item", random.randrange, GeradorObject.get_len_horarios_enumeration())


    # Criação do objeto individuo, parametro tools -> Forma de inicialização, creator -> Classe Invididuo
    # toolbox -> attr_bool, n -> tamanho quantidade de aulas N*2 = N quantidade de disciplinas e N*2 quantidade de aulas
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, n=QUANTIDADE_AULAS)

    #Definição da populacao
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)


    def fitness_function(individual):
        dList = GeradorObject.get_list_horarios_by_enum()
        disp = GeradorObject.recreateDisciplines(disciplines,dList,individual,QUANTIDADE_AULAS_POR_DISCIPLINA)
        ativacoes =[]
        ativacoes.append(R1(disp))
        ativacoes.append(R2(disp))

        result = 0
        for i in range(len(ativacoes)):
            result += ativacoes[i].get('violations') * pesos[i]
        
        
        return result,
        
    
    # registra a função de ativação
    toolbox.register("evaluate", fitness_function)

    if crossover == 1:
        # realiza o processo de cross over de 1 corte
        toolbox.register("mate", tools.cxOnePoint)
    elif crossover == 2:
         # realiza o processo de cross over de 2 cortes
        toolbox.register("mate", tools.cxTwoPoint)

    # função de mutação;
    toolbox.register("mutate",tools.mutUniformInt,low=0,up=GeradorObject.get_len_horarios_enumeration()-1,indpb=0.10)


    """
        Aplica a seleção por Torneio e utiliza do elitismo para preservar
        os melhores individuos das gerações, a ideia é transferir os melhores 
        individuos para geração atual garantindo uma qualidade na solução.

        preserva apenas 10% da solução, e os outros 90% dos individuos
        são selecionados pelo metodo da roleta.
    """
    def selElitistAndTournament(individuals, k, frac_elitist, tournsize):
        return tools.selBest(individuals, int(k*frac_elitist)) + tools.selTournament(individuals, int(k*(1-frac_elitist)), tournsize=tournsize)

    
    
    toolbox.register("select", selElitistAndTournament, frac_elitist=0.1 , tournsize=3)


    populacao = toolbox.population(n=populacao)
    probabilidade_crossver = 1.0
    probabilidade_mutacao = taxa_mutacao
    num_geracoes=numero_geracoes

    estatisticas = tools.Statistics(key=lambda individuo: individuo.fitness.values)
    estatisticas.register("avg", numpy.mean)
    estatisticas.register("std", numpy.std)
    estatisticas.register("min", numpy.min)
    estatisticas.register("max", numpy.max)
    
    t2 = time.time()
    populacao, info = algorithms.eaSimple(populacao,toolbox,
                        probabilidade_crossver,probabilidade_mutacao,
                        num_geracoes,estatisticas)


    melhor = tools.selBest(populacao,1)
    
    valores_grafico = info.select("min")
    plt.plot(valores_grafico)
    plt.title('Acompanhamento dos valores')
    print()
    dList = GeradorObject.get_list_horarios_by_enum()
    melhor = GeradorObject.recreateDisciplines(disciplines,dList,melhor[0],QUANTIDADE_AULAS_POR_DISCIPLINA)
    lcc_list = []
    si_list = []
    for i in melhor:
        if i.curso == "lcc":
            lcc_list.append(i)
        else:
            si_list.append(i)
    s = lcc_list
    l = si_list
    lcc_list = sorted(s,key=lambda discipline: discipline.periodo, reverse=False)
    si_list = sorted(l,key= lambda discipline: discipline.periodo, reverse=False)

    

    temp2 = time.time() - t2
    minutos = temp2/60
    exportador = Export(SERVER_DIRECTORY_SAVE)
    
    exportador.export_csv_by_type("si", si_list) 
    exportador.export_csv_by_type("lcc", lcc_list)
    exportador.export_graphic(plt)
    if crossover == 1:
        exportador.export_time_process(numero_individuos,num_geracoes,taxa_mutacao,"Cruzamento um corte",minutos)
    else:
        exportador.export_time_process(numero_individuos,num_geracoes,taxa_mutacao,"Cruzamento dois cortes",minutos)
    print()
    print("Melhores resultados enviados para: "+SERVER_DIRECTORY_SAVE+"folders_kitkat/exports !")