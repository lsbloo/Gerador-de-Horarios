
class Horario(object):
    def __init__(self,id,codigo,sequencia):
        self.id=id
        self.codigo=codigo
        self.sequencia = sequencia
    
    def toString(self):

        return "\n Dia: {id} : codigo: {codigo} : sequencia: {sequencia}".format(id=self.id,codigo=self.codigo,sequencia=self.sequencia)
        