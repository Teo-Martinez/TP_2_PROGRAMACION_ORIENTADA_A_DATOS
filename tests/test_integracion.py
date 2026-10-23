"""Verificar propiedades del flujo completo y la versión mínima de sintaxis."""

import ast
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.crear_muestra import crear_registros

ROOT = Path(__file__).resolve().parents[1]


class TestIntegracion(unittest.TestCase):
    def test_comparaciones_csv_json_identicas(self):
        with tempfile.TemporaryDirectory() as carpeta:
            resultados = []
            for extension in ["csv", "json"]:
                salida = Path(carpeta) / extension
                proceso = subprocess.run(
                    [sys.executable, "-m", "src.main", "--archivo",
                     f"data/productos.{extension}", "--salida", str(salida),
                     "--categoria", "cereales", "--ordenar", "energia"],
                    cwd=ROOT, capture_output=True, text=True,
                )
                self.assertEqual(proceso.returncode, 0, proceso.stderr)
                resultados.append((salida / "comparacion.csv").read_bytes())
            self.assertEqual(resultados[0], resultados[1])

    def test_todos_rechazados_dejan_motivos(self):
        with tempfile.TemporaryDirectory() as carpeta:
            entrada = Path(carpeta) / "entrada.json"
            filas = [dict(crear_registros()[0], codigo="codigo_invalido")]
            entrada.write_text(json.dumps(filas), encoding="utf-8")
            salida = Path(carpeta) / "salidas"
            proceso = subprocess.run(
                [sys.executable, "-m", "src.main", "--archivo", str(entrada),
                 "--salida", str(salida)], cwd=ROOT, capture_output=True,
            )
            self.assertEqual(proceso.returncode, 1)
            with (salida / "rechazos.csv").open(
                    encoding="utf-8", newline="") as archivo:
                rechazos = list(csv.DictReader(archivo))
            self.assertEqual(len(rechazos), 1)
            self.assertIn("dígitos", rechazos[0]["motivo"])

    def test_proteger_entrada_de_sobrescritura(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "comparacion.csv"
            ruta.write_text("entrada que no debe borrarse", encoding="utf-8")
            original = ruta.read_bytes()
            proceso = subprocess.run(
                [sys.executable, "-m", "src.main", "--archivo", str(ruta),
                 "--salida", carpeta], cwd=ROOT, capture_output=True,
            )
            self.assertEqual(proceso.returncode, 1)
            self.assertEqual(ruta.read_bytes(), original)

    def test_sintaxis_python_310(self):
        for carpeta in ["src", "scripts", "tests"]:
            for ruta in (ROOT / carpeta).glob("*.py"):
                with self.subTest(archivo=ruta.name):
                    ast.parse(ruta.read_text(encoding="utf-8"),
                              feature_version=(3, 10))
