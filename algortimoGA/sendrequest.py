import requests
import json
from models import ModelList

class SenderRequest(object):
    def __init__(self):
        pass
    def decode(self,dump):
        return dump.decode("UTF-8")
    def senderHorarios(self,url,json_data):
        resp = requests.post(url,data=json.dumps(json_data,ensure_ascii=False).encode("UTF-8"),
        headers={'Content-Type': 'application/json'})
        if resp.status_code == 200:
            print('Horarios inseridos com sucesso')
            return True
        print('Não foi possivel enviar os horários')
        return False
    
    def senderDisciplina(self,url,json_data):
        p = []
        for data in json_data:
            p.append(json.loads(self.decode(json.dumps(data,ensure_ascii=False).encode("UTF-8"))))
        
        resp = requests.post(url,data=json.dumps(p), headers={'Content-Type': 'application/json; charset=utf-8'})
        if resp.status_code == 200:
            print('Disciplinas inseridas com sucesso')
            return True
        
        print('Não foi possivel enviar as disciplinas')
        return False
    def senderSala(self,url,json_data):
        resp = requests.post(url,data=json.dumps(json_data,ensure_ascii=False).encode("UTF-8"), headers={'Content-Type': 'application/json'})
        if resp.status_code == 200:
            print('Salas inseridas com sucesso')
            return True
        print('Não foi possivel enviar as salas')
        return False
        

    @staticmethod
    def parsedict(obj):
        if hasattr(obj, '__dict__'):
            obj = obj.__dict__
        if isinstance(obj, dict):
            return { k:para_dict(v) for k,v in obj.items() }
   
        elif isinstance(obj, list) or isinstance(obj, tuple):
            return [para_dict(e) for e in obj]
    
        else: 
            return obj

