import heapq
import random
import math
import tkinter as tk
from tkinter import simpledialog

def ask_string(prompt, title="Entrada"):
    """
    Abre una ventana emergente para que el usuario ingrese un texto.
    """
    root = tk.Tk()
    root.withdraw() 
    result = simpledialog.askstring(title, prompt)
    root.destroy()
    if result:
        return result.strip()
    return None

def ask_int(prompt, title="Entrada"):
    """
    Abre una ventana emergente para que el usuario ingrese un número entero.
    """
    root = tk.Tk()
    root.withdraw()
    result = simpledialog.askinteger(title, prompt)
    root.destroy()
    return result

def calcular_heuristica(nodo, destino):
    """
    Estima el tiempo restante (en minutos) desde 'nodo' hasta 'destino'.
    Se utiliza la diferencia entre los valores ASCII del primer caracter de cada nombre.
    """
    if nodo == destino:
        return 0
    return abs(ord(nodo[0]) - ord(destino[0]))

def buscar_ruta(grafo, inicio, destino):
    """
    Implementa el algoritmo A* separando el costo real (g) y el valor acumulado (f).

    Parametros:
      - grafo: diccionario donde cada clave es una estacion y su valor es una lista de tuplas 
               (estacion vecina, tiempo en minutos para llegar a ella).
      - inicio: estacion de partida.
      - destino: estacion de llegada.
      
    Retorna:
      - Una lista con la ruta optima.
      - El costo real total (g) en minutos.
    """
    # La cola contiene tuplas de la forma (f, g, nodo, ruta)
    cola = []
    g_inicial = 0
    f_inicial = g_inicial + calcular_heuristica(inicio, destino)
    heapq.heappush(cola, (f_inicial, g_inicial, inicio, [inicio]))
    visitados = set()

    while cola:
        f, g, nodo_actual, ruta = heapq.heappop(cola)
        if nodo_actual == destino:
            return ruta, g  # Retorna la ruta y el costo real
        
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        
        for vecino, tiempo in grafo.get(nodo_actual, []):
            nuevo_g = g + tiempo
            nuevo_f = nuevo_g + calcular_heuristica(vecino, destino)
            nueva_ruta = ruta + [vecino]
            heapq.heappush(cola, (nuevo_f, nuevo_g, vecino, nueva_ruta))
    
    return None, float('inf')

def crear_grafo_manual():
    """
    Permite al usuario crear un grafo manualmente mediante ventanas emergentes.
    Se asume que el usuario ingresa:
      - Estaciones (por ejemplo: Tunal, Biblioteca, etc.).
      - Número de conexiones para cada estacion y el tiempo (en minutos) para cada conexion.
    """
    grafo = {}
    num_nodos = ask_int("Ingrese la cantidad de estaciones (nodos):", "Creacion de Grafo")
    if num_nodos is None:
        return grafo
    nodos = []
    for i in range(num_nodos):
        nodo = ask_string(f"Ingrese el nombre de la estacion {i+1}:", "Creacion de Grafo")
        if nodo:
            nodos.append(nodo.upper())
    
    for nodo in nodos:
        num_conexiones = ask_int(f"¿Cuantas conexiones tiene la estacion {nodo}?", "Conexiones")
        conexiones = []
        if num_conexiones is None:
            num_conexiones = 0
        for i in range(num_conexiones):
            vecino = ask_string(f"Ingrese el nombre de la estacion conectada a {nodo} (ej: BIBLIOTECA):", "Conexiones")
            if vecino is None:
                continue
            tiempo = ask_int(f"Ingrese el tiempo en minutos desde {nodo} hasta {vecino.upper()}:", "Tiempo")
            if tiempo is None:
                tiempo = 0
            conexiones.append((vecino.upper(), tiempo))
        grafo[nodo] = conexiones
    return grafo

def crear_grafo_aleatorio_complejidad():
    """
    Genera un grafo de forma aleatoria en funcion de la complejidad elegida:
      - Complejidad 1: 3 estaciones, cada una con entre 0 y 3 conexiones.
      - Complejidad 2: 4 estaciones, cada una con entre 1 y 3 conexiones.
      - Complejidad 3: 5 estaciones, cada una con entre 1 y 3 conexiones.
    Los tiempos para cada conexion se asignan aleatoriamente entre 1 y 10 minutos.
    Nota: Se ajusta el maximo de conexiones al maximo posible (número de estaciones - 1).
    """
    prompt = (
        "Seleccione la complejidad del grafo:\n\n"
        "1. 3 estaciones, cada una con entre 0 y 3 conexiones.\n"
        "2. 4 estaciones, cada una con entre 1 y 3 conexiones.\n"
        "3. 5 estaciones, cada una con entre 1 y 3 conexiones.\n\n"
        "Ingrese un número (1-3):"
    )
    complexity = ask_int(prompt, "Complejidad del Grafo")
    if complexity not in [1, 2, 3]:
        print("Complejidad no valida. Se usara 1 por defecto.")
        complexity = 1
    
    if complexity == 1:
        num_stations = 3
        min_conexiones, max_conexiones = 0, 3
    elif complexity == 2:
        num_stations = 4
        min_conexiones, max_conexiones = 1, 3
    else:  # complexity == 3
        num_stations = 5
        min_conexiones, max_conexiones = 1, 3
    
    max_possible = num_stations - 1
    if max_conexiones > max_possible:
        max_conexiones = max_possible
    
    # Generar nombres de estaciones: se usan letras consecutivas a partir de 'A'
    nodos = [chr(ord('A') + i) for i in range(num_stations)]
    grafo = {}
    
    for nodo in nodos:
        num_conexiones = random.randint(min_conexiones, max_conexiones)
        posibles_conexiones = [x for x in nodos if x != nodo]
        num_conexiones = min(num_conexiones, len(posibles_conexiones))
        conexiones_elegidas = random.sample(posibles_conexiones, num_conexiones)
        conexiones = [(vecino, random.randint(1, 10)) for vecino in conexiones_elegidas]
        grafo[nodo] = conexiones
    
    return grafo

