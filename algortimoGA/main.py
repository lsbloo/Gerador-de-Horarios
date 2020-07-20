from settings_global.setting_global import SERVER_PORT,SERVER_HOST,URL_HORARIO,URL_DISCIPLINA,URL_SALA
import subprocess
import os
import random
import numpy
import json
import pickle
from sendrequest import SenderRequest
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import matplotlib.pyplot as plt
from ativacoes import R1
import sys
import time
from helper import helpy
from readercsv import ImportCsv
from geratores import GeradorObject
from doenv import loadenv

loadenv()


disciplina = "disciplines.csv"
horario = "horarios.csv"
sala = "salas.csv"

def kitkatGA(populacao,numero_geracoes,taxa_mutacao,crossover):
    QUANTIDADE_AULAS_POR_DISCIPLINA = 2
    
    disciplines = GeradorObject.generate_disciplines(QUANTIDADE_AULAS_POR_DISCIPLINA)
    
    QUANTIDADE_DISCIPLINAS = len(disciplines)
    
    QUANTIDADE_AULAS = QUANTIDADE_DISCIPLINAS * QUANTIDADE_AULAS_POR_DISCIPLINA

    pesos = (-1.0,)

    toolbox = base.Toolbox()
    # define a função de avaliação com os pesos 1 (solução otima) , 0 (solução pessima)
    creator.create("FitnessMin", base.Fitness, weights=pesos)


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
        # recria as disciplinas de acordo com a representação de horarios do individuo
        disp = GeradorObject.recreateDisciplines(disciplines,dList,individual,QUANTIDADE_AULAS_POR_DISCIPLINA)
        ativacoes =[]
        ativacoes.append(R1(disp))
        
        valuesx = []
        for i in range(len(ativacoes)):
            valuesx.append(ativacoes[i].get('violations'))
        
        return valuesx
        
    
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

    populacao, info = algorithms.eaSimple(populacao,toolbox,
                        probabilidade_crossver,probabilidade_mutacao,
                        num_geracoes,estatisticas)


    melhor = tools.selBest(populacao,1)
    #print(melhor[0].fitness.values)
    
    valores_grafico = info.select("min")
    plt.plot(valores_grafico)
    plt.title('Acompanhamento dos valores')
    plt.show()


    #print(melhor[0])

    """
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
    """
    

def main():
    args=[]
    for parameter in sys.argv[1:]:
        args.append(parameter)
    
    if len(args) != 0:
        if args[0] == "--help":
            helpy()
        elif args[0] == "import" and len(args) == 4:
            csvImport = ImportCsv()
            senderData = SenderRequest()

            if args[1] == disciplina and args[2] == horario and args[3] == sala:
                list_horarios = csvImport.readerHorario(horario)
                list_parsed =[]
                for horarios in list_horarios:
                    list_parsed.append(horarios.get())
                senderData.senderHorarios(URL_HORARIO,list_parsed)
                list_disciplinas = csvImport.readerDisciplina(disciplina)
                list_disciplines_parsed = []
                for disp in list_disciplinas:
                    list_disciplines_parsed.append(disp.get())
                senderData.senderDisciplina(URL_DISCIPLINA,list_disciplines_parsed)
                
                list_salas = csvImport.readerSala(sala)
                list_sala_parsed = []
                for salax in list_salas:
                    list_sala_parsed.append(salax.get())
                senderData.senderSala(URL_SALA,list_sala_parsed)

        elif args[0] == "run":
            print("Configuração Algoritmo Genético")
            print()
            populacao = int(input("Número de individuos:"))
            geracoes = int(input("Número de gerações: "))
            mutacao = float(input("Defina a taxa de mutação: "))
            crossover = int(input("Digite (1) para cruzamento de um corte: (2) para cruzamento de dois cortes: "))
            kitkatGA(populacao,geracoes,mutacao,crossover)
            
    else:
        print()
        print("Para obter informações \/")
        print("Digite python3 main.py --help")

main()

