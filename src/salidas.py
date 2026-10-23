"""Comunicar comparaciones y conservar trazabilidad en archivos locales."""

import csv
import json
from pathlib import Path
import sys

from src.productos import UNIDADES

COLUMNAS = ["codigo", "nombre"] + [
    f"{nombre}_{unidad}_100g" for nombre, unidad in UNIDADES.items()
]


def escribir_csv(ruta, registros, campos):
    """Escribir encabezado incluso sin filas y distinguir ausencias de cero."""
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for registro in registros:
            escritor.writerow({
                campo: "No disponible" if valor is None else valor
                for campo, valor in registro.items()
            })


def guardar_resultados(carpeta, tabla, rechazos, cambios, diagnostico):
    """Reemplazar salidas para evitar acumular registros entre ejecuciones."""
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    escribir_csv(carpeta / "comparacion.csv", tabla, COLUMNAS)
    escribir_csv(carpeta / "rechazos.csv", rechazos,
                 ["registro", "codigo", "motivo"])
    escribir_csv(carpeta / "cambios.csv", cambios,
                 ["registro", "codigo", "campo", "original", "normalizado",
                  "motivo"])
    (carpeta / "diagnostico.json").write_text(
        json.dumps(diagnostico, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def mostrar_comparacion(tabla):
    """Mostrar dos decimales sin redondear los datos guardados."""
    if not tabla:
        print("La consulta no tiene productos para comparar.")
        return
    print("Nutrientes por 100 g: energía en kcal, sodio en mg y resto en g.")
    print(" | ".join(COLUMNAS))
    for fila in tabla:
        valores = []
        for campo in COLUMNAS:
            valor = fila[campo]
            if valor is None:
                valores.append("No disponible")
            elif isinstance(valor, float):
                valores.append(f"{valor:.2f}")
            else:
                valores.append(str(valor))
        print(" | ".join(valores))


def mostrar_rechazos(rechazos, total):
    """Informar descartes del listado sin generar ni reemplazar archivos."""
    if not rechazos:
        return
    print(f"Advertencia: registros rechazados: {len(rechazos)} de {total}.",
          file=sys.stderr)
    print("Las categorías incluyen solo fichas válidas.", file=sys.stderr)
    for rechazo in rechazos:
        numero = rechazo["registro"]
        codigo = rechazo["codigo"]
        motivo = rechazo["motivo"]
        print(f"Registro {numero} | código: {codigo} | motivo: {motivo}",
              file=sys.stderr)
