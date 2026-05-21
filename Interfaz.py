import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from subproceso import graficar

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ejemplos = {
    "lineas":     ("1,2,3,4",    "10,20,15,25"),
    "scatter":    ("1,2,3,4",    "10,20,15,25"),
    "barras":     ("A,B,C,D",    "10,20,15,25"),
    "torta":      ("A,B,C,D",    "10,20,15,25"),
    "histograma": ("A,B,C,D",    "10,20,15,25"),
}

class Interfaz:
    def __init__ (self,ventana):
        self.ventana = ventana
        self.ventana.title("Generador de Gráficas")
        self.ventana.geometry("1100x600")
        self.ventana.resizable(False,False)

        self.canvas_preview = None
        self.canvas_real = None

        #PREVIEW
        self.previews = {}
        for tipo in  ["lineas", "barras", "torta", "scatter", "histograma"]:
            eje_x, eje_y = ejemplos[tipo]
            fig = graficar(eje_x, eje_y, tipo, "", "", tipo,tamaño=(2.5,1.5))
            self.previews[tipo] = fig

        self.build_ui()

    def build_ui(self):
        titulo = tk.Label(self.ventana, text="GENERADOR DE GRÁFICAS", font=("Times New Roman",16,"bold"))
        titulo.pack(pady=10)

        #LISTA GRAFICAS
        self.texto_lista = tk.Label(self.ventana, text="Tipos de graficas:", font=("Times New Roman",12))
        self.texto_lista.place(x=30, y=50)

        self.combobox = ttk.Combobox(self.ventana, values=["lineas","barras","scatter","torta","histograma"], state="readonly", width=32)
        self.combobox.place(x=30, y=75)
        
        self.combobox.bind("<<ComboboxSelected>>", self.mostrar_campos)

        #DATOS
        self.texto_dato1 = tk.Label(self.ventana, font=("Times New Roman",12))
        self.datos1 = tk.Entry(self.ventana, width=50)

        self.texto_dato2 = tk.Label(self.ventana, font=("Times New Roman",12))
        self.datos2 = tk.Entry(self.ventana, width=50)

        #TITULO GRAFICA
        self.texto_nombre = tk.Label(self.ventana, text="Nombre del archivo: ", font=("Times New Roman",12))
        self.nombreArchivo = tk.Entry(self.ventana, width=30)

        #BOTON GENERAR GRÁFICA
        self.botonGenerar = tk.Button(self.ventana, text="GENERAR GRÁFICA", font=("Times New Roman",10), command=self.generar)

        #PREVIEW
        tk.Label(self.ventana, text="Vista del tipo de grafica:", font=("Times New Roman",12,"italic")).pack()
        self.frame_preview = tk.Frame(self.ventana, borderwidth=2, relief="solid")
        self.frame_preview.place(x=30, y=120)

        self.mostrar_preview("lineas")

        #VISTA PREVIA DE LA GRAFICA
        tk.Label(self.ventana,text="Vista previa de la grafica:", font=("Times New Roman",12,"italic")).place(x=470, y=100)
        self.frame_grafica = tk.Frame(self.ventana, borderwidth=2, relief="solid")
        self.frame_grafica.place(x=470, y=120)

        #BOTON SALIR
        botonSalir = tk.Button(self.ventana, text="SALIR", font=("Times New Roman", 10), command=self.salir)
        botonSalir.place(x=1000, y=550)

    def mostrar_campos(self, evento):
        tipo = self.combobox.get()
        if not tipo:
            return

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
        self.texto_dato1.place(x=30, y=300)
        self.datos1.place(x=30, y=325)

        self.texto_dato2.place(x=30, y=375)
        self.datos2.place(x=30, y=400)

        self.texto_nombre.place(x=30, y=450)
        self.nombreArchivo.place(x=30, y=475)

        self.botonGenerar.pack()
        self.botonGenerar.place(x=30, y=520)

        self.mostrar_preview(tipo)

    def mostrar_preview(self,tipo):
        for widget in self.frame_preview.winfo_children():
            widget.destroy()

        fig = self.previews[tipo]
        canvas = FigureCanvasTkAgg(fig,master=self.frame_preview)
        canvas.draw()
        canvas.get_tk_widget().pack()

    #GENERAR GRAFICA
    def generar(self):
        try:
            tipo = self.combobox.get()
            if not tipo:
                messagebox.showinfo("ERROR", "Seleccione una grafica.")
                return

            tipo = self.combobox.get()

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

            #Vista de la grafica
            fig = graficar(",".join(str(i) for i in lista1),",".join(str(i) for i in lista2),tipo, "", "", "",tamaño=(5,4))

            if self.canvas_real:
                self.canvas_real.get_tk_widget().destroy()  # Elimina canvas anterior

            self.canvas_real = FigureCanvasTkAgg(fig, master=self.frame_grafica)
            self.canvas_real.draw()
            self.canvas_real.get_tk_widget().pack()
            plt.close(fig)

        except:
            messagebox.showinfo("ERROR", "Datos invalidos.")

    def salir(self):
        if messagebox.askyesno("Salir", "¿Deseas salir?"):
            self.ventana.destroy()


ventana = tk.Tk()
interfaz = Interfaz(ventana)

ventana.mainloop()