import random
import math
import matplotlib.pyplot as plt
import numpy as np

def sphere(vetor):
    return sum(i**2 for i in vetor)

def rastrigin(vetor):
    resultado = 0
    for i in vetor:
        resultado += (i**2) - (10 * math.cos(2 * math.pi * i)) + 10
    return resultado

def rosenbrock(vetor):
    resultado = 0
    for i in range(len(vetor) - 1):
        resultado += 100 * (vetor[i+1] - vetor[i]**2)**2 + (vetor[i] - 1)**2
    return resultado

class Bee:
    def __init__(self, dimension):
        self.position = np.random.uniform(-5, 5, dimension)  # Inicializa a posição aleatoriamente
        self.fitness = float('inf')

tamanho_colonia = 20
fator_abandono = 0.04
funcao_objetivo = sphere  
n_dimensoes = 10
limite_dimensoes = 5
n_ciclos = 1000

def abc_algorithm(tamanho_colonia, fator_abandono, funcao_objetivo, n_dimensoes, limites_dimensoes, n_ciclos):
    bees = [Bee(n_dimensoes) for _ in range(tamanho_colonia)]

    for bee in bees:
        bee.fitness = funcao_objetivo(bee.position)

    best_bee = min(bees, key=lambda b: b.fitness)
    best_position = best_bee.position.copy()
    best_fitness = best_bee.fitness

    fitness_history = []

    for ciclo in range(n_ciclos):
        for i in range(tamanho_colonia):
            new_position = bees[i].position + np.random.uniform(-1, 1, n_dimensoes)
            new_position = np.clip(new_position, limites_dimensoes[0], limites_dimensoes[1])  # Restringe a posição

            new_fitness = funcao_objetivo(new_position)

            if new_fitness < bees[i].fitness:
                bees[i].position = new_position
                bees[i].fitness = new_fitness

                if new_fitness < best_fitness:
                    best_fitness = new_fitness
                    best_position = new_position
            else:
                if np.random.rand() < fator_abandono:
                    bees[i].position = np.random.uniform(limites_dimensoes[0], limites_dimensoes[1], n_dimensoes)
                    bees[i].fitness = funcao_objetivo(bees[i].position)

        fitness_history.append(best_fitness)
        print(f"Ciclo {ciclo + 1}, Melhor Fitness: {best_fitness}")

    return best_position, best_fitness, fitness_history

tamanho_colonia = 30           
fator_abandono = 0.3           
funcao_objetivo = sphere       
n_dimensoes = 10              
limites_dimensoes = [-5, 5]    
n_ciclos = 100 

melhor_posicao, melhor_fitness, fitness_history = abc_algorithm(tamanho_colonia, fator_abandono, funcao_objetivo, n_dimensoes, limites_dimensoes, n_ciclos)