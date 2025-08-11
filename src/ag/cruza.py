import random
'''toma la mitad de p1 y completa con tareas de p2 que no esten ya en el nuevo individuo'''

def cruza(padre1, padre2, prob_cruza):
    if random.random() > prob_cruza:
        # No se cruzan y se devuelve una copia del padre1
        return padre1.copy()

    n = len(padre1)
    mitad = n // 2

    hijo = padre1[:mitad]

    for tarea in padre2:
        if tarea not in hijo:
            hijo.append(tarea)

    return hijo
