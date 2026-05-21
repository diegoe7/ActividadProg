import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import tempfile
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from subproceso import graficar

# Generic sample data for combobox previews
SAMPLE_X = "1,2,3,4,5"
SAMPLE_Y = "3,1,4,1,5"

class Interfaz(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("Graficator 3.0")
        self.geometry("1100x650")
        self.resizable(False, False)

        # Track if real graph is showing
        self.preview_real_activa = False

        # Pregenerate generic previews once at startup
        self.previews_genericos = {}
        for tipo in ["linea", "barras", "pie", "dispersion", "linea de tendencia"]:
            fig, _, _ = graficar(SAMPLE_X, SAMPLE_Y, tipo, "", "", tipo)
            self.previews_genericos[tipo] = fig

        self._build_ui()

    def _build_ui(self):
        # ── TITLE ──────────────────────────────────────────────
        tk.Label(self, text="GRAFICATOR 3.0",
                 font=("Times New Roman", 18, "bold")).place(x=400, y=10)

        # ── LEFT PANEL - INPUTS ────────────────────────────────
        tk.Label(self, text="Datos X:",
                 font=("Times New Roman", 11)).place(x=20, y=60)
        self.entry_x = tk.Entry(self, width=35)
        self.entry_x.place(x=20, y=85)

        tk.Label(self, text="Datos Y:",
                 font=("Times New Roman", 11)).place(x=20, y=120)
        self.entry_y = tk.Entry(self, width=35)
        self.entry_y.place(x=20, y=145)

        tk.Label(self, text="Tipo de grafica:",
                 font=("Times New Roman", 11)).place(x=20, y=190)
        self.combobox = ttk.Combobox(self,
                        values=["linea", "barras", "pie",
                                "dispersion", "linea de tendencia"],
                        state="readonly", width=32)
        self.combobox.set("linea")
        self.combobox.place(x=20, y=215)
        self.combobox.bind("<<ComboboxSelected>>", self._on_combobox_change)

        # ── CHECKBUTTON ────────────────────────────────────────
        self.check_var = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(self,
                           text="Agregar título y etiquetas",
                           font=("Times New Roman", 11),
                           variable=self.check_var,
                           command=self._toggle_labels)
        self.checkbutton.place(x=20, y=260)

        # ── LABEL FIELDS (hidden by default) ──────────────────
        self.label_titulo = tk.Label(self, text="Título:",
                                     font=("Times New Roman", 11))
        self.entry_titulo = tk.Entry(self, width=35)

        self.label_eje_x = tk.Label(self, text="Etiqueta Eje X:",
                                    font=("Times New Roman", 11))
        self.entry_eje_x = tk.Entry(self, width=35)

        self.label_eje_y = tk.Label(self, text="Etiqueta Eje Y:",
                                    font=("Times New Roman", 11))
        self.entry_eje_y = tk.Entry(self, width=35)

        # ── BUTTONS ────────────────────────────────────────────
        self.btn_preview = tk.Button(self, text="Vista previa",
                            font=("Times New Roman", 11),
                            command=self._on_preview)
        self.btn_preview.place(x=20, y=580)

        self.btn_guardar = tk.Button(self, text="Guardar",
                            font=("Times New Roman", 11),
                            command=self._on_guardar)
        self.btn_guardar.place(x=130, y=580)

        self.btn_salir = tk.Button(self, text="Salir",
                          font=("Times New Roman", 11),
                          command=self._on_salir)
        self.btn_salir.place(x=1020, y=610)

        # ── GENERIC PREVIEW FRAME ──────────────────────────────
        tk.Label(self, text="Vista previa del tipo de gráfica:",
                 font=("Times New Roman", 10, "italic")).place(x=390, y=55)
        self.frame_generico = tk.Frame(self, borderwidth=2, relief="solid")
        self.frame_generico.place(x=390, y=80, width=320, height=250)

        # ── REAL PREVIEW FRAME ─────────────────────────────────
        tk.Label(self, text="Vista previa de tu gráfica:",
                 font=("Times New Roman", 10, "italic")).place(x=730, y=55)
        self.frame_real = tk.Frame(self, borderwidth=2, relief="solid")
        self.frame_real.place(x=730, y=80, width=340, height=250)

        # Show default generic preview
        self._mostrar_preview_generico("linea")

    def _toggle_labels(self):
        if self.check_var.get():
            # Show label fields
            self.label_titulo.place(x=20, y=295)
            self.entry_titulo.place(x=20, y=318)
            self.label_eje_x.place(x=20, y=353)
            self.entry_eje_x.place(x=20, y=376)
            self.label_eje_y.place(x=20, y=411)
            self.entry_eje_y.place(x=20, y=434)
        else:
            # Hide label fields
            self.label_titulo.place_forget()
            self.entry_titulo.place_forget()
            self.label_eje_x.place_forget()
            self.entry_eje_x.place_forget()
            self.label_eje_y.place_forget()
            self.entry_eje_y.place_forget()

    def _on_combobox_change(self, event):
        tipo = self.combobox.get()
        # Always update generic preview
        self._mostrar_preview_generico(tipo)
        # If real graph was showing, keep it but bring back generic too
        if self.preview_real_activa:
            self.preview_real_activa = False

    def _mostrar_preview_generico(self, tipo):
        for widget in self.frame_generico.winfo_children():
            widget.destroy()
        fig = self.previews_genericos[tipo]
        canvas = FigureCanvasTkAgg(fig, master=self.frame_generico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def mostrar_grafico_real(self, ruta):
        # Clear generic preview
        for widget in self.frame_generico.winfo_children():
            widget.destroy()
        # Show real graph
        for widget in self.frame_real.winfo_children():
            widget.destroy()
        img = tk.PhotoImage(file=ruta)
        label = tk.Label(self.frame_real, image=img)
        label.image = img  # keep reference
        label.pack(fill=tk.BOTH, expand=True)
        self.preview_real_activa = True

    def _on_preview(self):
        dat_x = self.entry_x.get()
        dat_y = self.entry_y.get()
        tipo = self.combobox.get()
        titulo = self.entry_titulo.get() if self.check_var.get() else ""
        eje_x = self.entry_eje_x.get() if self.check_var.get() else ""
        eje_y = self.entry_eje_y.get() if self.check_var.get() else ""

        if not dat_x or not dat_y:
            messagebox.showerror("Error", "Por favor ingrese los datos X e Y")
            return

        self.controlador.preview(dat_x, dat_y, tipo, eje_x, eje_y, titulo)

    def _on_guardar(self):
        dat_x = self.entry_x.get()
        dat_y = self.entry_y.get()
        tipo = self.combobox.get()
        titulo = self.entry_titulo.get() if self.check_var.get() else ""
        eje_x = self.entry_eje_x.get() if self.check_var.get() else ""
        eje_y = self.entry_eje_y.get() if self.check_var.get() else ""

        if not dat_x or not dat_y:
            messagebox.showerror("Error", "Por favor ingrese los datos X e Y")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg")],
            title="Guardar grafico"
        )

        if ruta:  # user didn't cancel
            self.controlador.guardar(dat_x, dat_y, tipo, eje_x, eje_y, titulo, ruta)

    def _on_salir(self):
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
        self.ruta_actual = ruta
        self.modo = guardado
        arg = [sys.executable, "subproceso.py",  # ✅
               dat_x, dat_y, tipo,
               x_label or "", y_label or "", titulo or "",
               ruta, guardado]
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
                    messagebox.showinfo("Grafico guardado", "El grafico fue guardado exitosamente")
            else:
                error = self.proceso.stderr.read()
                messagebox.showerror("Error", f"{error}")  # ✅

    def ejecutar(self):
        self.vista.mainloop()

if __name__ == "__main__":
    app = Controlador()
    app.ejecutar()
