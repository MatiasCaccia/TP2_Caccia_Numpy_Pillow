"""Ejemplo 1: lo mínimo de NumPy para entender una imagen como matriz.

No trabaja con imágenes todavía: crea arrays chiquitos e imprime su
forma (``shape``), su tipo de dato (``dtype``) y el resultado de
operarlos, para fijar el vocabulario antes de aplicarlo a píxeles.
"""

import numpy as np


def crear_arrays_de_ejemplo() -> tuple[np.ndarray, np.ndarray]:
    """Crea un array 1D y uno 2D de ejemplo.

    Returns:
        Una tupla ``(vector, tabla)`` con un array de una dimensión y
        otro de dos dimensiones.
    """
    vector = np.array([1, 2, 3])
    tabla = np.array([[1, 2, 3], [4, 5, 6]])
    return vector, tabla


def describir_array(array: np.ndarray, nombre: str = "array") -> None:
    """Imprime shape, dtype y contenido de un array, con formato prolijo.

    Args:
        array: Array a describir.
        nombre: Nombre a mostrar en la salida, para identificarlo.
    """
    print(f"\n{nombre}:")
    print(array)
    print(f"  shape = {array.shape}   dtype = {array.dtype}")


def operar_sobre_array_completo(vector: np.ndarray) -> np.ndarray:
    """Multiplica cada elemento del array por 2, sin usar ningún ``for``.

    Esta es la idea de "vectorización": la operación se aplica a todos
    los elementos a la vez. En una imagen, la misma idea sirve para
    invertir colores o promediar canales sin recorrer píxel por píxel.

    Args:
        vector: Array de entrada.

    Returns:
        Un nuevo array con cada elemento multiplicado por 2.
    """
    return vector * 2


def crear_arrays_especiales() -> dict[str, np.ndarray]:
    """Crea algunos arrays "especiales" muy usados al trabajar con imágenes.

    Returns:
        Diccionario con:
            - ``"ceros"``: array de 2x3 lleno de ceros.
            - ``"unos"``: array de 3x2 lleno de unos.
            - ``"aleatorio_uint8"``: array de 5x5 con enteros al azar
              entre 0 y 255, del mismo tipo de dato que usa una imagen.
    """
    return {
        "ceros": np.zeros((2, 3)),
        "unos": np.ones((3, 2)),
        "aleatorio_uint8": np.random.randint(0, 256, size=(5, 5), dtype=np.uint8),
    }


def indexar_ejemplos(tabla: np.ndarray) -> None:
    """Muestra distintas formas de indexar un array 2D.

    Args:
        tabla: Array de dos dimensiones a indexar.
    """
    print("\nIndexado de la tabla:")
    print(f"  tabla[0, 0]  (primer elemento)      -> {tabla[0, 0]}")
    print(f"  tabla[:, 0]  (primera columna)       -> {tabla[:, 0]}")
    print(f"  tabla[1, :]  (segunda fila)          -> {tabla[1, :]}")
    print(f"  tabla[:, 1:] (todas menos 1a columna)-> {tabla[:, 1:].tolist()}")


def ejecutar_demo() -> None:
    """Corre, en orden, todos los ejemplos de este módulo e imprime resultados."""
    print("=" * 60)
    print("EJEMPLO 1 · NumPy básico")
    print("=" * 60)

    vector, tabla = crear_arrays_de_ejemplo()
    describir_array(vector, "vector (1D)")
    describir_array(tabla, "tabla (2D)")

    duplicado = operar_sobre_array_completo(vector)
    describir_array(duplicado, "vector * 2 (vectorizado)")

    for nombre, array in crear_arrays_especiales().items():
        describir_array(array, nombre)

    indexar_ejemplos(tabla)


if __name__ == "__main__":
    ejecutar_demo()
