import random

def cruza(p1, p2, num_estaciones):
    """Cruza con hibridación completa: hijos combinan tareas de padres en posiciones pares."""
    hijo = [[] for _ in range(num_estaciones)]
    tareas_p1 = [t for est in p1 for t in est]
    mitad = len(tareas_p1) // 2
    usadas = set()

    for i, t in enumerate(tareas_p1):
        if i < mitad:
            for e in range(num_estaciones):
                if t in p1[e]:
                    hijo[e].append(t)
                    usadas.add(t)
                    break
    for est in p2:
        for t in est:
            if t not in usadas:
                random.choice(hijo).append(t)
                usadas.add(t)
    return hijo

