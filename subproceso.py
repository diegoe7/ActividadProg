import sys
import os
import matplotlib.pyplot as plt
import numpy as np

def graficar_guardar(datosx, datosy, tipo, x_label, y_label, titulo, ruta):
    
    carpeta = os.path.dirname(ruta)
    if carpeta:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            print(f"Carpeta '{carpeta}' creada")
        else:
            print(f"la carpeta '{carpeta}' ya existe")

    x = [i.strip() for i in datosx.split(',')]
    y = [float(i.strip()) for i in datosy.split(',')]

    if len(x) != len(y):
        raise ValueError("Las listas de datos no tienen la misma longitud")

    if x_label: ax.set_xlabel(x_label)
    if y_label: ax.set_ylabel(y_label)
    if titulo: ax.set_title(titulo)

    lista_colores = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange', 'tab:purple', 'tab:yellow', 'tab:turquoise', 'tab:coral', 'tab:gray']
    colores = []

    for i in range(len(x)):
        col_i = i % len(lista_colores)
        col_escogido = lista_colores[col_i]
        colores.append(col_escogido)

    fig, ax = plt.subplots()

    if tipo == 'linea':
        num_x = [float(i) for i in x]
        ax.plot(num_x, y, marker='o', color='green')

    elif tipo == 'barras':
        ax.bar(x, y, color=colores)

    elif tipo == 'pie':
        ax.pie(y, labels=x, color=colores, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

    elif tipo == 'linea de tendencia':
        num_x = np.array([float(i) for i in x])
        num_y = np.array(y)
        a, b = np.polyfit(num_x, num_y, deg = 1)
        tendencia = a * num_x + b
        ax.plot(num_x, num_y, marker='o', linestyle='', color='blue')
        ax.plot(num_x, tendencia, color='red')

    elif tipo == 'linea de tendencia' and len(x) < 2:
        raise ValueError("Se necesitan al menos dos puntos para calcular la línea de tendencia")
    
    else:
        num_x = [float(i) for i in x]
        ax.scatter(num_x, y, color='purple')

    plt.savefig(ruta)

if __name__ == "__main__":
    try:
        dat_x = sys.argv[1]
        dat_y = sys.argv[2]
        tipo_g = sys.argv[3]
        x_lab = sys.argv[4]
        y_lab = sys.argv[5]
        titu = sys.argv[6]
        rut = sys.argv[7]
        graficar_guardar(dat_x, dat_y, tipo_g, x_lab, y_lab, titu, rut)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
