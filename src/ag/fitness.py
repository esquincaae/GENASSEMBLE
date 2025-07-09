from src.ag.algoritmo_genetico import evaluar_precedencias, evaluar_exceso_tareas, evaluar_balanceo, evaluar_makespan, evaluar_estaciones_vacias

def fitness(estaciones, dependencias, tiempos):
    penal = 0
    penal += evaluar_precedencias(estaciones, dependencias, tiempos)
    penal += evaluar_exceso_tareas(estaciones)
    penal += evaluar_balanceo(estaciones, tiempos)
    penal += evaluar_estaciones_vacias(estaciones)
    return evaluar_makespan(estaciones, tiempos) + penal