"""Ejemplo 3: separar una imagen en sus canales Rojo, Verde y Azul.

Muestra cómo indexar la tercera dimensión de un array de imagen
(``array[:, :, canal]``) y cómo reconstruir una imagen de 3 canales con
``np.stack`` para poder visualizar cada canal con su color real.
"""

import os

import numpy as np

from src.imagen_io import guardar_array_como_imagen


def extraer_canales(array_imagen: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Separa una imagen RGB en sus tres canales.

    Args:
        array_imagen: Array de forma ``(alto, ancho, 3)``.

    Returns:
        Tupla ``(rojo, verde, azul)``, cada uno una matriz 2D de forma
        ``(alto, ancho)``.
    """
    canal_rojo = array_imagen[:, :, 0]
    canal_verde = array_imagen[:, :, 1]
    canal_azul = array_imagen[:, :, 2]
    return canal_rojo, canal_verde, canal_azul


def colorear_canal(canal: np.ndarray, posicion: int) -> np.ndarray:
    """Reconstruye una imagen de 3 canales mostrando solo uno con su color real.

    Por ejemplo, para el canal rojo arma una imagen donde el canal 0 es
    el canal original y los canales 1 y 2 quedan en cero, así se ve en
    tonos de rojo en vez de en gris.

    Args:
        canal: Matriz 2D con los valores de un único canal.
        posicion: Índice del canal dentro de RGB (0=rojo, 1=verde, 2=azul).

    Returns:
        Array de forma ``(alto, ancho, 3)`` y ``dtype=uint8``.
    """
    ceros = np.zeros_like(canal)
    canales = [ceros, ceros, ceros]
    canales[posicion] = canal
    return np.stack(canales, axis=2).astype(np.uint8)


def ejecutar_demo(array_imagen: np.ndarray, carpeta_salida: str) -> None:
    """Separa la imagen en canales, los colorea y guarda las 3 versiones.

    Args:
        array_imagen: Array de la imagen de entrada (RGB).
        carpeta_salida: Carpeta donde guardar los resultados.
    """
    print("=" * 60)
    print("EJEMPLO 3 · Canales RGB")
    print("=" * 60)

    canal_rojo, canal_verde, canal_azul = extraer_canales(array_imagen)
    nombres_y_canales = (
        ("rojo", canal_rojo, 0),
        ("verde", canal_verde, 1),
        ("azul", canal_azul, 2),
    )

    for nombre, canal, posicion in nombres_y_canales:
        print(f"\ncanal {nombre}: shape={canal.shape}  "
              f"promedio={canal.mean():.1f}")
        imagen_coloreada = colorear_canal(canal, posicion)
        guardar_array_como_imagen(
            imagen_coloreada,
            os.path.join(carpeta_salida, f"02_canal_{nombre}.png"),
        )


if __name__ == "__main__":
    from src.imagen_io import abrir_como_array
    from src.rutas import elegir_imagen_interactivamente, carpeta_salida

    _ruta = elegir_imagen_interactivamente()
    _array = abrir_como_array(_ruta)
    ejecutar_demo(_array, carpeta_salida("canales_rgb"))
