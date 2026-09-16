#!/usr/bin/env python3
"""Punto de entrada de los ejemplos de la clase de NumPy y Pillow.

Ejecutar desde la raíz del proyecto:

    python3 main.py

El programa lista las imágenes de ``materiales/``, pide elegir una, y
corre todos los ejemplos de ``src/`` sobre ella, guardando cada
resultado dentro de ``outputs/<nombre_del_ejemplo>/``.

Estos ejemplos son material de apoyo para entender NumPy y Pillow: no
resuelven el TP2 ("Museo de Pantallas"). Los filtros Game Boy y CRT,
y la inserción en la pantalla del aparato, quedan para que cada grupo
los implemente.
"""

import os

from src import canales_rgb, dibujo, filtro_posicional, imagen_io, numpy_basico, transformaciones
from src.rutas import (
    DIRECTORIO_SALIDAS,
    asegurar_carpeta_salida,
    carpeta_salida,
    elegir_imagen_interactivamente,
)


def ejecutar_todos_los_ejemplos(ruta_imagen: str) -> None:
    """Corre, en orden, los seis ejemplos del paquete ``src`` sobre una imagen.

    Args:
        ruta_imagen: Ruta a la imagen elegida por el usuario.
    """
    asegurar_carpeta_salida(DIRECTORIO_SALIDAS)

    numpy_basico.ejecutar_demo()

    array_imagen = imagen_io.ejecutar_demo(ruta_imagen, carpeta_salida("imagen_io"))
    canales_rgb.ejecutar_demo(array_imagen, carpeta_salida("canales_rgb"))
    transformaciones.ejecutar_demo(array_imagen, carpeta_salida("transformaciones"))
    dibujo.ejecutar_demo(array_imagen, carpeta_salida("dibujo"))
    filtro_posicional.ejecutar_demo(array_imagen, carpeta_salida("filtro_posicional"))

    print("\n" + "=" * 60)
    print(f"Listo. Todos los resultados quedaron en: {DIRECTORIO_SALIDAS}")
    print("=" * 60)


def main() -> None:
    """Orquesta la ejecución interactiva de todos los ejemplos."""

    print("Clase NumPy + Pillow — TP2 Museo de Pantallas")
    print(f"Directorio de trabajo: {os.getcwd()}")

    ruta_imagen = elegir_imagen_interactivamente()
    print(f"\nUsando imagen: {ruta_imagen}")

    ejecutar_todos_los_ejemplos(ruta_imagen)


if __name__ == "__main__":
    main()
