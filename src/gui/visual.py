from src.ag.ejecutar_ag import ejecutar_algoritmo_genetico
import tkinter as tk
from tkinter import messagebox
import pandas as pd

tareas_df = pd.read_csv("data/tareas.csv")
precedencias_df = pd.read_csv("data/precedencias.csv", index_col=0)
tipos_estaciones_df = pd.read_csv("data/tipos_estaciones.csv")

def iniciar_interfaz():
    def ejecutar_algoritmo():
        global tareas_df, precedencias_df, tipos_estaciones_df
        try:
            estaciones = 5
            poblacion = int(entry_poblacion.get())
            generaciones = int(entry_generaciones.get())
            p_cruza = float(entry_cruza.get())
            p_mutacion = float(entry_mutacion.get())

            if not (0 <= p_cruza <= 1 and 0 <= p_mutacion <= 1):
                raise ValueError("Las probabilidades deben estar entre 0.0 y 1.0")
            
            # Validar que las columnas existan 
            if not {'Nombre', 'Tiempo'}.issubset(tareas_df.columns):
                raise ValueError("El archivo de tareas debe tener las columnas 'Nombre' y 'Tiempo'.")
            if not {'Estacion', 'Tipos'}.issubset(tipos_estaciones_df.columns):
                raise ValueError("El archivo de tipos de estaciones debe tener las columnas 'Estacion' y 'Tipos'.")

            estaciones_tipos = {
                row['Estacion']: row['Tipos'].split(",") for _, row in tipos_estaciones_df.iterrows()
            }

            nombresTareas = list(tareas_df['Nombre'])
            infoTareas = {
                row['Nombre']: {
                    'tiempo': row['Tiempo'],
                    'tipo': row['Tipo']
                } for _, row in tareas_df.iterrows()
            }

            # Convertir precedencias_df a diccionario de listas
            matPrecedencias = {}
            for nombre in nombresTareas:
                if nombre in precedencias_df.index:
                    deps = precedencias_df.loc[nombre]
                    if isinstance(deps, pd.DataFrame):
                        deps = deps.iloc[0]
                    matPrecedencias[nombre] = deps[deps == 1].index.tolist()
                else:
                    matPrecedencias[nombre] = []

            # Llama al algoritmo genético
            mejor_individuo, evolucion = ejecutar_algoritmo_genetico(
                nombresTareas, infoTareas, matPrecedencias, estaciones, poblacion, generaciones, p_cruza, p_mutacion, estaciones_tipos)

        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos:\n{e}")

    root = tk.Tk()
    root.title("GENASSEMBLE")

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
