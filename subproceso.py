try:

    import sys
    import os
    import matplotlib.pyplot as plt
    import numpy as np

except ImportError as e:
    print(f"Error al importar librerias: {e}")
    sys.exit(1)

def graficar(datosx, datosy, tipo, x_label, y_label, titulo, tamano=None):

    x = [i.strip() for i in datosx.split(',')]
    y = [i.strip() for i in datosy.split(',')]

    if len(x) != len(y):
        raise ValueError("Las listas de datos no tienen la misma longitud")
    
    if "" in x or "" in y:
        raise ValueError("Existen valores vacios, en la lista de datos")
    
    try:
        num_y = [float(i) for i in y]
    except ValueError:
        raise ValueError("La lista de datos Y contiene valores no numericos")
    
    graf_mat = ["Linea", "Linea de tendencia", "Dispersion"]
    num_x = []
    if tipo in graf_mat:
        try:
            num_x = [float(i) for i in x]
        except ValueError:
            raise ValueError("La lista de datos X contiene valores no numericos")
        
    if tamano:
        fig, ax = plt.subplots(figsize=tamano)
    else:
        fig, ax = plt.subplots()

    if x_label: ax.set_xlabel(x_label)
    if y_label: ax.set_ylabel(y_label)
    if titulo: ax.set_title(titulo)

    lista_colores = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange', 'tab:purple', 'tab:yellow', 'tab:turquoise', 'tab:coral', 'tab:gray']
    colores = []

    for i in range(len(x)):
        col_i = i % len(lista_colores)
        col_escogido = lista_colores[col_i]
        colores.append(col_escogido)

    if tipo == 'Linea':
        ax.plot(num_x, num_y, marker='o', color='green')

    elif tipo == 'Barras':
        ax.bar(x, num_y, color=colores)

    elif tipo == 'Pie':
        for i in num_y:
            if i < 0:
                raise ValueError("El grafico no puede tener valores negativos")
        if sum(num_y) == 0:
            raise ValueError("La suma de los valores no puede ser cero")
        ax.pie(num_y, labels=x, colors=colores, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

    elif tipo == 'Linea de tendencia':
        if len(x) < 2:
            raise ValueError("Se necesitan al menos dos puntos para calcular la línea de tendencia")
        num_x = np.array(num_x)
        num_y = np.array(num_y)
        a, b = np.polyfit(num_x, num_y, deg = 1)
        tendencia = a * num_x + b
        ax.plot(num_x, num_y, marker='o', linestyle='', color='blue')
        ax.plot(num_x, tendencia, color='red')
    
    else:
        ax.scatter(num_x, num_y, color='purple')

    return fig, x, y

def graficaryguardar(datosx, datosy, tipo, x_label, y_label, titulo, ruta, guardado):
        
    carpeta = os.path.dirname(ruta)
    if carpeta:
        try:            
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
                print(f"Carpeta '{carpeta}' creada")
        except OSError as e:
            print(f"Error al crear la carpeta: {e}")

    fig, x, y = graficar(datosx, datosy, tipo, x_label, y_label, titulo)
    fig.savefig(ruta)
    plt.close(fig)

    if guardado == "Guardar":
        nombre_archivo, _ = os.path.splitext(ruta)
        try:
            with open(f"{nombre_archivo}_data.txt", 'w') as txt_file:
                txt_file.write(f"Tipo de grafico: {tipo}\n")
                for i in range(len(x)):
                    txt_file.write(f"{x[i]}: {y[i]}\n")
        except OSError as e:
            print(f"Error al guardar los datos: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        dat_x = sys.argv[1]
        dat_y = sys.argv[2]
        tipo_g = sys.argv[3]
        x_lab = sys.argv[4]
        y_lab = sys.argv[5]
        titu = sys.argv[6]
        rut = sys.argv[7]
        guardado = sys.argv[8]

        graficaryguardar(dat_x, dat_y, tipo_g, x_lab, y_lab, titu, rut, guardado)
        sys.exit(0)

    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
