import random

#Half-Fixed + Random Completion

#Mitad del padre 1 se hereda tal cual (posición + estación).

#La otra mitad se rellena usando el padre 2

def cruza(p1, p2, num_estaciones, infoTareas):
    hijo = [[] for _ in range(num_estaciones)]
    tareas_p1 = [t for est in p1 for t in est]
    mitad = len(tareas_p1) // 2
    usadas = set()

    # Determinar el tipo de cada estación según p1
    tipos_por_estacion = []
    for est in p1:
        if est:
            tipos_por_estacion.append(infoTareas[est[0]]['tipo'])
        else:
            tipos_por_estacion.append(None)

    # Heredar la mitad de p1
    for i, t in enumerate(tareas_p1):
        if i < mitad:
            for e in range(num_estaciones):
                if t in p1[e]:
                    hijo[e].append(t)
                    usadas.add(t)
                    break

    # Completar con tareas de p2, respetando el tipo de estación
    for est_idx, est in enumerate(p2):
        tipo_est = tipos_por_estacion[est_idx]
        for t in est:
            if t not in usadas and infoTareas[t]['tipo'] == tipo_est:
                hijo[est_idx].append(t)
                usadas.add(t)

    # Si quedan tareas sin asignar, distribúyelas en estaciones compatibles
    restantes = [t for t in [t for est in p2 for t in est] if t not in usadas]
    for t in restantes:
        tipo_t = infoTareas[t]['tipo']
        posibles = [i for i, tipo in enumerate(tipos_por_estacion) if tipo == tipo_t]
        if posibles:
            hijo[random.choice(posibles)].append(t)
            usadas.add(t)

    return hijo