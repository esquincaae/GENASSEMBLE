import random

'''se hace una mutacion basada en permutas, tomando dos posiciones al azar'''

def mutacion(individuo, prob_mutacion):
    individuo_mutado = individuo[:]

    if random.random() < prob_mutacion:
        i, j = random.sample(range(len(individuo_mutado)), 2)
        individuo_mutado[i], individuo_mutado[j] = individuo_mutado[j], individuo_mutado[i]

    return individuo_mutado