import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import tempfile
import os

#Esta clase se mueve al nuevo archivo
#class DataProcessor:
#   def __init__(self):
#       self.x_data = []
#       self.y_data = []

#   def process_input(self, raw_x, raw_y):
#       self.x_data = [int(i.strip()) for i in raw_x.split(',')]
#       self.y_data = [int(i.strip()) for i in raw_y.split(',')]
#       return self.x_data, self.y_data

# --- VIEW (Expanded UI) ---
class Interfaz(tk.Tk):
#   def __init__(self, controller):
#       super().__init__()
#       self.controller = controller
#       self.title("Data Grapher Pro")
#       
        # 1. Top Frame for Inputs to keep things organized
#       input_frame = tk.Frame(self)
#       input_frame.pack(pady=10)

#       tk.Label(input_frame, text="X Values:").grid(row=0, column=0)
#       self.entry_x = tk.Entry(input_frame)
#       self.entry_x.grid(row=0, column=1)

#       tk.Label(input_frame, text="Y Values:").grid(row=1, column=0)
#       self.entry_y = tk.Entry(input_frame)
#       self.entry_y.grid(row=1, column=1)

        # 2. Dropdown for Graph Type
#       tk.Label(input_frame, text="Graph Type:").grid(row=2, column=0)
#       self.graph_type_var = tk.StringVar(value="Line") # Default value
#       self.dropdown = ttk.Combobox(input_frame, textvariable=self.graph_type_var, state="readonly")
#       self.dropdown['values'] = ("Line", "Bar", "Scatter")
#       self.dropdown.grid(row=2, column=1, pady=5)
        
        # 3. Buttons Frame
#      btn_frame = tk.Frame(self)
#        btn_frame.pack(pady=5)

#       self.plot_btn = tk.Button(btn_frame, text="Draw Graph", command=self.on_plot_click)
#       self.plot_btn.grid(row=0, column=0, padx=5)

#       self.save_btn = tk.Button(btn_frame, text="Save Graph", command=self.on_save_click)
#      self.save_btn.grid(row=0, column=1, padx=5)

        # Matplotlib Figure setup
#       self.figure = Figure(figsize=(5, 4), dpi=100)
#       self.ax = self.figure.add_subplot(111)
#       self.canvas = FigureCanvasTkAgg(self.figure, self)
#       self.canvas.get_tk_widget().pack()

#   def on_plot_click(self):
        # Pass the inputs AND the selected graph type to the controller
#       self.controller.generate_graph(self.entry_x.get(), self.entry_y.get(), self.graph_type_var.get())

#   def on_save_click(self):
        # Open a "Save As" dialog. It returns a string of the chosen file path.
#       file_path = filedialog.asksaveasfilename(
#          defaultextension=".png", 
#            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
#           title="Choose where to save your graph"
#       )
        
        # If the user didn't click 'Cancel', send the path to the controller
#       if file_path:
#          self.controller.save_graph(file_path)

#   def draw_plot(self, x, y, graph_type):
#       self.ax.clear()
        
        # Draw different graphs based on the dropdown selection
#       if graph_type == "Bar":
#           self.ax.bar(x, y, color='skyblue')
#       elif graph_type == "Scatter":
#           self.ax.scatter(x, y, color='red')
#       else:
#           self.ax.plot(x, y, marker='o', color='green')
            
#       self.canvas.draw()

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
        arg = ["python", "Sub.py", dat_x, dat_y, tipo, x_label, y_label, titulo, ruta, guardado]

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
                    messagebox.showinfo("Grafico guardado")
            else:
                error = self.proceso.stderr.read()
                messagebox.showerror(f"Error: {error}")

    def ejecutar(self):
        self.vista.mainloop()

if __name__ == "__main__":    
    app = Controlador()
    app.ejecutar()
