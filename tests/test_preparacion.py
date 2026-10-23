"""Probar limpieza, trazabilidad y restricciones con entradas separadas."""

from copy import deepcopy
from pathlib import Path
import unittest

from scripts.crear_muestra import crear_registros
from src.fuentes import FuenteCSV, FuenteJSON
from src.preparacion import diagnosticar, preparar_productos

ROOT = Path(__file__).resolve().parents[1]


class TestPreparacion(unittest.TestCase):
    def test_muestra_completa_y_diagnostico(self):
        registros = crear_registros()
        diagnostico = diagnosticar(registros)
        productos, rechazos, _ = preparar_productos(registros)
        self.assertEqual(len(productos), 500)
        self.assertEqual(rechazos, [])
        self.assertEqual(diagnostico["faltantes"]["azucares"], 72)

    def test_invalidos_y_limites(self):
        cambios = [
            {"codigo": "12"}, {"codigo": 12345678},
            {"codigo": "１２３４５６７８"}, {"nombre": ""},
            {"categorias": "|"}, {"base_g": 1000},
            {"proteinas": -1}, {"proteinas": "nan"},
            {"sodio": "inf"}, {"proteinas": True},
            {"grasas": 101}, {"energia_unidad": "g"},
            {"sodio_unidad": "ml"}, {"azucares": 90},
        ]
        for cambio in cambios:
            with self.subTest(cambio=cambio):
                fila = dict(crear_registros()[0], **cambio)
                productos, rechazos, _ = preparar_productos([fila])
                self.assertEqual(productos, [])
                self.assertEqual(len(rechazos), 1)

    def test_duplicados_conteos_y_entrada_intacta(self):
        fila = crear_registros()[0]
        filas = [fila, dict(fila), dict(fila, codigo="mal")]
        copia = deepcopy(filas)
        productos, rechazos, _ = preparar_productos(filas)
        self.assertEqual(len(productos), 1)
        self.assertEqual(len(productos) + len(rechazos), len(filas))
        self.assertEqual(filas, copia)

    def test_cambios_conocidos_y_ceros(self):
        fila = dict(crear_registros()[0], codigo="00000001", nombre=" Prueba ",
                    proteinas="2500", proteinas_unidad="MG", sodio=0)
        productos, rechazos, cambios = preparar_productos([fila])
        self.assertEqual(rechazos, [])
        self.assertEqual(productos[0].codigo, "00000001")
        self.assertEqual(productos[0].obtener_nutriente("sodio"), 0)
        self.assertIsNone(productos[0].obtener_nutriente("azucares"))
        indice = {c["campo"]: c for c in cambios}
        self.assertEqual(indice["proteinas"]["normalizado"], 2.5)
        self.assertEqual(indice["nombre"]["normalizado"], "Prueba")

    def test_equivalencia_lecturas(self):
        resultados = []
        for fuente, archivo in [(FuenteCSV(), "productos.csv"),
                                (FuenteJSON(), "productos.json")]:
            productos, rechazos, _ = preparar_productos(
                fuente.cargar(ROOT / "data" / archivo)
            )
            self.assertEqual(rechazos, [])
            resultados.append([
                (p.codigo, p.categorias, [p.obtener_nutriente(c) for c in (
                    "energia", "proteinas", "carbohidratos", "azucares",
                    "grasas", "sodio")]) for p in productos
            ])
        self.assertEqual(resultados[0], resultados[1])

    def test_esquema_y_vacio(self):
        for registros in [[], [{"codigo": "00000001"}]]:
            with self.assertRaises(ValueError):
                preparar_productos(registros)
