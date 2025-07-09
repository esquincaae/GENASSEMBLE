from src.ag.emparejamiento import emparejamiento
from src.ag.cruza import cruza
from src.ag.mutacion import mutacion
from src.ag.poda import poda
from src.ag.algoritmo_genetico import generar_individuo
from src.ag.fitness import fitness
from src.gui import graph as graph

import copy
import random

def ejecutar_algoritmo_genetico(tareas, tiempos, dependencias, num_estaciones,
                                tam_poblacion, num_generaciones,
                                prob_cruza, prob_mutacion):

    poblacion = [generar_individuo(tareas, num_estaciones) for _ in range(tam_poblacion)]
    mejor_fitness = float('inf')
    mejor_individuo = None
    evolucion = []

    for gen in range(num_generaciones):
        nueva_poblacion = []

        parejas = emparejamiento(poblacion, porcentaje=0.25)

        for p1, p2 in parejas:
            if random.random() < prob_cruza:
                hijo = cruza(p1, p2, num_estaciones)
            else:
                hijo = copy.deepcopy(random.choice([p1, p2]))

            if random.random() < prob_mutacion:
                hijo = mutacion(hijo, num_estaciones)

            nueva_poblacion.append(hijo)

            if len(nueva_poblacion) >= tam_poblacion:
                break

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

    # Graficar resultados
    graph.graficar_evolucion(evolucion)
    graph.graficar_gantt(mejor_individuo, tiempos, num_estaciones, tareas)
    graph.ventana_top_3(poblacion, tiempos, dependencias, fitness)
    graph.ventana_resumen_mejor(poblacion, tiempos, dependencias, fitness)

    return mejor_individuo, evolucion