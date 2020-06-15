import random
from individuos_ag import Individuo
from geratores import GeradorObject

class AlgoritmoGenetico(object):
    def __init__(self,tamanho_populacao):
        self.tamanho_populacao=tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
    
   
    def criar_populacao(self,limite_restricoes):
        for i in range(self.tamanho_populacao):
            dt = random.sample(GeradorObject.generate_disciplines(),len(GeradorObject.generate_disciplines()))
            self.populacao.append(Individuo(dt,limite_restricoes,None))

        self.melhor_solucao = self.populacao[0]
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,key=lambda populacao: populacao.nota_avaliacao,reverse=True)
    
    def selecao(self):
        lista_melhores_individuos=[]
        
             
    def melhor_individuo(self,individuo):
        if individuo.nota_avaliacao < self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
        return self

    
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        
        return soma
    
    def seleciona_pai(self,soma_avaliacao):
        pai = -1
        valor_sorteado = rd() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            
            pai += 1
            i +=1
        return pai



    def len_populacao(self):
        return len(self.populacao)

    def return_only_individuo(self,index):
        return self.populacao[index]
    
    def return_populacao(self):
        return self.populacao