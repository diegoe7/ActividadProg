import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Graficas import Graficador

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Interfaz:
    def __init__ (self,ventana):
        self.ventana = ventana
        self.ventana.title("Generador de Gráficas")
        self.ventana.geometry("1100x600")

        self.grafica = Graficador()

        titulo = tk.Label(ventana, text="GENERADOR DE GRÁFICAS", font=("Times New Roman",16,"bold"))
        titulo.pack(pady=10)

        #LISTA GRAFICAS
        self.texto_lista = tk.Label(ventana, text="Tipos de graficas:", font=("Times New Roman",12))
        self.texto_lista.pack(pady=5)
        self.texto_lista.place(x=10, y=50)
        self.ListaGraficas = tk.Listbox(ventana)
        self.ListaGraficas.pack()
        self.ListaGraficas.place(x=10, y=75)

        graficas = ["barras", "lineas", "scatter", "histograma", "torta"]
        for grafica in graficas:
            self.ListaGraficas.insert(tk.END,grafica)
        
        self.ListaGraficas.bind("<<ListboxSelect>>", self.mostrar_campos)

        #DATOS
        self.texto_dato1 = tk.Label(ventana, font=("Times New Roman",12))
        self.datos1 = tk.Entry(ventana, width=50)

        self.texto_dato2 = tk.Label(ventana, font=("Times New Roman",12))
        self.datos2 = tk.Entry(ventana, width=50)

        #TITULO GRAFICA
        self.texto_nombre = tk.Label(ventana, text="Nombre del archivo: ", font=("Times New Roman",12))
        self.nombreArchivo = tk.Entry(ventana, width=30)

        #BOTON GENERAR GRÁFICA
        self.botonGenerar = tk.Button(ventana, text="GENERAR GRÁFICA", font=("Times New Roman",10), command=self.generar)

        #VISTA PREVIA DE LA GRAFICA
        self.frame_grafica = tk.Frame(ventana)
        self.frame_grafica.pack(pady=10)
        self.frame_grafica.place(x=470, y=120)
        self.canvas = None

        #BOTON SALIR
        botonSalir = tk.Button(ventana, text="SALIR", font=("Times New Roman", 10), command=self.salir)
        botonSalir.pack(pady=5)
        botonSalir.place(x=1000, y=550)

    def mostrar_campos(self, evento):
        opcion = self.ListaGraficas.curselection()
        if not opcion:
            return
        
        tipo = self.ListaGraficas.get(opcion[0])

        labels = {
            "barras" : ("Categorias:", "Valores:"),
            "lineas" : ("Eje X:", "Eje Y:"),
            "scatter": ("Eje X:", "Eje Y:"),
            "histograma": ("Etiquetas:", "Valores:"),
            "torta": ("Labels:", "Datos:")
        }

        label1, label2 = labels[tipo]

        self.texto_dato1.config(text=label1)
        self.texto_dato2.config(text=label2)

        #Mostrar los datos
        self.texto_dato1.pack()
        self.texto_dato1.place(x=10, y=300)
        self.datos1.pack(pady=5)
        self.datos1.place(x=10, y=325)

        self.texto_dato2.pack()
        self.texto_dato2.place(x=10, y=375)
        self.datos2.pack(pady=5)
        self.datos2.place(x=10, y=400)

        self.texto_nombre.pack()
        self.texto_nombre.place(x=10, y=450)
        self.nombreArchivo.pack(pady=5)
        self.nombreArchivo.place(x=10, y=475)

        self.botonGenerar.pack()
        self.botonGenerar.place(x=10, y=520)

    #GENERAR GRAFICA
    def generar(self):
        try:
            opcion = self.ListaGraficas.curselection()
            if not opcion:
                messagebox.showinfo("ERROR", "Seleccione una grafica.")
                return

            tipo = self.ListaGraficas.get(opcion[0])

            #Leer los datos
            listaDatos1 = self.datos1.get()
            listaDatos2 = self.datos2.get()

            lista1 = listaDatos1.split(",")
            lista2 = listaDatos2.split(",")

            lista1 = [i.strip() for i in lista1]
            lista2 = [float(i.strip()) for i in lista2] #Cambiara los strings a numeros

            if tipo in ["lineas", "scatter"]:
                lista1 = [float(i) for i in lista1]

            #Verificar cantidad de datos
            if len(lista1) != len(lista2):
                messagebox.showinfo("ERROR","La cantidad de datos no coincide.")
                return
            
            self.grafica.cargar_datos(lista1,lista2) #Guardar los datos en el objeto

            #Vista de la grafica
            fig = self.grafica.generar_grafica(tipo)  # Obtiene la figura

            if self.canvas:
                self.canvas.get_tk_widget().destroy()  # Elimina canvas anterior

            self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()
            plt.close(fig)

        except:
            messagebox.showinfo("ERROR", "Datos invalidos.")

    def salir(self):
        if messagebox.askyesno("Salir", "¿Deseas salir?"):
            self.ventana.destroy()


ventana = tk.Tk()
interfaz = Interfaz(ventana)

ventana.mainloop()