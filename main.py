class Nodo:
    def __init__(self, pregunta, izquierda=None, derecha=None):
        self.pregunta = pregunta
        self.izquierda = izquierda
        self.derecha = derecha


def preorder(nodo):
    """Retorna una cadena con el recorrido preorder del árbol."""
    if nodo is None:
        return ""
    result = str(nodo.pregunta) + "\n"
    result += preorder(nodo.izquierda)
    result += preorder(nodo.derecha)
    return result


def inorder(nodo):
    """Retorna una cadena con el recorrido inorder del árbol."""
    if nodo is None:
        return ""
    result = inorder(nodo.izquierda)
    result += str(nodo.pregunta) + "\n"
    result += inorder(nodo.derecha)
    return result


def postorder(nodo):
    """Retorna una cadena con el recorrido postorder del árbol."""
    if nodo is None:
        return ""
    result = postorder(nodo.izquierda)
    result += postorder(nodo.derecha)
    result += str(nodo.pregunta) + "\n"
    return result


def exportar_arbol(nodo, archivo):
    """Exporta el árbol a un archivo externo."""
    with open(archivo, 'w') as f:
        f.write("Recorrido Preorder:\n")
        f.write(preorder(nodo))
        f.write("\nRecorrido Inorder:\n")
        f.write(inorder(nodo))
        f.write("\nRecorrido Postorder:\n")
        f.write(postorder(nodo))


def jugar_adivinanzas(nodo):
    """Función para jugar al juego de adivinanzas recursivamente."""
    respuesta = input(nodo.pregunta + " (y/n): ").lower()

    if respuesta == "y":
        if nodo.izquierda:
            jugar_adivinanzas(nodo.izquierda)
        else:
            print("¡Adiviné correctamente!")
    elif respuesta == "n":
        if nodo.derecha:
            jugar_adivinanzas(nodo.derecha)
        else:
            # Si no se sabe la respuesta, se solicita al jugador la nueva pregunta y respuesta.
            objeto = input("No sé qué es. ¿Qué es el objeto/animal/personaje que estabas pensando? ")
            nueva_pregunta = input("Escribe una pregunta que distinga {} de {}. ".format(objeto, nodo.pregunta))
            respuesta_nueva_pregunta = input("¿Cuál sería la respuesta a tu pregunta? (y/n) ")

            # Se actualiza el árbol con la nueva información.
            nodo.derecha = Nodo(nodo.pregunta)
            nodo.izquierda = Nodo(objeto)
            nodo.pregunta = nueva_pregunta

            if respuesta_nueva_pregunta == "y":
                nodo.izquierda, nodo.derecha = nodo.derecha, nodo.izquierda
    else:
        print("Respuesta erronea, vuelva a intentarlo")


# Inicio del juego
arbol = Nodo("¿Es un animal?")
jugar_adivinanzas(arbol)

# Preguntar al jugador si desea jugar de nuevo
jugar_de_nuevo = input("¿Quieres jugar de nuevo? (y/n) ").lower()

while jugar_de_nuevo == "y":
    # Reiniciar el juego con una nueva pregunta inicial
    arbol = Nodo("¿Es un animal?")
    jugar_adivinanzas(arbol)
    jugar_de_nuevo = input("¿Quieres jugar de nuevo? (y/n) ").lower()

print("¡Gracias por jugar!")
print("Exportando arbol a txt")
exportar_arbol(arbol, "arbol.txt")
