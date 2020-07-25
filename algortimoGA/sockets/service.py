import os
import sys
from os import path
import asyncio
import websocket
from websocket import create_connection
import json
import httputil
from datetime import date
import cherrypy
import pandas as pd
from .settings.setting_socket import SERVER_PORT,SERVER_HOST,SERVER_DIRECTORY_SAVE
from threading import Thread



FAIL_PATH_DIR = 'DONT FOUND SERVER DIRECTORY PATH SAVE JSON OBJECTS INPUT'
FAIL_SERVER_PORT='DONT FOUND SERVER.PORT'
FAIL_SERVER_HOST='DONT FOUND SERVER.HOST'

folder_input='folders_kitkat/'
archive_json_disciplines='disciplines.txt'
archive_json_horarios='horarios.txt'
archive_json_sala='salas.txt'

if SERVER_DIRECTORY_SAVE != FAIL_PATH_DIR:
    print("alouuu")
    dirx = SERVER_DIRECTORY_SAVE+folder_input
    archives = [archive_json_disciplines,archive_json_horarios,archive_json_sala]
    for i in range(3):
        file = open(dirx+archives[i],"w")
        file.write('')
        file.close()


class ThreadService(Thread):
    def __init__(self,pool,start_service,filex):
        super(ThreadService, self).__init__()
        self.pool=pool
    
    def run(self):
        self.pool.map(start_service,filex)


class MyProcessor(object):         
    def run(self, df):
        return df.agg(['mean', 'min', 'max'])

class SenderData(object):
    def __init__(self,name):
        try:
            self.name=name
            self.dir=None
            if SERVER_DIRECTORY_SAVE != FAIL_PATH_DIR:
                self.dir = SERVER_DIRECTORY_SAVE+folder_input
                re = self.check_path()
                if re: 
                    print('Folder created! .')
                else:
                    os.mkdir(self.dir)
        except Exception as e:
            print('SenderData Sender: ', e)


    
    def check_path(self):
        if self.dir != None:
            if  path.exists(self.dir):
                return True
        return False

    def createJsonArchive(self,param):
        if self.dir != None:
            f = open(self.dir+param,"w+")
            return f
        return None


    def sender(self,data_set):
        if self.name == 'disciplines':
            f = self.createJsonArchive(archive_json_disciplines)
            if f != None:
                with open(self.dir+archive_json_disciplines, 'w') as outfile:
                    json.dump(data_set,outfile)
                    return True
            
        elif self.name == 'horarios':

            f = self.createJsonArchive(archive_json_horarios)
            if f != None:
                with open(self.dir+archive_json_horarios, 'w') as outfile:
                    json.dump(data_set,outfile)
                    return True
        else:
            f = self.createJsonArchive(archive_json_sala)
            if f != None:
                with open(self.dir+archive_json_sala,'w') as outfile:
                    json.dump(data_set,outfile)
                    return True
        return False

    
def get_time_today():
    return str(date.today)



"""
    Simple WebService. Receiver and Send informations of genetic soluction;
"""
class KitKatWebService(object):

   @cherrypy.expose
   @cherrypy.tools.json_out()
   @cherrypy.tools.json_in()
   def discipline(self):
       data = cherrypy.request.json
       
       if len(data) == 0:
           cherrypy.response.status = "404 NOT FOUND"
           cherrypy.response.header_list = [("Content-Type", 'application/json'),("Server", "KitKatWebService"),("Content-Length", "0"),]
           cherrypy.response.body = {"error" :'Nenhuma informação sobre disciplinas encontradas'}
           
           return cherrypy.response.body
       else:
           cherrypy.response.status = "200 OK"
           cherrypy.response.header_list = [("Content-Type", 'application/json'),("Server", "KitKatWebService"),("Content-Length", "0"),]
           obj_sender = SenderData('disciplines')
           res = obj_sender.sender(data)
           if res:
                cherrypy.response.body = {"success" :'Dados alimentados com sucesso',"message": "Sender Discipline OK"}
           else:
               cherrypy.response.body = {"success" :'Erro ao inserir dados do tipo disciplina',"message": "Sender Discipline FAIL"}
           return cherrypy.response.body
    
   @cherrypy.expose
   @cherrypy.tools.json_out()
   @cherrypy.tools.json_in()
   def horario(self):
       data = cherrypy.request.json
       if len(data) == 0:
           cherrypy.response.status = "404 NOT FOUND"
           cherrypy.response.header_list = [("Content-Type", 'application/json'),("Server", "KitKatWebService"),("Content-Length", "0"),]
           cherrypy.response.body = {"error" :'Nenhuma informação sobre os horarios encontrados'}
           return cherrypy.response.body
       else:
           cherrypy.response.status = "200 OK"
           cherrypy.response.header_list = [("Content-Type", 'application/json'),("Server", "KitKatWebService"),("Content-Length", "0"),]
           obj_sender = SenderData('horarios')
           res = obj_sender.sender(data)
           if res:
                cherrypy.response.body = {"success" :'Dados alimentados com sucesso',"message": "Sender Horarios OK"}
           else:
               cherrypy.response.body = {"success" :'Erro ao inserir dados do tipo Horário',"message": "Sender Horarios FAIL"}
           return cherrypy.response.body
    
   @cherrypy.expose
   @cherrypy.tools.json_out()
   @cherrypy.tools.json_in()
   def sala(self):
       data = cherrypy.request.json
       if len(data) == 0:
           cherrypy.response.status = "404 NOT FOUND"
           cherrypy.response.header_list = [("Content-Type", 'application/json'),("Server", "KitKatWebService"),("Content-Length", "0"),]
           cherrypy.response.body = {"error" :'Nenhuma informação sobre as salas encontradas'}
           return cherrypy.response.body
       else:
           cherrypy.response.status = "200 OK"
           cherrypy.response.header_list = [("Content-Type", 'application/json'),("Server", "KitKatWebService"),("Content-Length", "0"),]
           obj_sender = SenderData('salas')
           res = obj_sender.sender(data)
           if res:
                cherrypy.response.body = {"success" :'Dados alimentados com sucesso',"message": "Sender Salas OK"}
           else:
               cherrypy.response.body = {"success" :'Erro ao inserir dados do tipo Sala',"message": "Sender Salas FAIL"}
           return cherrypy.response.body



"""
 -Init KitKat WebService.
"""
def quickstart():
    print(str(SERVER_HOST))
    print(str(SERVER_PORT))

    configuration = {
        "server.socket_host": str(SERVER_HOST), 
        "server.socket_port": int(SERVER_PORT)
    }

    cherrypy.config.update(configuration)
    cherrypy.quickstart(KitKatWebService())