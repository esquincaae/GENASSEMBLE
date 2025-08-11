import numpy as np

PENALIZACION_PRECEDENCIA = 3
PENALIZACION_DESEQUILIBRIO = 5

def evaluar_precedencias(individuo, dependencias, infoTareas):
    pos = {t: i for i, t in enumerate(individuo)}
    penal = 0
    for tarea, deps in dependencias.items():
        for d in deps:
            # Si la tarea depende de otra que aparece después en el individuo
            # penalizamos por la violación de la precedencia
            if pos.get(d, -1) > pos.get(tarea, -1):
                penal += PENALIZACION_PRECEDENCIA * infoTareas[tarea]['tiempo']
    return penal

def evaluar_balanceo(individuo, infoTareas):
    num_estaciones = 5
    tam_estacion = len(individuo) // num_estaciones
    cargas = []

    for i in range(num_estaciones):
        inicio = i * tam_estacion
        fin = (i + 1) * tam_estacion if i < num_estaciones - 1 else len(individuo)
        estacion = individuo[inicio:fin]

        carga = sum(infoTareas[t]['tiempo'] for t in estacion)
        cargas.append(carga)

    desv = np.std(cargas)
    #print("Cargas por estación:", cargas)
    #print("Desviación estándar:", desv)
    return desv * PENALIZACION_DESEQUILIBRIO

def evaluar_makespan(individuo, infoTareas):
    # Suma total de tiempos (makespan simple)
    return sum(infoTareas[t]['tiempo'] for t in individuo)