def mostrar_grafo_tabla(grafo):
    """
    Muestra el grafo en una tabla ordenada con encabezados:
    Estacion | Conexiones (Estacion - Tiempo)
    """
    print("\nGrafo del Sistema de Transporte:")
    print("-" * 50)
    print("{:<12} | {:<30}".format("Estacion", "Conexiones (Estacion - Tiempo)"))
    print("-" * 50)
    for estacion, conexiones in grafo.items():
        if conexiones:
            conexiones_str = ", ".join([f"{vecino} - {tiempo}min" for vecino, tiempo in conexiones])
        else:
            conexiones_str = "Sin conexiones"
        print("{:<12} | {:<30}".format(estacion, conexiones_str))
    print("-" * 50)

def mostrar_mapa(grafo, ruta_optima):
    """
    Dibuja un mapa simple en una ventana emergente usando Tkinter Canvas.
    Cada estacion se coloca en un arreglo circular.
    Se dibujan las conexiones y se muestra la orientacion:
      - Si la relacion es bidireccional se dibujan flechas en ambos extremos (arrow="both").
      - Si es unidireccional se dibuja la flecha en la direccion permitida (arrow="last").
    Ademas, se muestra el tiempo (minutos) en el punto medio de cada conexion.
    Las flechas se dibujan con un arrowshape mayor para hacerlas mas notables.
    """
    window = tk.Tk()
    window.title("Mapa del Sistema de Transporte")
    canvas_width = 600
    canvas_height = 600
    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()

    # Distribuir las estaciones en un circulo
    nodes = list(grafo.keys())
    num_nodes = len(nodes)
    r_circle = min(canvas_width, canvas_height) // 3
    center_x = canvas_width // 2
    center_y = canvas_height // 2
    positions = {}
    
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / num_nodes
        x = center_x + r_circle * math.cos(angle)
        y = center_y + r_circle * math.sin(angle)
        positions[node] = (x, y)
        # Dibujar la estacion
        canvas.create_oval(x-10, y-10, x+10, y+10, fill="lightblue")
        canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))
    
    drawn_edges = set()
    
    # Dibujar conexiones con orientacion, flechas mas notables y mostrar el tiempo
    for estacion, conexiones in grafo.items():
        for vecino, tiempo in conexiones:
            if (estacion, vecino) in drawn_edges:
                continue
            x1, y1 = positions[estacion]
            x2, y2 = positions[vecino]
            
            # Verificar si existe la conexion inversa para determinar bidireccionalidad
            bidireccional = False
            if vecino in grafo:
                for rev_vecino, _ in grafo[vecino]:
                    if rev_vecino == estacion:
                        bidireccional = True
                        break
            
            arrow_style = "both" if bidireccional else "last"
            if bidireccional:
                drawn_edges.add((estacion, vecino))
                drawn_edges.add((vecino, estacion))
            else:
                drawn_edges.add((estacion, vecino))
            
            # Dibujar la linea con mayor grosor, color y un arrowshape mayor
            canvas.create_line(x1, y1, x2, y2,
                               fill="black",
                               dash=(4,4),
                               arrow=arrow_style,
                               arrowshape=(16,20,8),
                               width=2)
            # Calcular el punto medio para mostrar el tiempo
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            canvas.create_text(mid_x, mid_y,
                               text=f"{tiempo} min",
                               font=("Arial", 10),
                               fill="black")
    
    # Resaltar la ruta optima con linea roja, flecha y arrowshape mayor
    if ruta_optima:
        for i in range(len(ruta_optima)-1):
            node1 = ruta_optima[i]
            node2 = ruta_optima[i+1]
            x1, y1 = positions[node1]
            x2, y2 = positions[node2]
            canvas.create_line(x1, y1, x2, y2,
                               fill="red",
                               width=3,
                               arrow="last",
                               arrowshape=(16,20,8))
    
    window.mainloop()

def main():
    modo = ask_string("¿Desea ingresar el grafo manualmente (M) o generarlo automaticamente (A)? [M/A]:", "Modo de Creacion")
    if modo is None:
        print("No se ingreso una opcion valida.")
        return
    modo = modo.upper()
    
    if modo == 'M':
        sistema_transporte = crear_grafo_manual()
    else:
        sistema_transporte = crear_grafo_aleatorio_complejidad()
    
    mostrar_grafo_tabla(sistema_transporte)
    
    inicio = ask_string("Ingrese la estacion de inicio:", "Ruta")
    if inicio is None:
        print("No se ingreso la estacion de inicio.")
        return
    destino = ask_string("Ingrese la estacion de destino:", "Ruta")
    if destino is None:
        print("No se ingreso la estacion de destino.")
        return
    
    inicio = inicio.upper()
    destino = destino.upper()
    
    print(f"\nBuscando la ruta optima desde {inicio} hasta {destino}...\n")
    ruta_optima, costo_real = buscar_ruta(sistema_transporte, inicio, destino)
    
    if ruta_optima is not None:
        print("\nRuta optima encontrada:")
        print(" -> ".join(ruta_optima))
        print("Costo real del trayecto:", costo_real, "minutos")
        mostrar_mapa(sistema_transporte, ruta_optima)
    else:
        print("No se encontro una ruta valida entre los puntos especificados.")

if __name__ == "__main__":
    main()
