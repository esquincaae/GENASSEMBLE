import random
from itertools import combinations

#Selecciona un porcentaje de la población para formar parejas todos-con-todos

def emparejamiento(poblacion, porcentaje=0.5):
    # Seleccionar aleatoriamente un subconjunto de la población
    cantidad = max(2, int(len(poblacion) * porcentaje))
    seleccionados = random.sample(poblacion, cantidad)

    # Generar todas las combinaciones posibles de parejas
    parejas = list(combinations(seleccionados, 2))

    return parejas
