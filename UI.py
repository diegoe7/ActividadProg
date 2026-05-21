import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import tempfile
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from subproceso import graficar

ejemplo_x = "1, 2, 3, 4, 5"
ejemplo_y = "10, 20, 15, 25, 30"

nombres = {
    "Linea":("Datos X:", "Datos Y:"),
    "Barras":("Categorias:", "Valores:"),
    "Pie":("Etiquetas:", "Valores:"),
    "Linea de tendencia":("Datos X:", "Datos Y:"),
    "Dispersion":("Datos X:", "Datos Y:")
}

class Interfaz(tk.Tk):
    def __init__ (self,controlador):
        super().__init__()
        self.controlador = controlador
        self.title("Graficador")
        self.geometry("1100x650")
        self.resizable(False, False)
        self.vist_pre_act = False
        self.vist_pre_gen = {}

        for tipo in ["Linea", "Barras", "Pie", "Linea de tendencia", "Dispersion"]:
            fig, _, _ = graficar(ejemplo_x, ejemplo_y, tipo, "", "", tipo, tamano=(2.5,1.5))
            self.vist_pre_gen[tipo] = fig
        
        self.crear_vista(self)

    def crear_vista(self):
        tk.Label(self, text="GRAFICATOR 3.0", font=("Times New Roman", 20)).place(x=400, y=10)

        tk.Label(self, text="Seleccione el tipo de grafica:", font=("Times New Roman", 12)).place(x=20, y=60)
        self.combobox = ttk.Combobox(self, values=["Linea", "Barras", "Pie", "Linea de tendencia", "Dispersion"], state="readonly", width=20)
        self.combobox.set("Linea")
        self.combobox.place(x=20, y=85)
        self.combobox.bind("<<ComboboxSelected>>", self.op_combobox)

        self.nombre_x = tk.Label(self, text="Datos X:", font=("Times New Roman", 12))
        self.nombre_x.place(x=20, y=120)
        self.entrada_x = tk.Entry(self, width=35)
        self.entrada_x.place(x=20, y=145)

        self.nombre_y = tk.Label(self, text="Datos Y:", font=("Times New Roman", 12))
        self.nombre_y.place(x=20, y=190)
        self.entrada_y = tk.Entry(self, width=35)
        self.entrada_y.place(x=20, y=215)

        self.var_check = tk.BooleanVar()
        tk.Checkbutton(self, text="Agregar etiquetas y titulo", variable=self.var_check, command=self.mostrar_etiquetas).place(x=20, y=260)

        self.nom_titulo = tk.Label(self, text="Titulo:", font=("Times New Roman", 12))
        self.ent_titulo = tk.Entry(self, width=35)

        self.nom_x = tk.Label(self, text="Etiqueta eje X:", font=("Times New Roman", 12))
        self.ent_x = tk.Entry(self, width=35)
        self.nom_y = tk.Label(self, text="Etiqueta eje Y:", font=("Times New Roman", 12))
        self.ent_y = tk.Entry(self, width=35)

        tk.Button(self, text="Generar grafico", command=self.vista_previa).place(x=40, y=580)
        tk.Button(self, text="Guardar grafico", command=self.guardar_grafico).place(x=140, y=580)
        tk.Button(self, text="Salir", command=self.salir).place(x=1020, y=580)

        tk.Label(self, text="Grafico ejemplo:", font=("Times New Roman", 12)).place(x=400, y=60)
        self.recuadro1 = tk.Frame(self, borderwidth=1,relief="solid")
        self.recuadro1.place(x=400, y=80, width=150, height=100)

        tk.Label(self, text="Grafico generado:", font=("Times New Roman", 12)).place(x=730, y=60)
        self.recuadro2 = tk.Frame(self, borderwidth=1,relief="solid")
        self.recuadro2.place(x=730, y=80, width=340, height=250)

        self.mostrar_gen("Linea")
    
    def mostrar_etiquetas(self):
        tipo = self.combobox.get()
        if self.var_check.get():
            self.nom_titulo.place(x=20, y=300)
            self.ent_titulo.place(x=20, y=325)
            if tipo != "Pie":
                self.nom_x.place(x=20, y=370)
                self.ent_x.place(x=20, y=395)
                self.nom_y.place(x=20, y=440)
                self.ent_y.place(x=20, y=465)
        else:
            self.nom_titulo.place_forget()
            self.ent_titulo.place_forget()
            self.nom_x.place_forget()
            self.ent_x.place_forget()
            self.nom_y.place_forget()
            self.ent_y.place_forget()

    def op_combobox(self, opcion):
        tipo = self.combobox.get()
        nomx, nomy = nombres[tipo]
        self.nom_x.config(text=nomx)
        self.nom_y.config(text=nomy)
        self.mostrar_gen(tipo)

        if self.var_check.get():
            self.mostrar_etiquetas()

        if self.vist_pre_act:
            self.vist_pre_act = False
    
    def mostrar_gen(self, tipo):
        for widget in self.recuadro1.winfo_children():
            widget.destroy()
        fig = self.vist_pre_gen[tipo]
        canvas = FigureCanvasTkAgg(fig, master=self.recuadro1)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def mostrar_grafico(self, ruta):
        for widget in self.recuadro2.winfo_children():
            widget.destroy()
        img = tk.PhotoImage(file=ruta)
        etiqueta = tk.Label(self.recuadro2, image=img)
        etiqueta.image = img
        etiqueta.pack(fill=tk.BOTH, expand=True)
        self.vist_pre_act = True

    def vista_previa(self):
        dat_x = self.entrada_x.get()
        dat_y = self.entrada_y.get()
        tipo = self.combobox.get()
        titulo = self.ent_titulo.get() if self.var_check.get() else ""
        x_label = self.ent_x.get() if self.var_check.get() and tipo != "Pie" else ""
        y_label = self.ent_y.get() if self.var_check.get() and tipo != "Pie" else ""

        if not dat_x or not dat_y:
            messagebox.showinfo("ERROR", "Ingrese los datos para generar la grafica")
            return
        
        self.controlador.preview(dat_x, dat_y, tipo, x_label, y_label, titulo)        

    def guardar_grafico(self):
        dat_x = self.entrada_x.get()
        dat_y = self.entrada_y.get()
        tipo = self.combobox.get()
        titulo = self.ent_titulo.get() if self.var_check.get() else ""
        x_label = self.ent_x.get() if self.var_check.get() and tipo != "Pie" else ""
        y_label = self.ent_y.get() if self.var_check.get() and tipo != "Pie" else ""

        if not dat_x or not dat_y:
            messagebox.showinfo("ERROR", "Ingrese los datos para generar la grafica")
            return
        
        ruta = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")], title="Guardar grafico")

        if ruta:
            self.controlador.guardar(dat_x, dat_y, tipo, x_label, y_label, titulo, ruta)     

    def salir(self):
        if messagebox.askyesno("Salir", "¿Deseas salir?"):
            self.destroy()

