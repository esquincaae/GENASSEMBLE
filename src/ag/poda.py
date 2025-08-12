import random
from src.ag.fitness import fitness

def poda(poblacion, dependencias, infoTareas, tam_poblacion, sobrecarga):
    # Eliminar duplicados usando tuplas para poder hash
    poblacion_unica = {}
    for ind in poblacion:
        key = tuple(ind)  # el individuo es una lista de tareas
        poblacion_unica[key] = ind

    poblacion = list(poblacion_unica.values())

    # se ordena la población por fitness (menor es mejor)
    poblacion.sort(key=lambda ind: fitness(ind, dependencias, infoTareas, sobrecarga))

    mejor = poblacion[0] # se guarda el mejor individuo

    if len(poblacion) > tam_poblacion: # si la población es mayor que el tamaño deseado se reduce
        exceso = len(poblacion) - tam_poblacion
        # se eliminan aleatoriamente individuos
        indices_eliminar = random.sample(range(1, len(poblacion)), exceso)
        poblacion = [ind for i, ind in enumerate(poblacion) if i not in indices_eliminar]

    # se asegura que el mejor individuo esté presente
    if mejor not in poblacion:
        poblacion.append(mejor)

    return poblacion
