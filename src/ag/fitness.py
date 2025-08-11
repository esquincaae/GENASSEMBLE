from src.ag.penalizaciones import evaluar_precedencias, evaluar_balanceo, evaluar_makespan

#funcion fitness que evalua un individuo

def fitness(individuo, dependencias, infoTareas, poblacion):
    penal = 0
    penal += evaluar_precedencias(individuo, dependencias, infoTareas, poblacion)
    penal += evaluar_balanceo(individuo, infoTareas)
    return evaluar_makespan(individuo, infoTareas) + penal