class Controlador:
    def __init__(self):
        self.vista = Interfaz(self)

    def preview(self, dat_x, dat_y, tipo, x_label, y_label, titulo):
        ruta_temp = os.path.join(tempfile.gettempdir(), "grafico_temp.png")
        self.crear_daemon(dat_x, dat_y, tipo, x_label, y_label, titulo, ruta_temp, guardado="Vista previa")

    def guardar(self, dat_x, dat_y, tipo, x_label, y_label, titulo, ruta_final):
        self.crear_daemon(dat_x, dat_y, tipo, x_label, y_label, titulo, ruta_final, guardado="Guardar")

    def crear_daemon(self, dat_x, dat_y, tipo, x_label, y_label, titulo, ruta, guardado):
        # Anadir excepciones
        
        self.ruta_actual = ruta
        self.modo = guardado
        arg = [sys.executable, "Subproceso.py", dat_x, dat_y, tipo, x_label, y_label, titulo, ruta, guardado]

        try:
            self.proceso = subprocess.Popen(arg, stderr=subprocess.PIPE, text=True)
            self.estado_proceso()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar el subproceso: {e}")
        
    def estado_proceso(self):
        if self.proceso.poll() is None:
            self.vista.after(100, self.estado_proceso)
        else:
            if self.proceso.returncode == 0:
                if self.modo == "Vista previa":
                    self.vista.mostrar_grafico(self.ruta_actual)
                elif self.modo == "Guardar":
                    messagebox.showinfo("Grafico guardado", "El grafico se guardo exitosamente")
            else:
                error = self.proceso.stderr.read()
                messagebox.showerror("Error", f"{error}")

    def ejecutar(self):
        self.vista.mainloop()

if __name__ == "__main__":    
    app = Controlador()
    app.ejecutar()
