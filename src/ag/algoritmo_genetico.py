import random
import copy
import numpy as np
import src.gui.graph as graph  # importar módulo para graficar

# Parámetros fijos
PENALIZACION_PRECEDENCIA = 3
PENALIZACION_EXCESO_TAREAS = 10
PENALIZACION_DESEQUILIBRIO = 5
MAX_TAREAS_POR_ESTACION = 4

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
    return desv * PENALIZACION_DESEQUILIBRIO

def evaluar_makespan(estaciones, tiempos):
    cargas = [sum(tiempos[t] for t in est) for est in estaciones]
    return max(cargas)

def fitness(estaciones, dependencias, tiempos):
    penal = 0
    penal += evaluar_precedencias(estaciones, dependencias, tiempos)
    penal += evaluar_exceso_tareas(estaciones)
    penal += evaluar_balanceo(estaciones, tiempos)
    return evaluar_makespan(estaciones, tiempos) + penal

# --- Métodos explícitos del algoritmo genético ---

def emparejamiento(poblacion, porcentaje=0.25):
    """Selecciona un porcentaje de la población para formar parejas todos-con-todos."""
    num_seleccionados = max(2, int(len(poblacion) * porcentaje))
    seleccionados = random.sample(poblacion, num_seleccionados)
    parejas = []
    for i in range(num_seleccionados):
        for j in range(i + 1, num_seleccionados):
            parejas.append((seleccionados[i], seleccionados[j]))
    return parejas

def cruza(p1, p2, num_estaciones):
    """Cruza con hibridación completa: hijos combinan tareas de padres en posiciones pares."""
    hijo = [[] for _ in range(num_estaciones)]
    tareas_p1 = [t for est in p1 for t in est]
    mitad = len(tareas_p1) // 2
    usadas = set()

    for i, t in enumerate(tareas_p1):
        if i < mitad:
            for e in range(num_estaciones):
                if t in p1[e]:
                    hijo[e].append(t)
                    usadas.add(t)
                    break
    for est in p2:
        for t in est:
            if t not in usadas:
                random.choice(hijo).append(t)
                usadas.add(t)
    return hijo

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

def poda(poblacion, dependencias, tiempos, tam_poblacion):
    """
    Poda para mantener tamaño máximo:
    - Eliminar clones (mantener solo una copia)
    - Mantener el mejor individuo
    - Eliminar aleatoriamente para reducir tamaño si hay exceso
    """
    # Eliminar clones: usar tuplas para hashable
    poblacion_unica = {}
    for ind in poblacion:
        key = tuple(tuple(est) for est in ind)
        poblacion_unica[key] = ind

    poblacion = list(poblacion_unica.values())
    poblacion.sort(key=lambda ind: fitness(ind, dependencias, tiempos))
    mejor = poblacion[0]

    if len(poblacion) > tam_poblacion:
        # Eliminamos aleatoriamente excepto el mejor
        exceso = len(poblacion) - tam_poblacion
        indices_eliminar = random.sample(range(1, len(poblacion)), exceso)
        poblacion = [ind for i, ind in enumerate(poblacion) if i not in indices_eliminar]

    # Asegurarse que el mejor esté en la población
    if mejor not in poblacion:
        poblacion.append(mejor)

    return poblacion

# --- Algoritmo principal con llamadas explícitas ---

def ejecutar_algoritmo_genetico(tareas, tiempos, dependencias, num_estaciones,
                                tam_poblacion, num_generaciones,
                                prob_cruza, prob_mutacion):

    poblacion = [generar_individuo(tareas, num_estaciones) for _ in range(tam_poblacion)]
    mejor_fitness = float('inf')
    mejor_individuo = None
    evolucion = []

    for gen in range(num_generaciones):
        nueva_poblacion = []

        # Emparejamiento explícito
        parejas = emparejamiento(poblacion, porcentaje=0.25)

        # Cruza y mutación para generar descendencia
        for p1, p2 in parejas:
            if random.random() < prob_cruza:
                hijo = cruza(p1, p2, num_estaciones)
            else:
                hijo = copy.deepcopy(random.choice([p1, p2]))

            if random.random() < prob_mutacion:
                hijo = mutacion(hijo, num_estaciones)

            nueva_poblacion.append(hijo)

            # Si queremos mantener tamaño, podemos parar cuando llegue al máximo
            if len(nueva_poblacion) >= tam_poblacion:
                break

        # Agregamos la nueva generación + padres para poda
        poblacion.extend(nueva_poblacion)

        # Poda para mantener tamaño de población
        poblacion = poda(poblacion, dependencias, tiempos, tam_poblacion)

        # Evaluar mejor individuo
        poblacion.sort(key=lambda ind: fitness(ind, dependencias, tiempos))
        fit_actual = fitness(poblacion[0], dependencias, tiempos)
        evolucion.append(fit_actual)
        if fit_actual < mejor_fitness:
            mejor_fitness = fit_actual
            mejor_individuo = poblacion[0]

        print(f"Generación {gen+1}/{num_generaciones} - Mejor fitness: {mejor_fitness:.2f}")

    # Graficar resultados
    graph.graficar_evolucion(evolucion)
    graph.graficar_gantt(mejor_individuo, tiempos, num_estaciones, tareas)
    graph.ventana_top_3(poblacion, tiempos, dependencias, fitness)
    graph.ventana_resumen_mejor(poblacion, tiempos, dependencias, fitness)

    return mejor_individuo, evolucion
