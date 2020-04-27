


"""
Representa cada individuo contido em uma população.
"""
class Individual(object):
    def __init__(self,id=0,Chromosome):
        self.id=id
        self.chromosome=Chromosome
    
    def get_id(self):
        return self.id
    
    def setter_id(self,id_setter):
        self.id = id_setter
