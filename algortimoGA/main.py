from settings_global.setting_global import SERVER_PORT,SERVER_HOST,URL_HORARIO,URL_DISCIPLINA,URL_SALA,SERVER_DIRECTORY_SAVE
from sendrequest import SenderRequest
from helper import helpy
from readercsv import ImportCsv
from doenv import loadenv
import figlet
import sys
loadenv()


disciplina = "disciplines.csv"
horario = "horarios.csv"
sala = "salas.csv"

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
            from kitkatGA import kitkatGA
            kitkatGA(populacao,geracoes,mutacao,crossover)
            
    else:
        print()
        print("Para obter informações \/")
        print("Digite python3 main.py --help")

main()

