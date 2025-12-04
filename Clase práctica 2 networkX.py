import networkx as nx
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Proceso de contagio simple: una iteración
# ---------------------------------------------------------
def propagate_simple(G):
    """
    Realiza un paso de tiempo de un proceso de contagio simple en el grafo G.
    
    Cada nodo debe tener un atributo booleano 'infected' que indica si está infectado.
    La función modifica el grafo en sitio (in-place) y no devuelve nada.
    Regla: un nodo sano se infecta si tiene al menos un vecino infectado.
    """
    # Conjunto de nodos que pasarán a estar infectados en este paso
    to_infect = set()
    
    # Recorremos todos los nodos del grafo
    for v in G.nodes():
        # Si el nodo NO está infectado, miramos sus vecinos
        if not G.nodes[v].get("infected", False):
            for w in G.neighbors(v):
                # Si algún vecino está infectado, marcamos v para infectarlo
                if G.nodes[w].get("infected", False):
                    to_infect.add(v)
                    # Ya no hace falta seguir mirando más vecinos de v
                    break
    
    # Actualizamos el estado de infección de los nodos que se infectan en este paso
    for v in to_infect:
        G.nodes[v]["infected"] = True


# ---------------------------------------------------------
# 2. Función para dibujar el grafo con colores según infección
# ---------------------------------------------------------
def dibujar_infeccion(G, pos, titulo="Estado de la infección"):
    """
    Dibuja el grafo G coloreando los nodos según su estado de infección.
    - Rojo: infectado
    - Azul claro: no infectado
    """
    colores = [
        "red" if G.nodes[n].get("infected", False) else "lightblue"
        for n in G.nodes()
    ]
    
    plt.figure(figsize=(5, 5))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colores,
        node_size=600,
        font_size=8
    )
    plt.title(titulo)
    plt.axis("off")
    plt.show()


# ---------------------------------------------------------
# 3. Función auxiliar: contar cuántos nodos están infectados
# ---------------------------------------------------------
def contar_infectados(G):
    """
    Devuelve el número de nodos infectados en el grafo G.
    """
    return sum(1 for v in G.nodes() if G.nodes[v].get("infected", False))


# ---------------------------------------------------------
# 4. Ejemplo completo de uso
# ---------------------------------------------------------
if __name__ == "__main__":
    # --- Crear un grafo 
    n = 20 #nodos
    k = 4 #grado
    p = 0 #grafo tipo anillo
    
    G = nx.watts_strogatz_graph(n=n, k=k, p=p, seed=1)

    # --- Inicializar todos los nodos como NO infectados ---
    for v in G.nodes():
        G.nodes[v]["infected"] = False

    # --- Infectar manualmente algunos nodos iniciales ---
    G.nodes[0]["infected"] = True
    G.nodes[3]["infected"] = True

    # --- Calcular la posición de los nodos una vez (para que no cambie entre pasos) ---
    pos = nx.spring_layout(G, seed=1)

    # --- Listas para guardar la evolución del número de infectados ---
    pasos = [0]
    hist_infectados = [contar_infectados(G)]

    # --- Dibujar estado inicial ---
    dibujar_infeccion(G, pos, titulo="Paso 0 (estado inicial)")

    # --- Simular varios pasos de contagio ---
    num_pasos = 5
    for t in range(1, num_pasos + 1):
        propagate_simple(G)
        pasos.append(t)
        hist_infectados.append(contar_infectados(G))
        dibujar_infeccion(G, pos, titulo=f"Paso {t}")

    # --- Representar la evolución global de la infección ---
    plt.figure()
    plt.plot(pasos, hist_infectados, marker="o")
    plt.xlabel("Paso de tiempo")
    plt.ylabel("Número de nodos infectados")
    plt.title("Evolución de la infección en el tiempo")
    plt.grid(True)
    plt.show()