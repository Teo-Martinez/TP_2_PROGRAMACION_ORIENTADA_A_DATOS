"""Verificar la muestra sin necesitar todavía la aplicación."""

import csv
import json
from pathlib import Path
import tempfile
import unittest

from scripts.crear_muestra import crear_registros, guardar_muestra


class TestMuestra(unittest.TestCase):
    def test_cantidad_codigos_y_repeticion(self):
        registros = crear_registros()
        self.assertEqual(len(registros), 500)
        self.assertEqual(len({r["codigo"] for r in registros}), 500)
        self.assertEqual(registros, crear_registros())
        self.assertEqual(registros[0]["codigo"], "0000000000001")

    def test_faltantes_y_cero(self):
        registros = crear_registros()
        self.assertEqual(sum(r["azucares"] is None for r in registros), 72)
        self.assertEqual(registros[2]["sodio"], 0)

    def test_archivos_generados(self):
        with tempfile.TemporaryDirectory() as carpeta:
            destino = Path(carpeta)
            guardar_muestra(destino)
            with (destino / "productos.csv").open(
                    encoding="utf-8", newline="") as archivo:
                csv_filas = list(csv.DictReader(archivo))
            json_filas = json.loads(
                (destino / "productos.json").read_text(encoding="utf-8")
            )
            self.assertEqual(len(csv_filas), 500)
            self.assertEqual(json_filas, crear_registros())
            self.assertEqual(csv_filas[0]["codigo"], json_filas[0]["codigo"])
