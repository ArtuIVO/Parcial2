class Nodo:
    def __init__(self, pregunta, izquierda=None, derecha=None):
        self.pregunta = pregunta
        self.izquierda = izquierda
        self.derecha = derecha

    def __str__(self):
        """Devuelve una representación en cadena del nodo y sus subárboles."""
        return self._str_recursive(self)

    def _str_recursive(self, nodo, depth=0):
        """Recorrido recursivo para generar la representación en cadena del árbol."""
        if nodo is None:
            return ""

        # Espacios para la indentación según la profundidad
        indent = "  " * depth

        # Representación del nodo actual
        representation = f"{indent}- {nodo.pregunta}\n"

        # Representación de los subárboles izquierdo y derecho recursivamente
        if nodo.izquierda:
            representation += self._str_recursive(nodo.izquierda, depth + 1)
        if nodo.derecha:
            representation += self._str_recursive(nodo.derecha, depth + 1)

        return representation


def reconstruir_arbol(preorder, inorder):
    """Reconstruye un árbol binario a partir de los recorridos preorder e inorder."""
    if not preorder or not inorder:
        return None

    raiz_val = preorder[0]
    raiz = Nodo(raiz_val)

    # Encontrar índice de la raíz en el recorrido inorder
    raiz_index = inorder.index(raiz_val)

    # Recursivamente construir subárboles izquierdo y derecho
    raiz.izquierda = reconstruir_arbol(preorder[1:raiz_index + 1], inorder[:raiz_index])
    raiz.derecha = reconstruir_arbol(preorder[raiz_index + 1:], inorder[raiz_index + 1:])

    return raiz


def cargar_arbol_desde_txt(archivo):
    """Carga un árbol binario desde un archivo de texto con recorridos preorder e inorder."""
    with open(archivo, 'r') as f:
        lineas = f.readlines()

    # Encontrar los índices donde comienzan los recorridos en el archivo
    pre_idx = lineas.index("Recorrido Preorder:\n") + 1
    in_idx = lineas.index("Recorrido Inorder:\n") + 1

    # Obtener listas de recorridos desde el archivo
    preorder = [line.strip() for line in lineas[pre_idx:in_idx - 1]]
    inorder = [line.strip() for line in lineas[in_idx:-1]]

    # Reconstruir el árbol a partir de los recorridos preorder e inorder
    arbol = reconstruir_arbol(preorder, inorder)

    return arbol


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

    while True:
        if respuesta == "y":
            if nodo.izquierda:
                # Si hay una rama izquierda, continuar con la siguiente pregunta
                jugar_adivinanzas(nodo.izquierda)
            else:
                print("¡Adiviné correctamente!")  # Adivinó correctamente
                break
        elif respuesta == "n":
            if nodo.derecha:
                # Mostrar la siguiente pregunta en la rama derecha
                respuesta = input(nodo.derecha.pregunta + " (y/n): ").lower()
            else:
                # No se adivinó y se necesita agregar una nueva pregunta
                objeto = input("No sé qué es. ¿Qué es el objeto/animal/personaje que estabas pensando? ").lower()
                nueva_pregunta = input(f"Escribe una pregunta que distinga {objeto} de {nodo.pregunta}. ")
                respuesta_nueva_pregunta = input(f"¿Cuál sería la respuesta a tu pregunta '{nueva_pregunta}'? (y/n) ").lower()

                # Crear el nuevo nodo con la nueva pregunta y objeto
                nuevo_nodo = Nodo(nueva_pregunta)
                nuevo_nodo.izquierda = Nodo(objeto)  # El nuevo objeto se convierte en la rama izquierda
                nuevo_nodo.derecha = None

                # Mostrar la nueva pregunta antes de solicitar la respuesta
                respuesta = input(nueva_pregunta + " (y/n): ").lower()

                if respuesta == respuesta_nueva_pregunta:
                    print("¡Adiviné correctamente!")  # Adivinó correctamente
                else:
                    print("No adiviné correctamente. ¡Voy a aprender más!")
                    nodo.derecha = nuevo_nodo  # Conectar el nuevo nodo como siguiente pregunta
                    break


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
print("Exportando árbol a txt")
exportar_arbol(arbol, "arbol.txt")

# Opcional: Cargar un árbol binario desde un archivo de texto
a = input("¿Desea cargar un archivo para convertirlo en un árbol binario? (y/n) ").lower()

while a == "y":
    b = input("Ingrese el nombre de su archivo: ")
    arbol_cargado = cargar_arbol_desde_txt(b)

    if arbol_cargado is None:
        print("No se encontró el archivo.")
    else:
        # Jugar con el árbol cargado
        print("\nÁrbol cargado desde el archivo:")
        jugar_adivinanzas(arbol_cargado)
        break
