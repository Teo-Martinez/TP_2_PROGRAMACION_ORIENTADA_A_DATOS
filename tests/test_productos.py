"""Comprobar unidades y ausencia de información en el modelo."""

import unittest

from src.productos import ProductoNutricional


class TestProducto(unittest.TestCase):
    def test_conversiones_conocidas(self):
        producto = ProductoNutricional("00000001", "Ficha", ["cereales"], {
            "energia": (418.4, "kj"), "sodio": (0.2, "g"),
            "proteinas": (2500, "mg"), "grasas": (5, "g"),
        })
        self.assertAlmostEqual(producto.obtener_nutriente("energia"), 100)
        self.assertEqual(producto.obtener_nutriente("sodio"), 200)
        self.assertEqual(producto.obtener_nutriente("proteinas"), 2.5)
        self.assertEqual(producto.obtener_nutriente("grasas"), 5)

    def test_faltante_no_es_cero(self):
        producto = ProductoNutricional("00000001", "Ficha", [], {
            "sodio": (0, "mg"), "proteinas": (None, "g"),
        })
        self.assertEqual(producto.obtener_nutriente("sodio"), 0)
        self.assertIsNone(producto.obtener_nutriente("proteinas"))

    def test_unidad_y_nutriente_incompatibles(self):
        producto = ProductoNutricional("00000001", "Ficha", [], {
            "sodio": (3, "ml"),
        })
        with self.assertRaises(ValueError):
            producto.obtener_nutriente("sodio")
        with self.assertRaises(ValueError):
            producto.obtener_nutriente("vitamina_x")
