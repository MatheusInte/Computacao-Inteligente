import numpy as np
import matplotlib.pyplot as plt
import math

def funcao_sphere(vetor):
    resultado = 0
    for cont in vetor:
        resultado += cont**2
    return resultado

def funcao_rastrigin(vetor):
    resultado = 0
    for cont in vetor:
        numero = 2 * 3.1415 * cont
        angulo = (numero/180) * math.pi
        resultado += (cont**2) - (10 * math.cos(angulo)) + 10
    return resultado

def funcao_rosenbrock(vetor):
    resultado = 0
    for cont in range(0,(len(vetor) - 1)):
        resultado += 100 * (vetor[cont + 1] - vetor[cont]**2)**2 + (vetor[cont] - 1)**2
    return resultado

class Particula:
    def __init__(self, dimensao, limites):
        self.posicao = np.random.uniform(limites[0], limites[1], dimensao)
        self.velocidade = np.random.uniform(-1, 1, dimensao)
        self.melhor_posicao = np.copy(self.posicao)
        self.melhor_valor = float('inf')

    def atualizar_velocidade(self, melhor_global, w, c1, c2):
        r1 = np.random.random(self.posicao.shape)
        r2 = np.random.random(self.posicao.shape)
        cognitivo = c1 * r1 * (self.melhor_posicao - self.posicao)
        social = c2 * r2 * (melhor_global - self.posicao)
        self.velocidade = w * self.velocidade + cognitivo + social

    def atualizar_posicao(self, limites):
        self.posicao += self.velocidade
        self.posicao = np.clip(self.posicao, limites[0], limites[1])

def pso(funcao_fitness, dimensao, num_particulas, iteracoes, limites, w, w_max, w_min, c1, c2):
    particulas = [Particula(dimensao, limites) for _ in range(num_particulas)]
    melhor_global = np.copy(particulas[0].posicao)
    melhor_valor_global = float('inf')
    historico_fitness = []

    for t in range(iteracoes):
        for particula in particulas:
            valor_fitness = funcao_fitness(particula.posicao)
            if valor_fitness < particula.melhor_valor:
                particula.melhor_valor = valor_fitness
                particula.melhor_posicao = np.copy(particula.posicao)

            if valor_fitness < melhor_valor_global:
                melhor_valor_global = valor_fitness
                melhor_global = np.copy(particula.posicao)

        w = w_max - ((w_max - w_min) * t / iteracoes)  # Atualiza o valor de inércia
        for particula in particulas:
            particula.atualizar_velocidade(melhor_global, w, c1, c2)
            particula.atualizar_posicao(limites)

        historico_fitness.append(melhor_valor_global)

    return melhor_valor_global, melhor_global, historico_fitness, particulas


dimensao = 10
num_particulas = 50
iteracoes = 300
limites = (-5.12, 5.12)
w = 1
w_max = 1
w_min = 0.3
c1 = 2.05
c2 = 2.05

funcoes = {
    'sphere': funcao_sphere,
    'rastrigin': funcao_rastrigin,
    'rosenbrock': funcao_rosenbrock
}

funcao_escolhida = 'rastrigin' 

cenarios_resultados = []
for _ in range(30):
    melhor_valor, _, _, _ = pso(funcoes[funcao_escolhida], dimensao, num_particulas, iteracoes, limites, w, w_max, w_min, c1, c2)
    cenarios_resultados.append(melhor_valor)

cenarios = [cenarios_resultados]

melhor_valor, melhor_posicao, historico_fitness, particulas = pso(
    funcoes[funcao_escolhida], dimensao, num_particulas, iteracoes, limites, w, w_max, w_min, c1, c2)

plt.figure(figsize=(10, 5))
plt.plot(historico_fitness)
plt.title(f'Convergência - {funcao_escolhida}')
plt.xlabel('Iterações')
plt.ylabel('Melhor Valor de Fitness')
plt.grid()
plt.show()