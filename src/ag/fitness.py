from src.ag.penalizaciones import evaluar_precedencias, penalizar_mezcla_tipos, evaluar_balanceo, evaluar_makespan

#funcion fitness que evalua un individuo, 
# tomando en cuenta las penalizaciones por violaciones de restricciones

def fitness(estaciones, dependencias, infoTareas):
    penal = 0
    penal += evaluar_precedencias(estaciones, dependencias, infoTareas)
    penal += evaluar_balanceo(estaciones, infoTareas)
    penal += penalizar_mezcla_tipos(estaciones, infoTareas)
    return evaluar_makespan(estaciones, infoTareas) + penal