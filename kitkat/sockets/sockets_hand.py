###

from settings.settings_socket import SERVER_PORT,SERVER_HOST

import asyncio
import websocket
from websocket import create_connection
import json

url_teste = "ws://"

import cherrypy
import pandas as pd

class MyProcessor(object):         
    def run(self, df):
        return df.agg(['mean', 'min', 'max'])

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
       print(len(data))
       if len(data) == 0:
           cherrypy.response.status = "404 NOT FOUND"
           cherrypy.response.header_list = [("Content-Type", 'application/json'),("Server", "KitKatWebService"),("Date", httputil.HTTPDate()),("Content-Length", "255"),]
           cherrypy.response.body = ["Nenhuma informação sobre disciplinas encontradas"]
           return cherrypy.response





myprocessor = MyProcessor()

if __name__ == '__main__':
    config = {'server.socket_host': '0.0.0.0','server.socket_port': 8084}
    cherrypy.config.update(config)
    cherrypy.quickstart(KitKatWebService())
