import random
import copy

#Reubicación entre estaciones aleatoria.

def mutacion(hijo, num_estaciones):
    nuevo = copy.deepcopy(hijo)
    origenes = [i for i, est in enumerate(nuevo) if est]
    if not origenes:
        return nuevo
    origen = random.choice(origenes)
    destino = random.choice(range(num_estaciones))
    if nuevo[origen]:
        t = random.choice(nuevo[origen])
        nuevo[origen].remove(t)
        nuevo[destino].append(t)
    return nuevo

