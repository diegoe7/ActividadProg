import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graficador:

    def __init__(self):

        self.v = tk.Tk()
        self.v.title("Generador de Graficas")
        self.v.geometry("800x600")

        # -------------------------
        # DATOS
        # -------------------------

        tk.Label(self.v, text="Datos:").pack()

        self.txtdatos = tk.Entry(self.v, width=50)
        self.txtdatos.pack()

        # -------------------------
        # LABELS
        # -------------------------

        tk.Label(self.v, text="Labels:").pack()

        self.txtlabels = tk.Entry(self.v, width=50)
        self.txtlabels.pack()

        # -------------------------
        # TIPO DE GRAFICA
        # -------------------------

        tk.Label(self.v, text="Tipo de grafica:").pack()

        self.tipo = ttk.Combobox(
            self.v,
            values=["Barras", "Linea", "Pie"]
        )

        self.tipo.pack()
        self.tipo.current(0)

        # -------------------------
        # NOMBRE ARCHIVO
        # -------------------------

        tk.Label(self.v, text="Nombre archivo:").pack()

        self.txtarchivo = tk.Entry(self.v, width=30)
        self.txtarchivo.pack()

        # -------------------------
        # BOTONES
        # -------------------------

        tk.Button(
            self.v,
            text="Generar Grafica",
            command=self.generar
        ).pack(pady=5)

        tk.Button(
            self.v,
            text="Guardar Informacion",
            command=self.guardar
        ).pack(pady=5)

        # -------------------------
        # FIGURA
        # -------------------------

        self.fig = Figure(figsize=(5, 4), dpi=100)

        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=self.v
        )

        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

        self.v.mainloop()

    # -----------------------------------
    # GENERAR GRAFICA
    # -----------------------------------

    def generar(self):

        try:

            datos = np.array(
                list(
                    map(
                        float,
                        self.txtdatos.get().split(",")
                    )
                )
            )

            labels = self.txtlabels.get().split(",")

            if len(datos) != len(labels):

                raise ValueError(
                    "Cantidad diferente entre datos y labels"
                )

            tipo = self.tipo.get()

            self.ax.clear()

            if tipo == "Barras":

                self.ax.bar(labels, datos)

            elif tipo == "Linea":

                self.ax.plot(labels, datos)

            elif tipo == "Pie":

                self.ax.pie(datos, labels=labels)

            self.ax.set_title("Grafica")

            self.canvas.draw()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # -----------------------------------
    # GUARDAR ARCHIVO
    # -----------------------------------

    def guardar(self):

        try:

            nombre = self.txtarchivo.get()

            if nombre == "":

                raise ValueError(
                    "Ingrese nombre del archivo"
                )

            datos = self.txtdatos.get()

            labels = self.txtlabels.get()

            tipo = self.tipo.get()

            archivo = open(nombre + ".txt", "w")

            archivo.write(
                "TIPO DE GRAFICA:\n"
            )

            archivo.write(tipo + "\n\n")

            archivo.write(
                "DATOS:\n"
            )

            archivo.write(datos + "\n\n")

            archivo.write(
                "LABELS:\n"
            )

            archivo.write(labels)

            archivo.close()

            messagebox.showinfo(
                "Guardado",
                "Archivo guardado correctamente"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


# -------------------------
# EJECUTAR
# -------------------------

Graficador()
