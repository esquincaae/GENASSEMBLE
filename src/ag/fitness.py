from src.ag.penalizaciones import estaciones_validas, evaluar_precedencias, evaluar_exceso_tareas, evaluar_balanceo, evaluar_makespan, evaluar_estaciones_vacias

#funcion fitness que evalua un individuo, 
# tomando en cuenta las penalizaciones por violaciones de restricciones

def fitness(estaciones, dependencias, infoTareas, estaciones_tipos):
    penal = 0
    penal += estaciones_validas(estaciones, infoTareas, estaciones_tipos)
    penal += evaluar_precedencias(estaciones, dependencias, infoTareas)
    penal += evaluar_exceso_tareas(estaciones)
    penal += evaluar_balanceo(estaciones, infoTareas)
    penal += evaluar_estaciones_vacias(estaciones)
    return evaluar_makespan(estaciones, infoTareas) + penal