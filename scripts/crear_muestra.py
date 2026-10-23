"""Construir dos archivos equivalentes de productos completamente ficticios."""

import csv
import json
from pathlib import Path

DESTINO = Path(__file__).resolve().parents[1] / "data"
NOMBRES = ("energia", "proteinas", "carbohidratos", "azucares", "grasas",
           "sodio")
FAMILIAS = (
    ("cereales", "Cereal", (370, 10, 70, 12, 5, 150)),
    ("lacteos", "Yogur", (70, 6, 8, 6, 2, 50)),
    ("galletitas", "Galletita", (440, 7, 65, 20, 17, 250)),
    ("legumbres", "Lenteja", (330, 23, 55, 2, 2, 8)),
    ("frutos secos", "Mezcla", (590, 19, 20, 4, 49, 4)),
)


def crear_registros():
    """Devolver 500 fichas deterministas; ningún código es comercial real."""
    registros = []
    for numero in range(500):
        categoria, nombre, base = FAMILIAS[numero % len(FAMILIAS)]
        factor = 1 + (numero // len(FAMILIAS)) / 1000
        registro = {
            "codigo": f"{numero + 1:013d}",
            "nombre": f"{nombre} simulado {numero + 1:03d}",
            "categorias": f"{categoria}|envasados",
            "base_g": 100,
        }
        for nutriente, cantidad in zip(NOMBRES, base):
            valor = round(cantidad * factor, 6)
            unidad = "kcal" if nutriente == "energia" else "g"
            if nutriente == "sodio":
                unidad = "mg"
            if numero % 2 == 1:
                if nutriente == "energia":
                    valor = round(valor * 4.184, 6)
                    unidad = "kj"
                elif nutriente == "sodio":
                    valor = round(valor / 1000, 9)
                    unidad = "g"
                else:
                    valor = round(valor * 1000, 6)
                    unidad = "mg"
            if nutriente == "azucares" and numero % 7 == 0:
                valor = None
            if nutriente == "sodio" and numero == 2:
                valor = 0
            registro[nutriente] = valor
            registro[f"{nutriente}_unidad"] = unidad
        registros.append(registro)
    return registros


def guardar_muestra(destino=DESTINO):
    """Reemplazar CSV y JSON con la misma muestra, sin red ni aleatoriedad."""
    registros = crear_registros()
    destino.mkdir(parents=True, exist_ok=True)
    with (destino / "productos.csv").open(
            "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(registros[0]))
        escritor.writeheader()
        escritor.writerows(registros)
    (destino / "productos.json").write_text(
        json.dumps(registros, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    guardar_muestra()
    print("Se generaron 500 productos ficticios en CSV y JSON.")
