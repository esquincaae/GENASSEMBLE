import random
import copy

# Reordena aleatoriamente las tareas dentro de una estación, usando infoTareas para asegurar el tipo
def mutacion(hijo, num_estaciones, infoTareas):
    nuevo = copy.deepcopy(hijo)
    # Selecciona una estación con más de una tarea
    estaciones_mutables = [i for i, est in enumerate(nuevo) if len(est) > 1]
    if not estaciones_mutables:
        return nuevo
    idx = random.choice(estaciones_mutables)
    # Solo reordena tareas del mismo tipo
    tipo_estacion = infoTareas[nuevo[idx][0]]['tipo']
    tareas_tipo = [t for t in nuevo[idx] if infoTareas[t]['tipo'] == tipo_estacion]
    random.shuffle(tareas_tipo)
    nuevo[idx] = tareas_tipo
    return nuevo