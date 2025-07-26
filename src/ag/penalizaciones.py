from src.gui import graph as graph

import random
import numpy as np

PENALIZACION_PRECEDENCIA = 3
PENALIZACION_EXCESO_TAREAS = 10
PENALIZACION_DESEQUILIBRIO = 10
MAX_TAREAS_POR_ESTACION = 3
PENALIZACION_ESTACION_VACIA = 15 

def evaluar_precedencias(estaciones, dependencias, infoTareas):
    orden_global = [t for est in estaciones for t in est]
    pos = {t:i for i,t in enumerate(orden_global)}
    penal = 0
    for tarea, deps in dependencias.items():
        for d in deps:
            if pos[d] > pos[tarea]:
                penal += PENALIZACION_PRECEDENCIA * infoTareas[tarea]['tiempo']
    return penal

def evaluar_exceso_tareas(estaciones):
    penal = 0
    for est in estaciones:
        exceso = max(0, len(est) - MAX_TAREAS_POR_ESTACION)
        penal += exceso * PENALIZACION_EXCESO_TAREAS
    return penal

def evaluar_balanceo(estaciones, infoTareas):
    cargas = [sum(infoTareas[t]['tiempo'] for t in est) for est in estaciones]
    desv = np.std(cargas)
    return desv * PENALIZACION_DESEQUILIBRIO

def evaluar_estaciones_vacias(estaciones):
    penal = 0
    estvoid = 0
    for est in estaciones:
        if len(est) == 0:
            estvoid += 1
    penal += estvoid * PENALIZACION_ESTACION_VACIA
    return penal

def evaluar_makespan(estaciones, infoTareas):
    cargas = [sum(infoTareas[t]['tiempo'] for t in est) for est in estaciones]
    return max(cargas)