"""Probar ejecuciones reales, exportaciones y protección de la entrada."""

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def correr(*opciones):
    return subprocess.run([sys.executable, "-m", "src.main", *opciones],
                          cwd=ROOT, capture_output=True, text=True)


class TestConsola(unittest.TestCase):
    def test_exportacion_y_repeticion(self):
        with tempfile.TemporaryDirectory() as carpeta:
            opciones = ["--salida", carpeta, "--codigos", "0000000000001",
                        "0000000000002"]
            resultado = correr(*opciones)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            ruta = Path(carpeta) / "comparacion.csv"
            anterior = ruta.read_bytes()
            with ruta.open(encoding="utf-8", newline="") as archivo:
                filas = list(csv.DictReader(archivo))
            self.assertEqual(len(filas), 2)
            self.assertEqual(filas[0]["codigo"], "0000000000001")
            self.assertEqual(filas[0]["azucares_g_100g"], "No disponible")
            ruta_informe = Path(carpeta) / "diagnostico.json"
            informe = json.loads(ruta_informe.read_text(encoding="utf-8"))
            self.assertEqual(informe["validos"], 500)
            self.assertEqual(informe["seleccionados"], 2)
            self.assertEqual(correr(*opciones).returncode, 0)
            self.assertEqual(ruta.read_bytes(), anterior)

    def test_error_no_modifica_salidas(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "comparacion.csv"
            ruta.write_text("anterior", encoding="utf-8")
            resultado = correr("--salida", carpeta, "--codigos", "99999999")
            self.assertEqual(resultado.returncode, 1)
            self.assertEqual(ruta.read_text(), "anterior")
            self.assertEqual(len(list(Path(carpeta).iterdir())), 1)

    def test_listado_no_escribe(self):
        with tempfile.TemporaryDirectory() as carpeta:
            resultado = correr("--salida", carpeta, "--listar-categorias")
            self.assertEqual(resultado.returncode, 0)
            self.assertIn("cereales: 100", resultado.stdout)
            self.assertEqual(list(Path(carpeta).iterdir()), [])

    def test_errores_de_entrada_y_opciones(self):
        for opciones in [["--archivo", "no_existe.csv"], ["--descendente"],
                         ["--listar-categorias", "--ordenar", "sodio"]]:
            with self.subTest(opciones=opciones):
                resultado = correr(*opciones)
                self.assertEqual(resultado.returncode, 1)
                self.assertIn("Error:", resultado.stderr)

    def test_categoria_sin_coincidencias(self):
        with tempfile.TemporaryDirectory() as carpeta:
            resultado = correr("--salida", carpeta, "--categoria", "otra")
            self.assertEqual(resultado.returncode, 0)
            ruta = Path(carpeta) / "comparacion.csv"
            self.assertEqual(len(ruta.read_text().splitlines()), 1)
