import tkinter as tk
from tkinter import messagebox
import pandas as pd
import src.ag.algoritmo_genetico as algoritmo_genetico

tareas_df = pd.read_csv("data/tareas.csv")
precedencias_df = pd.read_csv("data/precedencias.csv", index_col=0)

def iniciar_interfaz():
    def ejecutar_algoritmo():
        global tareas_df, precedencias_df
        try:
            estaciones = int(entry_estaciones.get())
            poblacion = int(entry_poblacion.get())
            generaciones = int(entry_generaciones.get())
            p_cruza = float(entry_cruza.get())
            p_mutacion = float(entry_mutacion.get())

            if not (0 <= p_cruza <= 1 and 0 <= p_mutacion <= 1):
                raise ValueError("Las probabilidades deben estar entre 0.0 y 1.0")

            # Validar que las columnas requeridas estén presentes
            if not {'Tarea', 'Tiempo'}.issubset(tareas_df.columns):
                raise ValueError("El archivo de tareas debe tener las columnas 'Tarea' y 'Tiempo'.")

            tareas = list(tareas_df['Tarea'])
            tiempos = dict(zip(tareas_df['Tarea'], tareas_df['Tiempo']))

            # Convertir precedencias_df a diccionario de listas
            dependencias = {}
            print("Índices en precedencias_df:", precedencias_df.index.unique())
            print("Columnas en precedencias_df:", precedencias_df.columns)
            for tarea in tareas:
                if tarea in precedencias_df.index:
                    deps = precedencias_df.loc[tarea]
                    print(f"Tarea: {tarea}")
                    print(f"Tipo deps: {type(deps)}")
                    print(deps)
                    if isinstance(deps, pd.DataFrame):
                        deps = deps.iloc[0]
                        print(f"Tarea: {tarea}")
                        print(f"Tipo deps: {type(deps)}")
                        print(deps)
                    dependencias[tarea] = deps[deps == 1].index.tolist()
                else:
                    dependencias[tarea] = []

            # Llamar al algoritmo genético y obtener resultados
            mejor_individuo, evolucion = algoritmo_genetico.ejecutar_algoritmo_genetico(
                tareas, tiempos, dependencias, estaciones, poblacion, generaciones, p_cruza, p_mutacion
            )

            messagebox.showinfo("Éxito", "Algoritmo ejecutado correctamente. Revisa las gráficas generadas.")

        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos:\n{e}")

    root = tk.Tk()
    root.title("GENASSEMBLE - Algoritmo Genético para Asignación de Tareas")

    tk.Label(root, text="Número de estaciones:").grid(row=0, column=0, sticky='e')
    entry_estaciones = tk.Entry(root)
    entry_estaciones.grid(row=0, column=1)

    tk.Label(root, text="Tamaño de población:").grid(row=1, column=0, sticky='e')
    entry_poblacion = tk.Entry(root)
    entry_poblacion.grid(row=1, column=1)

    tk.Label(root, text="Número de generaciones:").grid(row=2, column=0, sticky='e')
    entry_generaciones = tk.Entry(root)
    entry_generaciones.grid(row=2, column=1)

    tk.Label(root, text="Probabilidad de cruza (0-1):").grid(row=3, column=0, sticky='e')
    entry_cruza = tk.Entry(root)
    entry_cruza.grid(row=3, column=1)

    tk.Label(root, text="Probabilidad de mutación (0-1):").grid(row=4, column=0, sticky='e')
    entry_mutacion = tk.Entry(root)
    entry_mutacion.grid(row=4, column=1)

    tk.Button(root, text="Ejecutar algoritmo", command=ejecutar_algoritmo, bg="lightgreen").grid(row=5, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
