import random

def emparejamiento(poblacion, porcentaje=0.25):
    """Selecciona un porcentaje de la población para formar parejas todos-con-todos."""
    num_seleccionados = max(2, int(len(poblacion) * porcentaje))
    seleccionados = random.sample(poblacion, num_seleccionados)
    parejas = []
    for i in range(num_seleccionados):
        for j in range(i + 1, num_seleccionados):
            parejas.append((seleccionados[i], seleccionados[j]))
    return parejas

