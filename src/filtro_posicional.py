"""Ejemplo 6: un filtro cuyo resultado depende de la POSICIÓN del píxel.

Hasta acá, cada transformación trataba a todos los píxeles por igual.
Este ejemplo -inspirado en el filtro halftone del notebook de la
materia- arma una grilla de puntos, posiblemente rotada, y dibuja en
cada posición un punto cuyo tamaño depende del brillo de la imagen en
ese lugar. Es la misma familia de idea que van a necesitar para el
dithering del filtro Game Boy del TP (un patrón que depende de
``x`` e ``y``), pero es un filtro distinto: no forma parte del TP.

No es la solución de ningún filtro del TP2.
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw

from src.imagen_io import guardar_array_como_imagen
from src.transformaciones import escala_de_grises_por_promedio


def calcular_coordenadas_de_grilla(
    alto: int, ancho: int, tamano_punto: int, angulo_grados: float
) -> list[tuple[int, int]]:
    """Calcula las posiciones de una grilla regular, rotada, sobre la imagen.

    Adaptado del ejemplo de filtro halftone visto en clase: en vez de una
    grilla alineada con los bordes de la imagen, la gira ``angulo_grados``
    grados alrededor del centro para lograr la trama diagonal clásica de
    la impresión offset.

    Args:
        alto: Alto de la imagen en píxeles.
        ancho: Ancho de la imagen en píxeles.
        tamano_punto: Separación entre puntos consecutivos de la grilla.
        angulo_grados: Ángulo de rotación de la grilla, en grados.

    Returns:
        Lista de posiciones ``(x, y)`` dentro de los límites de la imagen.
    """
    posiciones = []
    angulo_rad = math.radians(angulo_grados)
    centro_x, centro_y = ancho / 2, alto / 2

    diagonal = int(math.hypot(ancho, alto))
    cantidad_x = diagonal // tamano_punto + 3
    cantidad_y = diagonal // tamano_punto + 3

    offset_x = centro_x - (cantidad_x * tamano_punto) / 2
    offset_y = centro_y - (cantidad_y * tamano_punto) / 2

    for fila in range(cantidad_y):
        for columna in range(cantidad_x):
            gx = offset_x + columna * tamano_punto + tamano_punto / 2 - centro_x
            gy = offset_y + fila * tamano_punto + tamano_punto / 2 - centro_y

            rx = gx * math.cos(angulo_rad) - gy * math.sin(angulo_rad) + centro_x
            ry = gx * math.sin(angulo_rad) + gy * math.cos(angulo_rad) + centro_y

            x, y = int(round(rx)), int(round(ry))
            if 0 <= y < alto and 0 <= x < ancho:
                posiciones.append((x, y))

    return posiciones


def aplicar_trama_de_puntos(
    array_imagen: np.ndarray, tamano_punto: int = 12, angulo_grados: float = 45
) -> np.ndarray:
    """Dibuja un punto en cada posición de la grilla, con radio según el brillo.

    Los píxeles oscuros generan puntos grandes y los claros, puntos
    chicos (o ningún punto): es el principio de un filtro halftone.

    Args:
        array_imagen: Array RGB de la imagen de entrada.
        tamano_punto: Separación entre puntos de la grilla.
        angulo_grados: Ángulo de rotación de la grilla.

    Returns:
        Array RGB con la trama de puntos sobre fondo blanco.
    """
    gris = escala_de_grises_por_promedio(array_imagen)
    alto, ancho = gris.shape

    lienzo = Image.new("RGB", (ancho, alto), color="white")
    dibujo = ImageDraw.Draw(lienzo)

    radio_maximo = tamano_punto / 2
    for x, y in calcular_coordenadas_de_grilla(alto, ancho, tamano_punto, angulo_grados):
        brillo = gris[y, x] / 255.0          # 0 = negro, 1 = blanco
        radio = (1.0 - brillo) * radio_maximo  # más oscuro -> punto más grande
        if radio < 0.5:
            continue
        dibujo.ellipse(
            [(x - radio, y - radio), (x + radio, y + radio)],
            fill="black",
        )

    return np.array(lienzo)


def ejecutar_demo(array_imagen: np.ndarray, carpeta_salida: str) -> None:
    """Aplica la trama de puntos con dos ángulos distintos y guarda el resultado.

    Args:
        array_imagen: Array de la imagen de entrada (RGB).
        carpeta_salida: Carpeta donde guardar los resultados.
    """
    print("=" * 60)
    print("EJEMPLO 6 · Filtro dependiente de la posición (halftone)")
    print("=" * 60)

    for angulo in (0, 45):
        print(f"\ngenerando trama con ángulo={angulo}°...")
        resultado = aplicar_trama_de_puntos(array_imagen, tamano_punto=10, angulo_grados=angulo)
        guardar_array_como_imagen(
            resultado, os.path.join(carpeta_salida, f"09_halftone_{angulo}grados.png")
        )


if __name__ == "__main__":
    from src.imagen_io import abrir_como_array
    from src.rutas import elegir_imagen_interactivamente, carpeta_salida

    _ruta = elegir_imagen_interactivamente()
    _array = abrir_como_array(_ruta)
    ejecutar_demo(_array, carpeta_salida("filtro_posicional"))
