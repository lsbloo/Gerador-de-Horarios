import json
import os

from .settings.settings_local import SERVER_DIRECTORY_SAVE,ARCHIVE_JSON_DISCIPLINES,ARCHIVE_JSON_HORARIOS,ARCHIVE_JSON_SALAS,FOLDER_INPUT


FAIL_PATH_DIR = 'DONT FOUND SERVER DIRECTORY PATH SAVE JSON OBJECTS INPUT'

class GeradorDataSet(object):
    def __init__(self):
        try:
            if SERVER_DIRECTORY_SAVE != FAIL_PATH_DIR:
                self.directory_reader = SERVER_DIRECTORY_SAVE+FOLDER_INPUT
            else:
                print('PATH DONT SET')
                self.directory_reader = None
        
        except Exception as e:
            print(e)
    
    def get_data_disciplines(self):
        if self.directory_reader != None:
            with open(self.directory_reader+ARCHIVE_JSON_DISCIPLINES,'r') as outfile:
                data_set = json.load(outfile)
            
            if data_set!=None:
                return data_set.get('disciplines')
            else:
                return None
        return None
    
    def get_data_horarios(self):
        if self.directory_reader != None:
            with open(self.directory_reader+ARCHIVE_JSON_HORARIOS,'r') as outfile:
                data_set = json.load(outfile)
            
            if data_set!=None:
                return data_set.get('horarios')
            else:
                return None
        return None
    
    def get_data_salas(self):
        if self.directory_reader != None:
            with open(self.directory_reader+ARCHIVE_JSON_SALAS,'r') as outfile:
                data_set = json.load(outfile)
            
            if data_set!=None:
                return data_set.get('salas')
            else:
                return None
        return None

def getInstance():
    return GeradorDataSet()
