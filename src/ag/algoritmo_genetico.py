from src.gui import graph as graph

import random
import numpy as np

PENALIZACION_PRECEDENCIA = 3
PENALIZACION_EXCESO_TAREAS = 10
PENALIZACION_DESEQUILIBRIO = 5
MAX_TAREAS_POR_ESTACION = 3
PENALIZACION_ESTACION_VACIA = 15

def generar_individuo(tareas, num_estaciones):
    tareas_copia = tareas.copy()
    random.shuffle(tareas_copia)
    estaciones = [[] for _ in range(num_estaciones)]
    for t in tareas_copia:
        random.choice(estaciones).append(t)
    return estaciones

def evaluar_precedencias(estaciones, dependencias, tiempos):
    orden_global = [t for est in estaciones for t in est]
    pos = {t:i for i,t in enumerate(orden_global)}
    penal = 0
    for tarea, deps in dependencias.items():
        for d in deps:
            if pos[d] > pos[tarea]:
                penal += PENALIZACION_PRECEDENCIA * tiempos[tarea]
    return penal

def evaluar_exceso_tareas(estaciones):
    penal = 0
    for est in estaciones:
        exceso = max(0, len(est) - MAX_TAREAS_POR_ESTACION)
        penal += exceso * PENALIZACION_EXCESO_TAREAS
    return penal

def evaluar_balanceo(estaciones, tiempos):
    cargas = [sum(tiempos[t] for t in est) for est in estaciones]
    desv = np.std(cargas)
    print(f"desviacion estandar = {desv:.2f}")
    return desv * PENALIZACION_DESEQUILIBRIO

def evaluar_estaciones_vacias(estaciones):
    penal = 0
    estvoid = 0
    for est in estaciones:
        if len(est) == 0:
            estvoid += 1
    penal += estvoid * PENALIZACION_ESTACION_VACIA
    return penal

def evaluar_makespan(estaciones, tiempos):
    cargas = [sum(tiempos[t] for t in est) for est in estaciones]
    return max(cargas)