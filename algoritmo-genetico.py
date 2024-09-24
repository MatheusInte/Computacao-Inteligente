import random
import math

def criar_individuo(tamanho_cromossomo, limite_inferior, limite_superior):
    individuo = []
    for _ in range(tamanho_cromossomo):
        individuo.append(random.randint(limite_inferior, limite_superior))
    return individuo

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

def selecao_torneio(populacao, fitness, k=3):
    participantes = random.sample(list(zip(populacao,fitness)), k)
    participantes_ordenados = sorted(participantes, key = lambda x: x[1])
    return participantes_ordenados [0][0]

def selecao_proporcao(populacao, fitness):
    maximo_fitness = max(fitness)
    fitness_invertido = []
    for cont in fitness:
        fitness_invertido.append(maximo_fitness - cont)
    total_fitness = sum(fitness_invertido)
    probabilidade = []
    for cont in fitness_invertido:
        probabilidade.append(cont / total_fitness)
    pais = random.choices(populacao, weights = probabilidade, k = 2)
    return pais

def cruzamento(pai1, pai2, tipo_cruzamento):
    ponto1 = random.randint(1, len(pai1) - 1)
    if tipo_cruzamento == 2:
        ponto2 = random.randint(ponto1, len(pai1) - 1)
        filho1 = pai1[:ponto1] + pai2[ponto1:ponto2] + pai1[ponto2:]
        filho2 = pai2[:ponto1] + pai1[ponto1:ponto2] + pai2[ponto2:]
    else:
        filho1 = pai1[:ponto1] + pai2[ponto1:]
        filho2 = pai2[:ponto1] + pai1[ponto1:]
    return filho1, filho2

def mutacao(individuo, taxa_mutacao, limite_inferior, limite_superior):
    for cont in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[cont] = random.randint(limite_inferior, limite_superior)
    return individuo

def algoritmo_genetico(tamanho_populacao, quantidade_geracoes, taxa_cruzamento, taxa_mutacao, tipo_selecao, tipo_cruzamento, tamanho_cromossomo, limite_inferior, limite_superior, tipo_funcao):
    populacao = []
    for _ in range(tamanho_populacao): 
        populacao.append(criar_individuo(tamanho_cromossomo, limite_inferior, limite_superior))
    melhor_fitness_geracao = []
    melhores_individuos_geracao = []

    for geracao in range(quantidade_geracoes):
        fitness = []
        
        for individuo in populacao:
            fitness.append(tipo_funcao(individuo))
        
        melhor_fitness = min(fitness)
        melhor_individuo = populacao[fitness.index(melhor_fitness)]
        melhor_fitness_geracao.append(melhor_fitness)
        melhores_individuos_geracao.append(melhor_individuo)
        nova_populacao = []

        while len(nova_populacao) < tamanho_populacao:
            if tipo_selecao == 'proporcional':
                pai1,pai2 = selecao_proporcao(populacao, fitness)
            else:
                pai1,pai2 = selecao_torneio(populacao, fitness), selecao_torneio(populacao, fitness)
            
            if random.random() < taxa_cruzamento:
                filho1, filho2 = cruzamento(pai1, pai2, tipo_cruzamento)
            else:
                filho1, filho2 = pai1, pai2
            
            filho1 = mutacao(filho1, taxa_mutacao, limite_inferior, limite_superior)
            filho2 = mutacao(filho2, taxa_mutacao, limite_inferior, limite_superior)
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)

        populacao = nova_populacao[:tamanho_populacao]

    melhor_individuo = populacao[0]
    for individuo in populacao:
        if tipo_funcao(individuo) < tipo_funcao(melhor_individuo):
            melhor_individuo = individuo
        return melhores_individuos_geracao, melhor_fitness_geracao

TAMANHO_POPULACAO = 100
QUANTIDADE_GERACOES = 100
TAXA_CRUZAMENTO = 0.7
TAXA_MUTACAO = 0.05
TIPO_SELECAO = 'selecao_torneio'
TIPO_CRUZAMENTO = 2
TAMANHO_CROMOSSOMO = 30
LIMITE_INFERIOR = -100
LIMITE_SUPERIOR = 100
TIPO_FUNCAO = funcao_rosenbrock

melhores_individuos, historico_fitness = algoritmo_genetico(TAMANHO_POPULACAO, QUANTIDADE_GERACOES, TAXA_CRUZAMENTO, TAXA_MUTACAO, TIPO_SELECAO, TIPO_CRUZAMENTO, TAMANHO_CROMOSSOMO, LIMITE_INFERIOR, LIMITE_SUPERIOR, TIPO_FUNCAO)

print("MELHOR INDIVIDUO: ", melhores_individuos[-1])
