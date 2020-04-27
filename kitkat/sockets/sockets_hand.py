###

from settings.settings_socket import SERVER_PORT,SERVER_HOST,SERVER_DIRECTORY_SAVE
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


FAIL_PATH_DIR = 'DONT FOUND SERVER DIRECTORY PATH SAVE JSON OBJECTS INPUT'
FAIL_SERVER_PORT='DONT FOUND SERVER.PORT'
FAIL_SERVER_HOST='DONT FOUND SERVER.HOST'

folder_input='folders_kitkat/'
archive_json_disciplines='disciplines.txt'

class MyProcessor(object):         
    def run(self, df):
        return df.agg(['mean', 'min', 'max'])

class SenderData(object):
    def __init__(self,name):
        try:
            self.name=name
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

    def createJsonArchive(self):
        if self.dir != None:
            f = open(self.dir+archive_json_disciplines,"w+")
            return f
        return None
    
    def sender(self,data_set):
        
        if self.name == 'disciplines':
            # sender data disciplines json for line archive create.
            f = self.createJsonArchive()
            if f != None:
                with open(self.dir+archive_json_disciplines, 'w') as outfile:
                    json.dump(data_set,outfile)
                    print('Sender Disciplines OK')

    
def get_time_today():
    return str(date.today)


class KitKatWebService(object):

   @cherrypy.expose
   @cherrypy.tools.json_out()
   @cherrypy.tools.json_in()
   def process(self):
      data = cherrypy.request.json
      df = pd.DataFrame(data)
      output = myprocessor.run(df)
      return output.to_json()

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
           cherrypy.response.body = {"success" :'Dados alimentados com sucesso'}
           obj_sender = SenderData('disciplines')
           obj_sender.sender(data)
           return cherrypy.response.body


    

myprocessor = MyProcessor()

if __name__ == '__main__':
    config = {'server.socket_host': '0.0.0.0','server.socket_port': 8084}
    cherrypy.config.update(config)
    cherrypy.quickstart(KitKatWebService())
