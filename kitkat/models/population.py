

"""
 Representa cada população criada a partir de uma geração.
"""
class Population(object):
    def __init__(self,list_individuals, id = 0):
        self.list_individuals=list_individuals
        self.id=id
    
    
    def get_id(self):
        return self.id
    def setter_id(self,id_setter):
        self.id=id_setter
