import random

def generar_individuo(tareas, num_estaciones, infoTareas):
    # Obtener los tipos únicos de tareas
    tipos = list({infoTareas[n]['tipo'] for n in tareas})
    random.shuffle(tipos)  # Para variar el orden de tipos en las estaciones

    # Asignar un tipo a cada estación (si hay más estaciones que tipos, algunos tipos se repiten)
    tipos_por_estacion = [tipos[i % len(tipos)] for i in range(num_estaciones)]

    # Inicializar estaciones vacías
    estaciones = [[] for _ in range(num_estaciones)]

    # Agrupar tareas por tipo
    tareas_por_tipo = {tipo: [] for tipo in tipos}
    for nombre in tareas:
        tareas_por_tipo[infoTareas[nombre]['tipo']].append(nombre)

    # Asignar tareas a la estación correspondiente a su tipo
    for idx, tipo in enumerate(tipos_por_estacion):
        estaciones[idx].extend(tareas_por_tipo.get(tipo, []))

    return estaciones