import random
from individuos_ag import Individuo
from geratores import GeradorObject
from random import random as rd

class AlgoritmoGenetico(object):
    def __init__(self,tamanho_populacao):
        self.tamanho_populacao=tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
    
   
    def criar_populacao(self,limite_restricoes):
        for i in range(self.tamanho_populacao):
            dt = GeradorObject.generate_disciplines()
            self.populacao.append(Individuo(dt,limite_restricoes,None))

        self.melhor_solucao = self.populacao[0]
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,key=lambda populacao: populacao.nota_avaliacao,reverse=False)
        
    def selecao(self):
        lista_melhores_individuos=[]
        
             
    def melhor_individuo(self,individuo):
        if individuo.nota_avaliacao  > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
        return self

    
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        
        return soma
    
    #ROLETA
    def seleciona_pai(self,soma_avaliacao):
        pai = -1
        valor_gerador = rd() * soma_avaliacao
        i = 0
        soma=0
        #print(self.populacao)
        while i < len(self.populacao) and soma < valor_gerador:
            soma += self.populacao[i].nota_avaliacao
            #print(soma)
            i+=1
            pai+=1
        
        return pai
        
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("Geração: %s -> Nota Individuo Atual: %s \n  -> Pai: %s " %(self.populacao[0].geracao, melhor.nota_avaliacao,melhor.papai.geracao))



    def resolver(self,limite_restricoes,numero_geracoes,restricoes,taxa_mutacao):
        self.criar_populacao(limite_restricoes)

        for individuo in self.return_populacao():
            individuo.fitness(restricoes)
        
        self.ordena_populacao()

        if numero_geracoes == 0:
            melhor = self.populacao[0]
            q = self.melhor_individuo(melhor)
            return self.melhor_solucao

        else:
            for geracao in range(numero_geracoes):
                soma_avaliacao = self.soma_avaliacoes()
                nova_populacao =[]

                for individuos_gerados in range(0, self.len_populacao(), 2):
                    pai1 = self.seleciona_pai(soma_avaliacao)
                    pai2 = self.seleciona_pai(soma_avaliacao)
                    
                     
                    filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                    

                    nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                    nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
                
                self.populacao = list(nova_populacao)

                for individuo in self.populacao:
                    individuo.fitness(restricoes)
                
                self.ordena_populacao()


                self.visualiza_geracao()

                melhor = self.populacao[0]
                self.melhor_individuo(melhor)

        return self.melhor_solucao



    def len_populacao(self):
        return len(self.populacao)

    def return_only_individuo(self,index):
        return self.populacao[index]
    
    def return_populacao(self):
        return self.populacao
    
