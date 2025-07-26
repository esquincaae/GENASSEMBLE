from src.ag.penalizaciones import evaluar_precedencias, evaluar_exceso_tareas, evaluar_balanceo, evaluar_makespan, evaluar_estaciones_vacias

#funcion fitness que evalua un individuo, 
# tomando en cuenta las penalizaciones por violaciones de restricciones

def fitness(estaciones, dependencias, infoTareas):
    penal = 0
    penal += evaluar_precedencias(estaciones, dependencias, infoTareas)
    penal += evaluar_exceso_tareas(estaciones)
    penal += evaluar_balanceo(estaciones, infoTareas)
    penal += evaluar_estaciones_vacias(estaciones)
    return evaluar_makespan(estaciones, infoTareas) + penal