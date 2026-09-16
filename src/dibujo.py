"""Ejemplo 5: dibujar formas sobre una imagen con ``PIL.ImageDraw``.

NumPy no ofrece una forma cómoda de dibujar líneas o figuras; para eso
Pillow trae ``ImageDraw``, que dibuja directamente sobre un objeto
``Image`` (no sobre un array). Este ejemplo queda fuera del alcance del
TP, pero es una herramienta común de Pillow que vale la pena conocer.
"""

import os

import numpy as np
from PIL import Image, ImageDraw

from src.imagen_io import guardar_array_como_imagen


def dibujar_figuras_de_ejemplo(array_imagen: np.ndarray) -> np.ndarray:
    """Dibuja una cruz y un rectángulo sobre una copia de la imagen.

    Args:
        array_imagen: Array de la imagen de entrada (RGB).

    Returns:
        Array con las figuras dibujadas encima.
    """
    imagen = Image.fromarray(array_imagen)
    dibujo = ImageDraw.Draw(imagen)

    alto, ancho = array_imagen.shape[:2]
    margen = min(alto, ancho) // 6

    # Cruz en la esquina superior izquierda.
    dibujo.line([(margen, margen), (margen * 3, margen)], fill="red", width=5)
    dibujo.line([(margen, margen), (margen, margen * 3)], fill="blue", width=5)

    # Rectángulo centrado.
    centro_x, centro_y = ancho // 2, alto // 2
    dibujo.rectangle(
        [
            (centro_x - margen, centro_y - margen),
            (centro_x + margen, centro_y + margen),
        ],
        outline="yellow",
        width=4,
    )

    return np.array(imagen)


def ejecutar_demo(array_imagen: np.ndarray, carpeta_salida: str) -> None:
    """Dibuja las figuras de ejemplo y guarda el resultado.

    Args:
        array_imagen: Array de la imagen de entrada (RGB).
        carpeta_salida: Carpeta donde guardar el resultado.
    """
    print("=" * 60)
    print("EJEMPLO 5 · Dibujar con ImageDraw")
    print("=" * 60)

    resultado = dibujar_figuras_de_ejemplo(array_imagen)
    guardar_array_como_imagen(resultado, os.path.join(carpeta_salida, "08_con_dibujos.png"))


if __name__ == "__main__":
    from src.imagen_io import abrir_como_array
    from src.rutas import elegir_imagen_interactivamente, carpeta_salida

    _ruta = elegir_imagen_interactivamente()
    _array = abrir_como_array(_ruta)
    ejecutar_demo(_array, carpeta_salida("dibujo"))
