"""Utilidades de sistema de archivos, basadas en el módulo estándar ``os``.

Todo lo que en la clase se hace "a mano" con rutas (encontrar la carpeta
del proyecto, listar imágenes disponibles, crear la carpeta de salida)
vive acá, separado del código de procesamiento de imágenes.
"""

import os

# os.path.dirname(__file__) es la carpeta "src/"; subimos un nivel con
# os.path.dirname otra vez para llegar a la raíz del proyecto. Así los
# scripts funcionan sin importar desde qué directorio se los ejecute.
DIRECTORIO_SRC = os.path.dirname(os.path.abspath(__file__))
DIRECTORIO_PROYECTO = os.path.dirname(DIRECTORIO_SRC)

DIRECTORIO_MATERIALES = os.path.join(DIRECTORIO_PROYECTO, "materiales")
DIRECTORIO_SALIDAS = os.path.join(DIRECTORIO_PROYECTO, "outputs")

EXTENSIONES_IMAGEN = (".png", ".jpg", ".jpeg", ".bmp", ".gif")


def listar_imagenes_disponibles(carpeta: str = DIRECTORIO_MATERIALES) -> list[str]:
    """Devuelve los nombres de archivo de imagen dentro de ``carpeta``.

    Args:
        carpeta: Carpeta a inspeccionar. Por defecto, ``materiales/``.

    Returns:
        Lista de nombres de archivo (sin la ruta completa) ordenada
        alfabéticamente, filtrando solo extensiones de imagen conocidas.

    Raises:
        FileNotFoundError: Si ``carpeta`` no existe.
    """
    if not os.path.isdir(carpeta):
        raise FileNotFoundError(f"No existe la carpeta '{carpeta}'.")

    nombres = os.listdir(carpeta)
    imagenes = [
        nombre
        for nombre in nombres
        if nombre.lower().endswith(EXTENSIONES_IMAGEN)
        and os.path.isfile(os.path.join(carpeta, nombre))
    ]
    return sorted(imagenes)


def asegurar_carpeta_salida(carpeta: str = DIRECTORIO_SALIDAS) -> str:
    """Crea ``carpeta`` (y sus padres) si todavía no existe.

    ``os.makedirs`` con ``exist_ok=True`` evita tener que chequear a mano
    si la carpeta ya estaba creada de una ejecución anterior.

    Args:
        carpeta: Carpeta a crear. Por defecto, ``outputs/``.

    Returns:
        La misma ruta recibida, ya garantizada como existente.
    """
    os.makedirs(carpeta, exist_ok=True)
    return carpeta


def carpeta_salida(subcarpeta: str | None = None) -> str:
    """Devuelve (y crea si hace falta) una subcarpeta dentro de ``outputs/``.

    Args:
        subcarpeta: Subcarpeta dentro de ``outputs/`` para agrupar los
            resultados de un mismo ejemplo (p. ej. ``"canales_rgb"``).
            Si es ``None``, devuelve ``outputs/`` directamente.

    Returns:
        Ruta absoluta a la carpeta, ya creada.
    """
    carpeta = DIRECTORIO_SALIDAS if subcarpeta is None else os.path.join(
        DIRECTORIO_SALIDAS, subcarpeta
    )
    return asegurar_carpeta_salida(carpeta)


def ruta_salida(nombre_archivo: str, subcarpeta: str | None = None) -> str:
    """Arma una ruta de archivo dentro de ``outputs/`` y crea las carpetas necesarias.

    Args:
        nombre_archivo: Nombre del archivo a generar, p. ej. ``"gris.png"``.
        subcarpeta: Subcarpeta opcional dentro de ``outputs/`` (ver
            :func:`carpeta_salida`).

    Returns:
        Ruta absoluta y lista para usar en ``imagen.save(...)``.
    """
    return os.path.join(carpeta_salida(subcarpeta), nombre_archivo)


def validar_imagen_existe(ruta: str) -> None:
    """Valida que ``ruta`` exista y sea un archivo.

    Args:
        ruta: Ruta a validar.

    Raises:
        FileNotFoundError: Si la ruta no existe o no es un archivo.
    """
    if not os.path.isfile(ruta):
        raise FileNotFoundError(f"No se encontró la imagen '{ruta}'.")


def elegir_imagen_interactivamente(carpeta: str = DIRECTORIO_MATERIALES) -> str:
    """Le muestra al usuario las imágenes de ``carpeta`` y le pide elegir una.

    Pensado para usarse desde ``main.py`` al ejecutar la clase de forma
    interactiva por consola.

    Args:
        carpeta: Carpeta donde buscar imágenes.

    Returns:
        Ruta completa a la imagen elegida.
    """
    imagenes = listar_imagenes_disponibles(carpeta)
    if not imagenes:
        raise FileNotFoundError(f"No hay imágenes en '{carpeta}'.")

    print(f"\nImágenes disponibles en '{os.path.basename(carpeta)}/':")
    for indice, nombre in enumerate(imagenes, start=1):
        print(f"  {indice}. {nombre}")

    while True:
        eleccion = input(f"Elegí una imagen (1-{len(imagenes)}): ").strip()
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(imagenes):
            nombre_elegido = imagenes[int(eleccion) - 1]
            return os.path.join(carpeta, nombre_elegido)
        print("Opción inválida, probá de nuevo.")
