import random
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

def menu():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Ingresa una cadena manualmente")
        print("2. Genera cadenas de prueba")
        print("3. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            cadenas = []
            while True:
                cadena = input("Ingresa la cadena (o '0' para terminar): ")
                if cadena == "0":
                    break
                elif not set(cadena).issubset({"a", "b"}):
                    print("Error: La cadena solo puede contener 'a' y 'b'.")
                else:
                    cadenas.append(cadena)

            if cadenas:
                procesar_cadenas(cadenas)
        elif opcion == "2":
            try:
                n = int(input("¿Cuántas cadenas deseas generar?: "))
                if n <= 0:
                    print("Debe ingresar un número mayor a 0.")
                    continue
                cadenas = [generar_valida() if random.choice([True, False]) else generar_invalida() for _ in range(n)]
                procesar_cadenas(cadenas)
            except ValueError:
                print("Error: Ingresa un número válido.")
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

def procesar_cadenas(cadenas):
    procesadas = set()
    while True:
        print("\nCadenas disponibles:")
        for i, cadena in enumerate(cadenas, 1):
            print(f"  {i}. {cadena}")

        opcion = input("\nElige una cadena por su número (o '0' para volver): ")
        if opcion == "0":
            break

        try:
            indice = int(opcion) - 1
            if 0 <= indice < len(cadenas):
                cadena = cadenas[indice]
                procesadas.add(indice)
                es_aceptada = verificar_cadena(cadena)

                if es_aceptada:
                    print("Cadena aceptada :)")
                    while True:
                        print("\nOpciones adicionales:")
                        print("1. Ver la simulación del autómata de pila")
                        print("2. Ver forma sentencial de derivación de la cadena")
                        print("3. Ver árbol de derivación de la cadena")
                        print("4. Seleccionar otra cadena disponible")
                        opcion = input("Elige una opción: ")

                        if opcion == "1":
                            print(f"\nSimulación del autómata de pila para {cadena}:")
                            simular_automata_pila(cadena)
                        elif opcion == "2":
                            print("\nReglas de producción de la gramática en forma de Chomsky:")
                            print("S → AC | AB")
                            print("A → a")
                            print("B → b")
                            print("C → SB")
                            mostrar_derivacion_leftmost(cadena)
                        elif opcion == "3":
                            print(f"\nÁrbol de derivación de '{cadena}':")
                            construir_arbol_derivacion(cadena)
                        elif opcion == "4":
                            break
                        else:
                            print("Opción inválida. Intenta de nuevo.")
                else:
                    print("Cadena rechazada :(")

            else:
                print("Número fuera de rango.")
        except ValueError:
            print("Error: Ingresa un número válido.")

def generar_valida():
    n = random.randint(1, 50)
    return "a" * n + "b" * n

def generar_invalida():
    n = random.randint(1, 50)
    opciones = [
        "b" * n + "a" * n,
        "a" * (n+1) + "b" * n,
        "a" * n + "b" * (n+1),
        "ab" * n + "b"
    ]
    return random.choice(opciones)

def verificar_cadena(cadena):
    pila = []
    estado = 0  # Para controlar el estado de la lectura de 'a' y 'b'
    
    for char in cadena:
        if char == 'a':
            if estado == 1:  # Si estamos en el estado de leer 'b', no aceptamos más 'a'
                return False
            pila.append('X')  # Empujamos un marcador para cada 'a'
        elif char == 'b':
            if estado == 0:  # Si estamos en el estado 0, no hemos leído 'a' antes
                return False
            if pila:
                pila.pop()  # Sacamos el marcador de la pila por cada 'b'
            else:
                return False  # Si no hay 'X' para hacer pop, significa que la cadena no es válida
            estado = 1  # Ahora estamos leyendo 'b'
        else:
            return False  # Cadena no válida si contiene caracteres distintos de 'a' o 'b'
    
    # Si la pila está vacía, la cadena es válida (cada 'a' tuvo su correspondiente 'b')
    return len(pila) == 0


def simular_automata_pila(cadena):
    pila = []

    for i, char in enumerate(cadena):
        cadena_restante = cadena[i:]
        print(f"Paso {i+1}: Leyendo '{char}'")
        print(f"Cadena restante: {cadena_restante}")
        print(f"Pila antes: {pila}")

        if char == 'a':
            pila.append('X')
        elif char == 'b':
            if pila:
                pila.pop()
            else:
                print("Error: pila vacía. Cadena rechazada")
                return
        print(f"Pila después: {pila}\n")

    if not pila:
        print("Cadena aceptada :)")

def mostrar_derivacion_leftmost(cadena):
    print(f"\nSentential forms in a leftmost derivation of {cadena}:")
    n = len(cadena) // 2  # Número de 'a' y 'b'

    derivacion = ["S"]

    if n > 1:
      # Paso 1: Expandimos 'S' en 'AC'
      derivacion.append("AC")
    else:
      derivacion.append("AB")

    while True:
        ultima = derivacion[-1]
        nueva = list(ultima)  # Convertimos en lista para modificar caracteres

        # 1. Si hay 'A', convertir el más a la izquierda en 'a'
        if "A" in nueva:
            nueva[nueva.index("A")] = "a"
        # 2. Si hay 'S', expandirlo
        elif "S" in nueva:
            idx_s = nueva.index("S")
            if nueva[:idx_s].count("a") < (n - 1):  # Si hay menos de (n-1) 'a' antes de 'S'
                nueva[idx_s:idx_s+1] = list("AC")  # Expandir S → AC
            else:
                nueva[idx_s:idx_s+1] = list("AB")  # Expandir S → AB
        # 3. Si hay 'C' expandir a 'SB'
        elif "C" in nueva:
            nueva[nueva.index("C")] = "SB"
        # 4. Si hay 'B', convertir el más a la izquierda en 'b'
        elif "B" in nueva:
            nueva[nueva.index("B")] = "b"
        else:
            break  # Si ya no hay A, S o B, terminamos

        derivacion.append("".join(nueva))

    # Imprimir la derivación paso a paso
    for paso in derivacion:
        print(paso)

def construir_arbol_derivacion(cadena):
    n = len(cadena) // 2  # Número de 'a' y 'b'
    G = nx.DiGraph()
    posiciones = {}
    nodo_id = 0
    cola = deque()

    def agregar_nodo(padre, etiqueta, nivel, x):
        nonlocal nodo_id
        nodo = nodo_id
        nodo_id += 1
        G.add_node(nodo, label=etiqueta)
        posiciones[nodo] = (x, -nivel)
        if padre is not None:
            G.add_edge(padre, nodo)
        return nodo

    # Inicializar el árbol con la raíz S
    raiz = agregar_nodo(None, "S", 0, 0)
    cola.append((raiz, "S", 0, 0))

    count_S = 0
    while cola:
        padre, etiqueta, nivel, pos_x = cola.popleft()

        if etiqueta == "A":
            agregar_nodo(padre, "a", nivel + 1, pos_x)
        elif etiqueta == "B":
            agregar_nodo(padre, "b", nivel + 1, pos_x)
        elif etiqueta == "C":
            hijo1 = agregar_nodo(padre, "S", nivel + 1, pos_x - 1)
            hijo2 = agregar_nodo(padre, "B", nivel + 1, pos_x + 1)
            cola.append((hijo1, "S", nivel + 1, pos_x - 1))
            cola.append((hijo2, "B", nivel + 1, pos_x + 1))
        elif etiqueta == "S":
            if count_S < n - 1:
                hijo1 = agregar_nodo(padre, "A", nivel + 1, pos_x - 1)
                hijo2 = agregar_nodo(padre, "C", nivel + 1, pos_x + 1)
                cola.append((hijo1, "A", nivel + 1, pos_x - 1))
                cola.append((hijo2, "C", nivel + 1, pos_x + 1))
                count_S += 1
            else:
                hijo1 = agregar_nodo(padre, "A", nivel + 1, pos_x - 1)
                hijo2 = agregar_nodo(padre, "B", nivel + 1, pos_x + 1)
                cola.append((hijo1, "A", nivel + 1, pos_x - 1))
                cola.append((hijo2, "B", nivel + 1, pos_x + 1))

    labels = {n: d["label"] for n, d in G.nodes(data=True)}
    plt.figure(figsize=(5, n + 4))
    nx.draw(G, pos=posiciones, labels=labels, with_labels=True, node_size=2000, node_color="lightblue", font_size=12, font_weight="bold", edge_color="black")
    plt.title(f"Árbol de derivación de '{cadena}'")
    plt.show()

    G.clear()  # Limpiar el grafo después de mostrarlo
    plt.close()

menu()