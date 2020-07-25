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
  
    def export_csv_by_type(self,typex,dataset):
        with open(self.pathx+folder_input+CONST_EXPORT+"/"+typex+"-t1"+".csv", mode="w") as export_file:
            export_file_writer = csv.writer(export_file,delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            export_file_writer.writerow(["nome","curso","periodo","horario1", "horario2"])
            for disciplina in dataset:
                export_file_writer.writerow([disciplina.name,disciplina.curso,disciplina.periodo,disciplina.list_classes[0].horario.id,disciplina.list_classes[1].horario.id])
        export_file.close()
    def export_graphic(self,graphic):
        graphic.savefig(self.pathx+folder_input+CONST_EXPORT+"/"+"graphic_best")

    def export_time_process(self,num_individual,num_geracao,taxa_mutacao,cruzamento,time_minutos,quantity_violations,indices):
        
        with open(self.pathx+folder_input+CONST_EXPORT+"/time_execution.txt", mode="w") as outfile:
            outfile.write("Quantidade De Individuos: %d "%(num_individual))
            outfile.write("\nQuantidade De Gerações:%d "%(num_geracao))
            outfile.write("\nTaxa De Mutação:%0.2f"%(taxa_mutacao))
            outfile.write("\nCruzamento: %s "%(cruzamento))
            outfile.write("\nTempo de Execução (Minutos): %d "%(time_minutos))
            outfile.write("\nQuantidade de restrições violadas: %d"%(quantity_violations))
            outfile.write("\nRestrição indices:numero de violações: %s :"%(indices))
        outfile.close()

    