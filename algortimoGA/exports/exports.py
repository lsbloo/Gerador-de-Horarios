## modulo responsavel pelo processo de exportação dos quadros gerados do melhor individuo.
## tem como responsabilidade exportar os arquivos csv correspondente aos cursos, como também o grafico de valores do melhor individuo.

import csv
import os
import sys
from os import path

CONST_EXPORT = "exports"
folder_input='folders_kitkat/'

class Export(object):
    def __init__(self, pathx):
        self.pathx = pathx
        if not self.verify(pathx):
            self.file_created_at = os.mkdir(self.pathx+folder_input+CONST_EXPORT)
        

    def verify(self,pathx):
        if path.exists(self.pathx+folder_input+CONST_EXPORT):
            return True
        return False
    """
    exporta 
    """
    def export_csv_by_type(self,typex,dataset):
        with open(self.pathx+folder_input+CONST_EXPORT+"/"+typex+"-t1"+".csv", mode="w") as export_file:
            export_file_writer = csv.writer(export_file,delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for disciplina in dataset:
                export_file_writer.writerow([disciplina.name,disciplina.curso,disciplina.periodo,disciplina.list_classes[0].horario.id,disciplina.list_classes[1].horario.id])

    def export_graphic(self,graphic):
        graphic.savefig(self.pathx+folder_input+CONST_EXPORT+"/"+"best")
        
    