from src.ag.ejecutar_ag import ejecutar_algoritmo_genetico
import tkinter as tk
from tkinter import messagebox
import pandas as pd

tareas_df = pd.read_csv("data/tareas.csv")
precedencias_df = pd.read_csv("data/precedencias.csv", index_col=0)
sobrecarga_df = pd.read_csv("data/sobrecarga.csv")

def iniciar_interfaz():
    def ejecutar_algoritmo():
        global tareas_df, precedencias_df, sobrecarga_df
        estaciones = 5
        try:
            poblacion = int(entry_poblacion.get())
            generaciones = int(entry_generaciones.get())
            p_cruza = float(entry_cruza.get())
            p_mutacion = float(entry_mutacion.get())

            if not (0 <= p_cruza <= 1 and 0 <= p_mutacion <= 1):
                raise ValueError("Las probabilidades deben estar entre 0.0 y 1.0")

            # Validar columnas de sobrecarga_df
            if not {'Nombre', 'Tiempo', 'Tipo'}.issubset(sobrecarga_df.columns):
                raise ValueError("El archivo de sobrecarga debe tener las columnas 'Nombre', 'Tiempo' y 'Tipo'.")

            # se valida que las columnas existan en tareas_df
            if not {'Nombre', 'Tiempo', 'Tipo'}.issubset(tareas_df.columns):
                raise ValueError("El archivo de tareas debe tener las columnas 'Nombre', 'Tiempo' y 'Tipo'.")

            nombresTareas = list(tareas_df['Nombre'])
            
            infoTareas = {
                row['Nombre']: {
                    'tiempo': row['Tiempo'],
                    'tipo': row['Tipo']
                } for _, row in tareas_df.iterrows()
            }

            sobrecarga = {
                row['Tipo']: {
                    'tiempo': row['Tiempo'],
                    'Nombre': row['Nombre']
                } for _, row in sobrecarga_df.iterrows()
            }

            # Construir diccionario de precedencias { tarea: [lista de tareas predecesoras] }
            matPrecedencias = {}
            for tarea in nombresTareas:
                if tarea in precedencias_df.index:
                    fila = precedencias_df.loc[tarea]
                    # Obtener tareas predecesoras (donde valor==1)
                    predecesoras = fila[fila == 1].index.tolist()
                    matPrecedencias[tarea] = predecesoras
                else:
                    matPrecedencias[tarea] = []

            #ejecuta el algoritmo genético con lista de tareas y precedencias
            mejor_individuo, evolucion = ejecutar_algoritmo_genetico(
nombresTareas, infoTareas, matPrecedencias, estaciones, poblacion, generaciones, p_cruza, p_mutacion, sobrecarga)


        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos:\n{e}")

    root = tk.Tk()
    root.title("GENASSEMBLE")

    tk.Label(root, text="Tamaño de población:").grid(row=1, column=0, sticky='e')
    entry_poblacion = tk.Entry(root)
    entry_poblacion.grid(row=1, column=1)
    entry_poblacion.insert(0, "200")

    tk.Label(root, text="Número de generaciones:").grid(row=2, column=0, sticky='e')
    entry_generaciones = tk.Entry(root)
    entry_generaciones.grid(row=2, column=1)
    entry_generaciones.insert(0, "100")

    tk.Label(root, text="Probabilidad de cruza (0-1):").grid(row=3, column=0, sticky='e')
    entry_cruza = tk.Entry(root)
    entry_cruza.grid(row=3, column=1)
    entry_cruza.insert(0, "0.5")

    tk.Label(root, text="Probabilidad de mutación (0-1):").grid(row=4, column=0, sticky='e')
    entry_mutacion = tk.Entry(root)
    entry_mutacion.grid(row=4, column=1)
    entry_mutacion.insert(0, "0.8")

    tk.Button(root, text="Ejecutar algoritmo", command=ejecutar_algoritmo, bg="lightgreen").grid(row=5, column=0, columnspan=2, pady=10)

    root.mainloop()
