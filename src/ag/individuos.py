import random

def generar_individuo(tareas, num_estaciones):
    tareas_copia = tareas.copy()
    random.shuffle(tareas_copia)
    estaciones = [[] for _ in range(num_estaciones)]
    for t in tareas_copia:
        random.choice(estaciones).append(t)
    return estaciones