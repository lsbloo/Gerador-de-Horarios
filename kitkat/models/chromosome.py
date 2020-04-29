

"""
Representa o cromossomo contido no individuo.
"""
class Chromosome(object):
    def __init__(self,id,discipline):
        self.id=id
        self.discipline=discipline
    
    def get_id(self):
        return self.id
    
    def setter_id(self,id_setter):
        self.id = id_setter
