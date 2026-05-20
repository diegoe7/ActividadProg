import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class Graficador:
    def __init__(self):
        self.ejex= []
        self.ejey= np.array([])

    def cargar_datos(self,x,y):
        self.ejex= x
        self.ejey= np.array(y)
        
    def generar_grafica(self,tipo):
        fig, ax = plt.subplots(figsize=(5.5, 3.5))

        graficas = {
            "barras":
                lambda: ax.bar(self.ejex,self.ejey,color="lightgreen",edgecolor="black"),
            "lineas":
                lambda: ax.plot(self.ejex,self.ejey,color="blue",marker="o",linewidth=3),
            "scatter":
                lambda: ax.scatter(self.ejex,self.ejey,facecolor='C0', edgecolor='k'),
            "histograma":
                lambda: ax.hist(self.ejey,color="lightpink",edgecolor="black",linewidth=2),
            "torta":
                lambda: ax.pie(self.ejey,labels=self.ejex,autopct='%1.1f%%')
        }

        funcion= graficas.get(tipo)
        if funcion:
            funcion()
            ax.set_title(f"Grafica {tipo}")
            if tipo != "torta":  # La torta no usa ejes XY
                ax.set_xlabel("EJE X")
                ax.set_ylabel("EJE Y")
            return fig
        else: 
            print("Tipo invalido")
            return None