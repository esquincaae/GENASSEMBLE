import random

def generar_individuo(tareas, num_estaciones, infoTareas):
    # Obtener los tipos únicos de tareas
    tipos = list({infoTareas[n]['tipo'] for n in tareas})
    random.shuffle(tipos)  # se barajean el orden de los tipos

    # se asignan los tipos a las estaciones
    tipos_por_estacion = [tipos[i % len(tipos)] for i in range(num_estaciones)]

    # se agrupan las tareas por tipo
    tareas_por_tipo = {tipo: [] for tipo in tipos}
    for nombre in tareas:
        tareas_por_tipo[infoTareas[nombre]['tipo']].append(nombre)

    # Para cada tipo asignado a una estación, barajear las tareas de ese tipo
    for tipo in tareas_por_tipo:
        random.shuffle(tareas_por_tipo[tipo])

    # se crea una lista plana concatenando las tareas según el orden de tipos_por_estacion
    individuo = []
    for tipo in tipos_por_estacion:
        individuo.extend(tareas_por_tipo.get(tipo, []))

    return individuo