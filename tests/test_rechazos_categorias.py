"""Evitar que el listado de categorías oculte las fichas rechazadas."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.crear_muestra import crear_registros

ROOT = Path(__file__).resolve().parents[1]


def listar(registros, carpeta):
    """Ejecutar la consulta sobre una entrada de prueba independiente."""
    entrada = carpeta / "entrada.json"
    entrada.write_text(json.dumps(registros), encoding="utf-8")
    return subprocess.run(
        [sys.executable, "-m", "src.main", "--archivo", str(entrada),
         "--salida", str(carpeta / "salidas"), "--listar-categorias"],
        cwd=ROOT, capture_output=True, text=True,
    )


class TestRechazosCategorias(unittest.TestCase):
    def test_aviso_de_invalidos_y_duplicados(self):
        ficha = crear_registros()[0]
        registros = [ficha, dict(ficha, codigo="mal"), dict(ficha)]
        with tempfile.TemporaryDirectory() as carpeta:
            base = Path(carpeta)
            resultado = listar(registros, base)
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertIn("registros rechazados: 2 de 3", resultado.stderr)
            self.assertIn("Registro 2 | código: mal", resultado.stderr)
            self.assertIn("8 o 13 dígitos ASCII", resultado.stderr)
            esperado = "Registro 3 | código: 0000000000001"
            self.assertIn(esperado, resultado.stderr)
            self.assertIn("Código duplicado", resultado.stderr)
            self.assertIn("cereales: 1", resultado.stdout)
            self.assertIn("envasados: 1", resultado.stdout)
            self.assertFalse((base / "salidas").exists())

    def test_todos_invalidos_muestran_motivos_y_error(self):
        registros = [dict(crear_registros()[0], codigo="mal")]
        with tempfile.TemporaryDirectory() as carpeta:
            base = Path(carpeta)
            resultado = listar(registros, base)
            self.assertEqual(resultado.returncode, 1)
            self.assertIn("registros rechazados: 1 de 1", resultado.stderr)
            self.assertIn("Registro 1 | código: mal", resultado.stderr)
            self.assertIn("Error: No hay fichas válidas", resultado.stderr)
            self.assertEqual(resultado.stdout, "")
            self.assertNotIn("Traceback", resultado.stderr)
            self.assertFalse((base / "salidas").exists())

    def test_catalogo_valido_no_muestra_advertencias(self):
        with tempfile.TemporaryDirectory() as carpeta:
            resultado = listar(crear_registros(), Path(carpeta))
            self.assertEqual(resultado.returncode, 0)
            self.assertEqual(resultado.stderr, "")
            self.assertIn("cereales: 100", resultado.stdout)
            self.assertIn("envasados: 500", resultado.stdout)

    def test_listado_con_rechazos_preserva_reportes(self):
        registros = crear_registros()[:1]
        registros.append(dict(registros[0], codigo="mal"))
        with tempfile.TemporaryDirectory() as carpeta:
            base = Path(carpeta)
            salida = base / "salidas"
            salida.mkdir()
            nombres = ["comparacion.csv", "rechazos.csv", "cambios.csv",
                       "diagnostico.json"]
            anteriores = {}
            for nombre in nombres:
                ruta = salida / nombre
                ruta.write_text(f"Contenido anterior de {nombre}",
                                encoding="utf-8")
                anteriores[nombre] = ruta.read_bytes()
            resultado = listar(registros, base)
            self.assertEqual(resultado.returncode, 0)
            self.assertIn("registros rechazados: 1 de 2", resultado.stderr)
            self.assertEqual(sorted(p.name for p in salida.iterdir()),
                             sorted(nombres))
            for nombre in nombres:
                self.assertEqual((salida / nombre).read_bytes(),
                                 anteriores[nombre])
