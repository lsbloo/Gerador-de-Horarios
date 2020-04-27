###

from settings.settings_socket import SERVER_PORT,SERVER_HOST

import asyncio
import websocket
from websocket import create_connection
import json
import httputil
from datetime import date

url_teste = "ws://"

import cherrypy
import pandas as pd

class MyProcessor(object):         
    def run(self, df):
        return df.agg(['mean', 'min', 'max'])

class SenderData(object):
    def __init__(self,name):
        self.name=name 
    
    
    @staticmethod
    def sender(data_set):
        if self.name == 'disciplines':
            # sender data disciplines json for line archive create.
            pass

    
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


           return cherrypy.response.body




myprocessor = MyProcessor()

if __name__ == '__main__':
    config = {'server.socket_host': '0.0.0.0','server.socket_port': 8084}
    cherrypy.config.update(config)
    cherrypy.quickstart(KitKatWebService())
