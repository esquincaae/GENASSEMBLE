from src.ag.algoritmo_genetico import evaluar_precedencias, evaluar_exceso_tareas, evaluar_balanceo, evaluar_makespan

def fitness(estaciones, dependencias, tiempos):
    penal = 0
    penal += evaluar_precedencias(estaciones, dependencias, tiempos)
    penal += evaluar_exceso_tareas(estaciones)
    penal += evaluar_balanceo(estaciones, tiempos)
    return evaluar_makespan(estaciones, tiempos) + penal