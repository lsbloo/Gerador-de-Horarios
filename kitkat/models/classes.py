

"""
    Representa as aulas (Genes)
"""
class Classes(object):

    def __init__(self,sala,horario,dia,id=0):
        self.sala=sala
        self.horario=horario
        self.dia=dia
        self.id=0
    
    def get_id(self):
        return self.id
    
    def set_id(self,id_setter):
        self.id = id_setter
    
