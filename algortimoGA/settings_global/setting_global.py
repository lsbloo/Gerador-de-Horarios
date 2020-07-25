### Configurações Default
import os

# Configuration SERVER PORT
SERVER_PORT = os.environ.get('SERVER_PORT', 'DONT FOUND SERVER.PORT')
SERVER_HOST = os.environ.get('SERVER_HOST', 'DONT FOUND SERVER.HOST')




# CONFIGURATION PATH ARCHIVES JSON 
SERVER_DIRECTORY_SAVE = os.environ.get('SERVER_DIRECTORY_SAVE', 'DONT FOUND SERVER DIRECTORY PATH SAVE JSON OBJECTS INPUT')

FOLDER_INPUT='folders_kitkat/'
ARCHIVE_JSON_DISCIPLINES='disciplines.txt'
ARCHIVE_JSON_HORARIOS='horarios.txt'
ARCHIVE_JSON_SALAS='salas.txt'


#URLS
URL_HORARIO="http://%s:%s/%s"%(SERVER_HOST,SERVER_PORT,"horario")
URL_DISCIPLINA="http://%s:%s/%s"%(SERVER_HOST,SERVER_PORT,"discipline")
URL_SALA="http://%s:%s/%s"%(SERVER_HOST,SERVER_PORT,"sala")

# ARCHIVES CSV 
DISCIPLINA_CSV = "disciplines.csv"
HORARIO_CSV = "horarios.csv"
SALA_CSV = "salas.csv"