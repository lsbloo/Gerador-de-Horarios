

"""
 Representa as disciplinas genomas de um cromossomo;
"""
class Discipline(object):

    def __init__(self,name,curso,periodo,id,credito,professor,list_classes):
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

class ListDisciplines(object):
    def __init__(self,list_disciplines):
        self.list_disciplines=list_disciplines
    
    def get_dis(self):
        if self.list_disciplines != None:
            return self.list_disciplines
        return None

    
