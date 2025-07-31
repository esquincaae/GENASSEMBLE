from src.gui import graph as graph

import random
import numpy as np

PENALIZACION_PRECEDENCIA = 3
PENALIZACION_DESEQUILIBRIO = 10
PENALIZACION_MEZCLA_TIPOS = 100 

def evaluar_precedencias(estaciones, dependencias, infoTareas):
    orden_global = [t for est in estaciones for t in est]
    pos = {t:i for i,t in enumerate(orden_global)}
    penal = 0
    for tarea, deps in dependencias.items():
        for d in deps:
            if pos[d] > pos[tarea]:
                penal += PENALIZACION_PRECEDENCIA * infoTareas[tarea]['tiempo']
    return penal

def evaluar_balanceo(estaciones, infoTareas):
    cargas = [sum(infoTareas[t]['tiempo'] for t in est) for est in estaciones]
    desv = np.std(cargas)
    return desv * PENALIZACION_DESEQUILIBRIO

def penalizar_mezcla_tipos(estaciones, infoTareas):
    # Penaliza si en una estación hay tareas de más de un tipo
    penal = 0
    for est in estaciones:
        tipos = {infoTareas[t]['tipo'] for t in est}
        if len(tipos) > 1:
            penal += PENALIZACION_MEZCLA_TIPOS
    return penal

def evaluar_makespan(estaciones, infoTareas):
    cargas = [sum(infoTareas[t]['tiempo'] for t in est) for est in estaciones]
    return max(cargas)