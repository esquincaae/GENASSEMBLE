from src.ag.sobrecarga import evaluar_precedencias, evaluar_balanceo, evaluar_makespan

#funcion fitness que evalua un individuo

def fitness(individuo, dependencias, infoTareas, sobrecarga):
    overload = 0
    overload += evaluar_precedencias(individuo, dependencias, infoTareas, sobrecarga)
    overload += evaluar_balanceo(individuo, infoTareas)
    return evaluar_makespan(individuo, infoTareas) + overload

