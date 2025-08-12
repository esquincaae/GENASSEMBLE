import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import tkinter as tk

def agrupar_por_tipo(individuo, infoTareas, num_estaciones=None):
    estaciones_dict = {}
    for tarea in individuo:
        tipo = infoTareas[tarea]['tipo']
        if tipo not in estaciones_dict:
            estaciones_dict[tipo] = []
        estaciones_dict[tipo].append(tarea)

    estaciones = list(estaciones_dict.values())
    if num_estaciones:
        if len(estaciones) < num_estaciones:
            estaciones.extend([[]] * (num_estaciones - len(estaciones)))
        elif len(estaciones) > num_estaciones:
            estaciones = estaciones[:num_estaciones]
    return estaciones

def sobrecargar_individuo(individuo, infoTareas, dependencias, sobrecarga):
    pos = {t: i for i, t in enumerate(individuo)}
    for tarea, deps in dependencias.items():
        for d in deps:
            if pos.get(d, -1) > pos.get(tarea, -1):
                type_task = infoTareas[tarea]['tipo']
                infoTareas[tarea]['tiempo'] += sobrecarga[type_task]['tiempo']
    return individuo

def graficar_evolucion(mejores):
    plt.figure(figsize=(10,5))
    plt.plot(mejores, label='Mejor fitness (makespan + penalizaciones)')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title('Evolución del mejor individuo')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/evolucion_mejor_individuo.png')
    plt.show()

def graficar_gantt(individuo, infoTareas):
    
    
    tipos = []
    for t in individuo:
        tipo = infoTareas[t]['tipo']
        if tipo not in tipos:
            tipos.append(tipo)

    tipo_a_fila = {tipo: i for i, tipo in enumerate(tipos)}

    fig, ax = plt.subplots(figsize=(14, 6))
    colores = plt.cm.get_cmap('tab20', len(tipos))

    tiempo_global = 0
    disponibilidad_tipo = {tipo: 0 for tipo in tipos}
    max_tiempo = 0

    for tarea in individuo:
        tipo = infoTareas[tarea]['tipo']
        duracion = infoTareas[tarea]['tiempo']

        inicio = max(tiempo_global, disponibilidad_tipo[tipo])
        fin = inicio + duracion

        fila = tipo_a_fila[tipo]

        ax.broken_barh([(inicio, duracion)], (fila * 10, 9), facecolors=colores(fila), edgecolor='black')

        # Ajustar tamaño de fuente mínimo 6
        fontsize = max(1, min(12, duracion * 3))  # escala para que sea proporcional

        texto = tarea.replace(" ", "\n")  # reemplazar guiones bajos por espacios
        ax.text(inicio + duracion / 2, fila * 10 + 4.5, texto, ha='center', va='center',
                color='white', fontsize=fontsize, weight='bold',
                path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])

        tiempo_global = fin
        disponibilidad_tipo[tipo] = fin
        max_tiempo = max(max_tiempo, fin)

    for i in range(len(tipos) + 1):
        ax.axhline(i * 10, color='gray', linewidth=0.8, linestyle='--')

    ax.set_yticks([i * 10 + 4.5 for i in range(len(tipos))])
    ax.set_yticklabels(tipos, fontsize=11)

    ax.set_xlim(0, max_tiempo * 1.1)
    ax.set_xlabel('Tiempo', fontsize=12)
    ax.set_title('Diagrama de Gantt con texto ajustado', fontsize=14, weight='bold')
    ax.grid(axis='x', linestyle=':', linewidth=0.7)

    plt.tight_layout()
    plt.savefig('results/gantt_mejor_solucion.png')
    plt.show()

def ventana_top_3(poblacion, infoTareas, dependencias, fitness_func, sobrecarga):
    top_3 = sorted(poblacion, key=lambda ind: fitness_func(ind, dependencias, infoTareas, sobrecarga))[:3]

    ventana = tk.Toplevel()
    ventana.title("Top 3 mejores soluciones")
    ventana.geometry("920x350")

    texto = tk.Text(ventana, wrap='word', font=("Consolas", 10))
    texto.pack(fill='both', expand=True)

    texto.insert(tk.END, "Tabla con los 3 mejores resultados:\n\n")

    for i, ind in enumerate(top_3, start=1):
        fitness_val = fitness_func(ind, dependencias, infoTareas, sobrecarga)
        texto.insert(tk.END, f"🔹 Individuo {i} - Fitness total: {fitness_val:.2f}\n")

        estaciones = agrupar_por_tipo(ind, infoTareas)

        for est_idx, tareas in enumerate(estaciones, start=1):
            if tareas:
                tipo = infoTareas[tareas[0]]['tipo']  # Tomamos el tipo de la primera tarea
                tiempo_total = sum(infoTareas[t]['tiempo'] for t in tareas)
                texto.insert(tk.END, f"   Estación {est_idx} ({tipo}): [{', '.join(tareas)}] - Tiempo total: {tiempo_total}\n")
            else:
                texto.insert(tk.END, f"   Estación {est_idx}: vacía\n")

        texto.insert(tk.END, "\n")

    texto.config(state='disabled')

def ventana_resumen_mejor(poblacion, infoTareas, dependencias, fitness_func, sobrecarga):
    individuo_sobrecargado = sobrecargar_individuo(poblacion[0], infoTareas, dependencias, sobrecarga)
    mejor = min(poblacion, key=lambda ind: fitness_func(ind, dependencias, infoTareas, sobrecarga))
    estaciones = agrupar_por_tipo(mejor, infoTareas)

    cargas = [sum(infoTareas[t]['tiempo'] for t in tareas) for tareas in estaciones]
    makespan = sum(cargas) if cargas else 0
    sobrecargas = fitness_func(individuo_sobrecargado, dependencias, infoTareas, sobrecarga) - makespan

    ventana = tk.Toplevel()
    ventana.title("Resumen del mejor individuo")
    ventana.geometry("920x200")

    texto = tk.Text(ventana, wrap='word', font=("Consolas", 10))
    texto.pack(fill='both', expand=True)

    texto.insert(tk.END, "Resumen del mejor individuo:\n\n")

    for est_idx, tareas in enumerate(estaciones, start=1):
        if tareas:
            tipo = infoTareas[tareas[0]]['tipo']  # Obtener tipo desde la primera tarea
            tiempo_total = sum(infoTareas[t]['tiempo'] for t in tareas)
            texto.insert(tk.END, f"   Estación {est_idx} ({tipo}): [{', '.join(tareas)}] - Tiempo total: {tiempo_total}\n")
        else:
            texto.insert(tk.END, f"   Estación {est_idx}: vacía\n")

    texto.insert(tk.END, f"\nMakespan total: {makespan}\n")
    texto.insert(tk.END, f"Sobre cargas: {sobrecargas:.2f}\n")

    texto.config(state='disabled')
