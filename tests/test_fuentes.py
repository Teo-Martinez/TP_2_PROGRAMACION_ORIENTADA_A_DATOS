"""Probar contratos y errores sin depender de la lógica nutricional."""

from pathlib import Path
import tempfile
import unittest

from src.fuentes import FuenteCSV, FuenteDatos, FuenteJSON

ROOT = Path(__file__).resolve().parents[1]


class TestFuentes(unittest.TestCase):
    def test_lectores_conservan_codigos(self):
        csv = FuenteCSV().cargar(ROOT / "data/productos.csv")
        json = FuenteJSON().cargar(ROOT / "data/productos.json")
        self.assertEqual(len(csv), 500)
        self.assertEqual([r["codigo"] for r in csv],
                         [r["codigo"] for r in json])
        self.assertEqual(csv[0]["codigo"], "0000000000001")

    def test_contrato_abstracto(self):
        with self.assertRaises(TypeError):
            FuenteDatos()

    def test_entradas_malformadas(self):
        casos = [
            (FuenteCSV(), "codigo,codigo\n1,2"),
            (FuenteCSV(), "codigo,nombre\n123"),
            (FuenteCSV(), "codigo,nombre\n123,a,b"),
            (FuenteCSV(), ""),
            (FuenteJSON(), '{"productos": []}'),
            (FuenteJSON(), '[1, 2]'),
            (FuenteJSON(), '{'),
        ]
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "entrada"
            for fuente, contenido in casos:
                with self.subTest(contenido=contenido):
                    ruta.write_text(contenido, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        fuente.cargar(ruta)

    def test_archivo_inexistente_no_se_oculta(self):
        with tempfile.TemporaryDirectory() as carpeta:
            with self.assertRaises(FileNotFoundError):
                FuenteCSV().cargar(Path(carpeta) / "no_existe.csv")
