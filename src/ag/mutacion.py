import random
import copy

def mutacion(estaciones, num_estaciones):
    nuevo = copy.deepcopy(estaciones)
    if random.random() < 0.5:
        origenes = [i for i, est in enumerate(nuevo) if est]
        if not origenes:
            return nuevo
        origen = random.choice(origenes)
        destino = random.choice(range(num_estaciones))
        if nuevo[origen]:
            t = random.choice(nuevo[origen])
            nuevo[origen].remove(t)
            nuevo[destino].append(t)
    else:
        est_idx = random.choice(range(num_estaciones))
        est = nuevo[est_idx]
        if len(est) > 1:
            i1, i2 = random.sample(range(len(est)), 2)
            est[i1], est[i2] = est[i2], est[i1]
    return nuevo

