

"""
 Representa as disciplinas genomas de um cromossomo;
"""
class Discipline(object):

    def __init__(self,name,curso,periodo,id=0,credito,professor,list_classes):
        self.name=name
        self.curso=curso
        self.periodo=periodo
        self.id=id
        self.credito=credito
        self.professor=professor

        ### Lista da Grade Aulas em uma disciplina. 
        self.list_classes=list_classes
    
    def get_id(self):
        return self.id
    
    def setter_id(self,id_setter):
        self.id=id_setter
    
    
