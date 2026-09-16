"""Ejemplo 2: el flujo Pillow abre -> NumPy transforma -> Pillow guarda.

Este módulo no aplica ninguna transformación todavía: solo muestra cómo
pasar de un archivo en disco a un array de NumPy editable, y de vuelta
a un archivo en disco.
"""

import os

import numpy as np
from PIL import Image

from src.rutas import validar_imagen_existe


def abrir_como_array(ruta_imagen: str) -> np.ndarray:
    """Abre una imagen con Pillow y la convierte en array de NumPy.

    Args:
        ruta_imagen: Ruta al archivo de imagen.

    Returns:
        Array de forma ``(alto, ancho, canales)`` (o ``(alto, ancho)``
        si la imagen ya está en escala de grises), con ``dtype=uint8``.

    Raises:
        FileNotFoundError: Si ``ruta_imagen`` no existe.
    """
    validar_imagen_existe(ruta_imagen)
    with Image.open(ruta_imagen) as imagen:
        # .convert("RGB") normaliza imágenes con transparencia (RGBA) o en
        # paleta (P) para que siempre trabajemos con 3 canales conocidos.
        imagen_rgb = imagen.convert("RGB")
        return np.array(imagen_rgb)


def describir_imagen(array_imagen: np.ndarray, nombre: str = "imagen") -> None:
    """Imprime alto, ancho, cantidad de canales y tipo de dato de una imagen.

    Args:
        array_imagen: Array de la imagen a describir.
        nombre: Nombre a mostrar en la salida.
    """
    alto, ancho = array_imagen.shape[:2]
    canales = array_imagen.shape[2] if array_imagen.ndim == 3 else 1
    print(f"\n{nombre}:")
    print(f"  alto={alto}px  ancho={ancho}px  canales={canales}")
    print(f"  dtype={array_imagen.dtype}  valor mínimo={array_imagen.min()}  "
          f"valor máximo={array_imagen.max()}")


def guardar_array_como_imagen(array_imagen: np.ndarray, ruta_salida: str) -> None:
    """Convierte un array de NumPy en imagen y la guarda en disco.

    Args:
        array_imagen: Array a guardar. Si no es ``uint8``, se lo convierte
            automáticamente (recortando al rango 0-255) antes de guardar.
        ruta_salida: Ruta completa del archivo a crear, incluida la
            extensión (p. ej. ``".../outputs/resultado.png"``).
    """
    if array_imagen.dtype != np.uint8:
        array_imagen = np.clip(array_imagen, 0, 255).astype(np.uint8)

    Image.fromarray(array_imagen).save(ruta_salida)
    print(f"  guardado -> {ruta_salida}")


def ejecutar_demo(ruta_imagen: str, carpeta_salida: str) -> np.ndarray:
    """Abre una imagen, describe su array y la vuelve a guardar sin cambios.

    Args:
        ruta_imagen: Ruta a la imagen de entrada.
        carpeta_salida: Carpeta donde guardar la copia de verificación.

    Returns:
        El array de la imagen abierta, para reutilizarlo en otros ejemplos.
    """
    print("=" * 60)
    print("EJEMPLO 2 · Abrir, describir y guardar con Pillow + NumPy")
    print("=" * 60)

    array_imagen = abrir_como_array(ruta_imagen)
    describir_imagen(array_imagen, "imagen abierta")

    guardar_array_como_imagen(
        array_imagen, os.path.join(carpeta_salida, "01_copia_sin_cambios.png")
    )
    return array_imagen


if __name__ == "__main__":
    from src.rutas import elegir_imagen_interactivamente, carpeta_salida

    _ruta = elegir_imagen_interactivamente()
    ejecutar_demo(_ruta, carpeta_salida("imagen_io"))
