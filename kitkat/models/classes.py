

"""
    Representa as aulas (Genes) AULA
"""
class Classes(object):

    def __init__(self,id,codigo,capacidade):
        self.codigo=codigo
        self.capacidade=capacidade
        self.id=0
    
   
    def set_horario(self,horario):
        self.horario=horario
    
    def get_horario(self):
        return self.horario
    

    def get_id(self):
        return self.id
    
    def set_id(self,id_setter):
        self.id = id_setter
    
