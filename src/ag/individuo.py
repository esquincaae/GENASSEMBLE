import random

def generar_individuo(tareas, num_estaciones, estaciones_tipos):
    tareas_copia = tareas.copy()
    random.shuffle(tareas_copia)
    estaciones = [[] for _ in range(num_estaciones)]
    for t in tareas_copia:
        est = random.choice(estaciones)
        est.append(t)
    return estaciones