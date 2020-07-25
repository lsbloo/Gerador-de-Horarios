from settings_global.setting_global import SERVER_PORT,SERVER_HOST,URL_HORARIO,URL_DISCIPLINA,URL_SALA,SERVER_DIRECTORY_SAVE
from settings_global.setting_global import DISCIPLINA_CSV,HORARIO_CSV,SALA_CSV
from sendrequest import SenderRequest
from helper import helpy
from readercsv import ImportCsv
from doenv import loadenv
import figlet
import sys
import argparse
loadenv()

def helper():
    args=[]
    for parameter in sys.argv[1:]:
        args.append(parameter)
    if len(args) != 0:
        if args[0] == "--man":
            helpy()
            quit()

def importData():
    args=[]
    for parameter in sys.argv[1:]:
        args.append(parameter)
    if len(args) != 0:
        if args[0] == "import" and len(args) == 4:
            csvImport = ImportCsv()
            senderData = SenderRequest()
            if args[1] == DISCIPLINA_CSV and args[2] == HORARIO_CSV and args[3] == SALA_CSV:
                    list_horarios = csvImport.readerHorario(HORARIO_CSV)
                    list_parsed =[]
                    for horarios in list_horarios:
                        list_parsed.append(horarios.get())
                    senderData.senderHorarios(URL_HORARIO,list_parsed)
                    list_disciplinas = csvImport.readerDisciplina(DISCIPLINA_CSV)
                    list_disciplines_parsed = []
                    for disp in list_disciplinas:
                        list_disciplines_parsed.append(disp.get())
                    senderData.senderDisciplina(URL_DISCIPLINA,list_disciplines_parsed)
                    list_salas = csvImport.readerSala(SALA_CSV)
                    list_sala_parsed = []
                    for salax in list_salas:
                        list_sala_parsed.append(salax.get())
                    senderData.senderSala(URL_SALA,list_sala_parsed)
                    quit()




def run(args):
    populacao = args.i
    geracoes = args.g
    mutacao = args.m
    cruzamento = args.c
    if populacao != None and geracoes != None and mutacao != None and cruzamento != None:
        from kitkatGA import kitkatGA
        kitkatGA(populacao,geracoes,mutacao,cruzamento)
    else:
        print()
        print('Configuração do algoritmo genético invalida. ')
        print()
        print('Digite python3 main.py --man para exemplo configuração')
        print('Digite python3 main.py -h para visualizar configurações do algoritmo genetico.')
        quit()


def main():
    helper()
    importData()

    parser = argparse.ArgumentParser(description="Configuração de execução do algoritmo genético", epilog="digite python3 main.py --man para visualizar o manual. Digite python3 main.py -h para visualizar configurações do algoritmo genetico.")
    parser.add_argument("-i",help="Define a quantidade de individuos, número inteiro", type=int)
    parser.add_argument("-g", help="Define o número de gerações, número inteiro", type=int)
    parser.add_argument("-m",help="Define a taxa de mutação em porcentagem Ex: 0.10", type=float)
    parser.add_argument("-c", help="Define os tipos de cruzamento Digite(1) para cruzamento de um corte ou (2) para cruzamento de dois cortes, número inteiro ", type=int)

    args = parser.parse_args()
    run(args)

if __name__=="__main__":
    main()