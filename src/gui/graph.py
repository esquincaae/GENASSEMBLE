import matplotlib.pyplot as plt
import tkinter as tk

def graficar_evolucion(mejores):
    plt.figure(figsize=(10,5))
    plt.plot(mejores, label='Mejor fitness (makespan + penalizaciones)')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title('Evolución del Algoritmo Genético')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/evolucion_algoritmo.png')
    plt.show()

def graficar_gantt(individuo, infoTareas, num_estaciones, tareas):
    fig, ax = plt.subplots(figsize=(12, 6))
    colores = plt.cm.get_cmap('tab20', len(tareas))
    tiempos_actuales = [0]*num_estaciones

    tipos_estaciones = []
    for est in individuo:
        if est:
            tipos_estaciones.append(infoTareas[est[0]]['tipo'])
        else:
            tipos_estaciones.append('Vacia')

    individuo_reversed = individuo[::-1]

    for est_idx, est in enumerate(individuo_reversed):
        for tarea in est:
            inicio = tiempos_actuales[est_idx]
            duracion = infoTareas[tarea]['tiempo']
            ax.broken_barh([(inicio, duracion)], (est_idx*10, 9), facecolors=colores(tareas.index(tarea)))
            ax.text(inicio + duracion/2, est_idx*10 + 4.5, tarea, ha='center', va='center', color='white', fontsize=8)
            tiempos_actuales[est_idx] += duracion

    ax.set_yticks([i*10+4.5 for i in range(num_estaciones)])
    ax.set_yticklabels([f'{tipo}' for i, tipo in enumerate(tipos_estaciones)])
    ax.set_xlabel('Tiempo')
    ax.set_title('Diagrama de Gantt de la mejor solución')
    plt.tight_layout()
    plt.savefig('results/gantt_mejor_solucion.png')
    plt.show()

def ventana_top_3(poblacion, infoTareas, dependencias, fitness_func):
    top_3 = sorted(poblacion, key=lambda ind: fitness_func(ind, dependencias, infoTareas))[:3]

    ventana = tk.Toplevel()
    ventana.title("Top 3 mejores soluciones")
    ventana.geometry("750x400")

    texto = tk.Text(ventana, wrap='word', font=("Consolas", 10))
    texto.pack(fill='both', expand=True)

    texto.insert(tk.END, "Tabla con los 3 mejores resultados:\n\n")
    for i, ind in enumerate(top_3, start=1):
        texto.insert(tk.END, f"🔹 Individuo {i} - Fitness total: {fitness_func(ind, dependencias, infoTareas):.2f}\n")
        ttf = 0
        for est_idx, est in enumerate(ind):
            tareas = ', '.join(est)
            tiempo_total = sum(infoTareas[t]['tiempo'] for t in est)
            texto.insert(tk.END, f"   Estación {est_idx+1}: [{tareas}] - Tiempo total: {tiempo_total}\n")
        texto.insert(tk.END, "\n")

    texto.config(state='disabled')

def ventana_resumen_mejor(poblacion, infoTareas, dependencias, fitness_func):
    mejor = min(poblacion, key=lambda ind: fitness_func(ind, dependencias, infoTareas))
    cargas = [sum(infoTareas[t]['tiempo'] for t in est) for est in mejor]
    makespan = max(cargas)
    penalizaciones = fitness_func(mejor, dependencias, infoTareas) - makespan

    ventana = tk.Toplevel()
    ventana.title("Resumen del mejor individuo")
    ventana.geometry("750x300")

    texto = tk.Text(ventana, wrap='word', font=("Consolas", 10))
    texto.pack(fill='both', expand=True)

    texto.insert(tk.END, "Resumen del mejor individuo:\n\n")
    for est_idx, est in enumerate(mejor):
        tareas = ', '.join(est)
        tiempo_total = cargas[est_idx]
        texto.insert(tk.END, f"   Estación {est_idx+1}: [{tareas}] - Tiempo total: {tiempo_total}\n")

    texto.insert(tk.END, f"\nMakespan total: {makespan}\n")
    texto.insert(tk.END, f"Penalizaciones: {penalizaciones:.2f}\n")

    texto.config(state='disabled')

