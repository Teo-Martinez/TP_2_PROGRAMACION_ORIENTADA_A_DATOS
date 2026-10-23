"""Ejecutar el flujo completo con python -m src.main desde la raíz."""

import argparse
import hashlib
from pathlib import Path
import sys

from src.consultas import (
    comparar_etiquetas,
    listar_categorias,
    ordenar_productos,
    seleccionar_productos,
)
from src.diagnostico import resumir_validos
from src.fuentes import FuenteCSV, FuenteJSON
from src.preparacion import diagnosticar, preparar_productos
from src.productos import UNIDADES
from src.salidas import (
    guardar_resultados,
    mostrar_comparacion,
    mostrar_rechazos,
)


def crear_parser():
    """Definir las operaciones disponibles sin requerir modificar el código."""
    parser = argparse.ArgumentParser(description="Comparador por 100 gramos")
    parser.add_argument("--archivo", default="data/productos.csv")
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--codigos", nargs="+")
    grupo.add_argument("--categoria")
    grupo.add_argument("--listar-categorias", action="store_true")
    parser.add_argument("--ordenar", choices=list(UNIDADES))
    parser.add_argument("--descendente", action="store_true")
    parser.add_argument("--salida", default="outputs")
    return parser


def ejecutar(args):
    """Validar consulta antes de escribir; separar lectura y análisis."""
    if args.descendente and not args.ordenar:
        raise ValueError("--descendente necesita --ordenar.")
    if args.listar_categorias and args.ordenar:
        raise ValueError("El listado de categorías no ordena nutrientes.")
    ruta = Path(args.archivo)
    fuentes = {".csv": FuenteCSV(), ".json": FuenteJSON()}
    if ruta.suffix.casefold() not in fuentes:
        raise ValueError("La entrada debe ser un archivo CSV o JSON.")
    carpeta = Path(args.salida)
    for nombre in ["comparacion.csv", "rechazos.csv", "cambios.csv",
                   "diagnostico.json"]:
        if (carpeta / nombre).resolve() == ruta.resolve():
            raise ValueError("Una salida no puede reemplazar la entrada.")
    registros = fuentes[ruta.suffix.casefold()].cargar(ruta)
    diagnostico = diagnosticar(registros)
    productos, rechazos, cambios = preparar_productos(registros)
    if args.listar_categorias:
        mostrar_rechazos(rechazos, len(registros))
        for categoria, cantidad in listar_categorias(productos).items():
            print(f"{categoria}: {cantidad}")
        if not productos:
            raise ValueError("No hay fichas válidas para listar categorías.")
        return 0
    seleccion = seleccionar_productos(productos, args.codigos, args.categoria)
    if args.ordenar:
        seleccion = ordenar_productos(
            seleccion, args.ordenar, args.descendente
        )
    tabla = comparar_etiquetas(seleccion)
    if len(productos) + len(rechazos) != len(registros):
        raise ValueError("Los conteos de limpieza no coinciden.")
    diagnostico.update({
        "resumen_validos": resumir_validos(productos),
        "archivo": str(ruta),
        "sha256": hashlib.sha256(ruta.read_bytes()).hexdigest(),
        "validos": len(productos), "rechazados": len(rechazos),
        "seleccionados": len(seleccion), "campos_modificados": len(cambios),
        "registros_modificados": len({c["registro"] for c in cambios}),
        "regla_duplicados": "Conservar el primer registro válido por código",
    })
    guardar_resultados(carpeta, tabla, rechazos, cambios, diagnostico)
    print(f"Entrada: {len(registros)}; válidos: {len(productos)}; "
          f"rechazados: {len(rechazos)}; seleccionados: {len(tabla)}")
    mostrar_comparacion(tabla)
    print(f"Salidas guardadas en {carpeta}")
    if not productos:
        print("No hay fichas válidas; revisá rechazos.csv.", file=sys.stderr)
        return 1
    return 0


def main():
    """Comunicar errores y devolver un código de salida no nulo."""
    args = crear_parser().parse_args()
    try:
        return ejecutar(args)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
