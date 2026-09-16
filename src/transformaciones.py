"""Ejemplo 4: manipulaciones básicas de una imagen con NumPy.

Cubre las cuatro operaciones del notebook de la materia: escala de
grises "a mano" (promedio de canales), inversión de colores, volteos
(horizontal/vertical) y recorte central. Son ejercicios generales de
indexado y aritmética de arrays: ninguno resuelve, por sí solo, un
filtro del TP.
"""

import os

import numpy as np

from src.imagen_io import guardar_array_como_imagen


def escala_de_grises_por_promedio(array_imagen: np.ndarray) -> np.ndarray:
    """Convierte una imagen a escala de grises promediando sus 3 canales.

    Args:
        array_imagen: Array RGB de forma ``(alto, ancho, 3)``.

    Returns:
        Matriz 2D de forma ``(alto, ancho)`` con ``dtype=uint8``.
    """
    # axis=2 promedia "a través" de los canales, dejando un valor por píxel.
    promedio = np.mean(array_imagen, axis=2)
    return promedio.astype(np.uint8)


def invertir_colores(array_imagen: np.ndarray) -> np.ndarray:
    """Invierte los colores de una imagen (negativo fotográfico).

    Args:
        array_imagen: Array de la imagen de entrada.

    Returns:
        Array con cada valor reemplazado por ``255 - valor``.
    """
    return 255 - array_imagen


def voltear_verticalmente(array_imagen: np.ndarray) -> np.ndarray:
    """Voltea la imagen de arriba hacia abajo (invierte el orden de filas).

    Args:
        array_imagen: Array de la imagen de entrada.

    Returns:
        Array volteado verticalmente.
    """
    return np.flipud(array_imagen)


def voltear_horizontalmente(array_imagen: np.ndarray) -> np.ndarray:
    """Voltea la imagen de izquierda a derecha (invierte el orden de columnas).

    Args:
        array_imagen: Array de la imagen de entrada.

    Returns:
        Array volteado horizontalmente.
    """
    return np.fliplr(array_imagen)


def recortar_porcion_central(array_imagen: np.ndarray, porcentaje: float = 0.5) -> np.ndarray:
    """Recorta la porción central de la imagen.

    Args:
        array_imagen: Array de la imagen de entrada.
        porcentaje: Fracción del ancho/alto a conservar, centrada.
            Por ejemplo, ``0.5`` conserva el 50% central en cada eje.

    Returns:
        Array recortado.

    Raises:
        ValueError: Si ``porcentaje`` no está en el rango ``(0, 1]``.
    """
    if not 0 < porcentaje <= 1:
        raise ValueError("porcentaje debe estar entre 0 (exclusivo) y 1.")

    alto, ancho = array_imagen.shape[:2]
    margen_alto = int(alto * (1 - porcentaje) / 2)
    margen_ancho = int(ancho * (1 - porcentaje) / 2)

    return array_imagen[
        margen_alto: alto - margen_alto,
        margen_ancho: ancho - margen_ancho,
    ]


def ejecutar_demo(array_imagen: np.ndarray, carpeta_salida: str) -> None:
    """Aplica las cuatro transformaciones y guarda cada resultado.

    Args:
        array_imagen: Array de la imagen de entrada (RGB).
        carpeta_salida: Carpeta donde guardar los resultados.
    """
    print("=" * 60)
    print("EJEMPLO 4 · Transformaciones básicas")
    print("=" * 60)

    transformaciones = {
        "03_escala_de_grises.png": escala_de_grises_por_promedio(array_imagen),
        "04_invertida.png": invertir_colores(array_imagen),
        "05_volteada_vertical.png": voltear_verticalmente(array_imagen),
        "06_volteada_horizontal.png": voltear_horizontalmente(array_imagen),
        "07_recorte_central.png": recortar_porcion_central(array_imagen, 0.5),
    }

    for nombre_archivo, resultado in transformaciones.items():
        print(f"\n{nombre_archivo}: shape={resultado.shape}")
        guardar_array_como_imagen(resultado, os.path.join(carpeta_salida, nombre_archivo))


if __name__ == "__main__":
    from src.imagen_io import abrir_como_array
    from src.rutas import elegir_imagen_interactivamente, carpeta_salida

    _ruta = elegir_imagen_interactivamente()
    _array = abrir_como_array(_ruta)
    ejecutar_demo(_array, carpeta_salida("transformaciones"))
