class Discipline(object):
    def __init__(self,name,curso,periodo,id,credito,professor,list_classes):
        self.name=name
        self.curso=curso
        self.periodo=periodo
        self.id=id
        self.credito=credito
        self.professor=professor

        ### Lista da Grade Aulas em uma disciplina. GENOMA
        self.list_classes=list_classes
    

    def horarios_disponiveis(self):
        q = " "
        for i in self.list_classes:
            
            q+= i.horario.toString()
            q+=","
        return q

    def toString(self):
        return "Disciplina: {name}, Curso: {curso}, Periodo: {periodo}, Professor: {professor}, \n Horarios: {horario}".format(name=self.name,
        curso=self.curso,periodo=self.periodo,professor=self.professor,horario=self.horarios_disponiveis())
    
    def get_id(self):
        return self.id


    def setter_id(self,id_setter):
        self.id=id_setter
from random import random

"""
    Representa as aulas (Genes) AULA
"""
class Classes(object):

    def __init__(self,idx,codigo,capacidade):
        self.codigo=codigo
        self.capacidade=capacidade
        self.id=idx
        self.horario = 0
    
    def set_horario(self,horario):
        self.horario=horario
    
    def get_horario(self):
        return self.horario
    

    def get_id(self):
        return self.id
    
    def set_id(self,id_setter):
        self.id = id_setter

class Horario(object):
    def __init__(self,id,codigo,sequencia):
        self.id=id
        self.codigo=codigo
        self.sequencia = sequencia
    
    def toString(self):
        return "\n Dia: {id} : codigo: {codigo} : sequencia: {sequencia}".format(id=self.id,codigo=self.codigo,sequencia=self.sequencia)
        