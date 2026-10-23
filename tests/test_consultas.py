"""Probar selección y comparación con fichas previamente validadas."""

import unittest

from scripts.crear_muestra import crear_registros
from src.consultas import (
    buscar_producto,
    comparar_etiquetas,
    indexar_productos,
    listar_categorias,
    ordenar_productos,
    seleccionar_productos,
)
from src.preparacion import preparar_productos


class TestConsultas(unittest.TestCase):
    def setUp(self):
        self.productos, _, _ = preparar_productos(crear_registros())

    def test_busqueda_normal_y_ausente(self):
        indice = indexar_productos(self.productos)
        self.assertEqual(buscar_producto(indice, "0000000000001").nombre,
                         "Cereal simulado 001")
        self.assertIsNone(buscar_producto(indice, "99999999"))

    def test_multiples_categorias(self):
        categorias = listar_categorias(self.productos)
        self.assertEqual(categorias["envasados"], 500)
        self.assertEqual(categorias["cereales"], 100)
        self.assertEqual(len(seleccionar_productos(
            self.productos, categoria=" CEREALES ")), 100)
        self.assertEqual(seleccionar_productos(
            self.productos, categoria="inexistente"), [])

    def test_codigos_repetidos_y_filtros_invalidos(self):
        codigo = "0000000000001"
        self.assertEqual(len(seleccionar_productos(
            self.productos, codigos=[codigo, codigo])), 1)
        for parametros in [{"codigos": ["99999999"]}, {"categoria": " "},
                           {"codigos": [codigo], "categoria": "cereales"}]:
            with self.subTest(parametros=parametros):
                with self.assertRaises(ValueError):
                    seleccionar_productos(self.productos, **parametros)

    def test_comparacion_y_faltante(self):
        tabla = comparar_etiquetas(self.productos[:2])
        self.assertEqual(tabla[0]["proteinas_g_100g"], 10)
        self.assertAlmostEqual(tabla[1]["energia_kcal_100g"], 70)
        self.assertIsNone(tabla[0]["azucares_g_100g"])
        self.assertEqual(comparar_etiquetas([]), [])

    def test_ordenamiento_conversion_empates_y_ausencias(self):
        registros = crear_registros()[:4]
        for registro, valor, unidad in zip(
                registros, [None, 2000, 0, 2], ["g", "mg", "g", "g"]):
            registro["proteinas"] = valor
            registro["proteinas_unidad"] = unidad
        productos, _, _ = preparar_productos(registros)
        asc = ordenar_productos(productos, "proteinas")
        desc = ordenar_productos(productos, "proteinas", True)
        self.assertEqual([p.codigo for p in asc], [
            productos[i].codigo for i in [2, 1, 3, 0]])
        self.assertEqual([p.codigo for p in desc], [
            productos[i].codigo for i in [1, 3, 2, 0]])
        self.assertIs(productos[0], asc[-1])
        with self.assertRaises(ValueError):
            ordenar_productos(productos, "nutriente_inexistente")
