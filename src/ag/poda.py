import random
from src.ag.fitness import fitness

def poda(poblacion, dependencias, tiempos, tam_poblacion):
    # Eliminar clones: usar tuplas para hashable
    poblacion_unica = {}
    for ind in poblacion:
        key = tuple(tuple(est) for est in ind)
        poblacion_unica[key] = ind

    poblacion = list(poblacion_unica.values())
    poblacion.sort(key=lambda ind: fitness(ind, dependencias, tiempos))
    mejor = poblacion[0]

    if len(poblacion) > tam_poblacion:
        # Eliminamos aleatoriamente excepto el mejor
        exceso = len(poblacion) - tam_poblacion
        indices_eliminar = random.sample(range(1, len(poblacion)), exceso)
        poblacion = [ind for i, ind in enumerate(poblacion) if i not in indices_eliminar]

    # Asegurarse que el mejor esté en la población
    if mejor not in poblacion:
        poblacion.append(mejor)

    return poblacion