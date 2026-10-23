"""Verificar estructura, frecuencias y estadísticas sin imputar ausencias."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.crear_muestra import crear_registros
from src.diagnostico import resumir_estructura, resumir_validos
from src.fuentes import FuenteCSV, FuenteJSON
from src.preparacion import diagnosticar, preparar_productos

ROOT = Path(__file__).resolve().parents[1]


class TestDiagnostico(unittest.TestCase):
    def test_dimensiones_tipos_y_campos_ausentes(self):
        registros = [{"codigo": "00000001", "valor": None},
                     {"codigo": "00000002", "valor": 0},
                     {"codigo": "00000003", "otro": True}]
        informe = resumir_estructura(registros)
        self.assertEqual(informe["filas"], 3)
        self.assertEqual(informe["cantidad_columnas"], 3)
        self.assertEqual(informe["tipos_observados"]["valor"],
                         {"NoneType": 1, "int": 1})
        self.assertEqual(informe["campos_ausentes"]["valor"], 1)
        self.assertEqual(informe["tipos_observados"]["otro"], {"bool": 1})

    def test_ejemplos_acotados_y_entrada_intacta(self):
        registros = crear_registros()
        original = deepcopy(registros)
        informe = diagnosticar(registros)
        ejemplos = informe["estructura_entrada"]["ejemplos_como_texto"]
        self.assertEqual(len(ejemplos), 3)
        self.assertEqual(ejemplos[0]["codigo"], repr("0000000000001"))
        self.assertEqual(registros, original)
        json.dumps(informe, allow_nan=False)

    def test_errores_numericos_en_ejemplos_son_texto(self):
        informe = resumir_estructura([{"valor": float("nan")}])
        self.assertEqual(informe["ejemplos_como_texto"], [{"valor": "nan"}])
        json.dumps(informe, allow_nan=False)

    def test_conversion_cero_y_ausencia_en_estadisticas(self):
        registros = crear_registros()[:3]
        for registro, valor, unidad in zip(
                registros, [0, 2000, None], ["g", "mg", "g"]):
            registro["proteinas"] = valor
            registro["proteinas_unidad"] = unidad
        productos, _, _ = preparar_productos(registros)
        informe = resumir_validos(productos)["nutrientes"]["proteinas"]
        self.assertEqual(informe["conocidos"], 2)
        self.assertEqual(informe["desconocidos"], 1)
        self.assertEqual(informe["minimo"], 0)
        self.assertEqual(informe["maximo"], 2)
        self.assertEqual(informe["media"], 1)
        self.assertAlmostEqual(informe["cobertura_porcentaje"], 200 / 3)
        self.assertEqual(informe["unidad"], "g")

    def test_categorias_no_excluyentes_y_rechazos_excluidos(self):
        registros = crear_registros()[:2]
        registros += [dict(registros[0]), dict(registros[0], codigo="mal")]
        productos, rechazos, _ = preparar_productos(registros)
        informe = resumir_validos(productos)
        self.assertEqual(len(rechazos), 2)
        self.assertEqual(informe["total_productos"], 2)
        self.assertEqual(informe["categorias"]["envasados"], 2)
        self.assertEqual(informe["nutrientes"]["proteinas"]["conocidos"], 2)

    def test_catalogo_vacio_y_nutriente_sin_valores(self):
        informe = resumir_validos([])
        self.assertEqual(informe["categorias"], {})
        self.assertIsNone(informe["nutrientes"]["sodio"]["media"])
        sodio = informe["nutrientes"]["sodio"]
        self.assertIsNone(sodio["cobertura_porcentaje"])
        registro = dict(crear_registros()[0], proteinas=None)
        productos, _, _ = preparar_productos([registro])
        informe = resumir_validos(productos)["nutrientes"]["proteinas"]
        self.assertEqual(informe["conocidos"], 0)
        self.assertEqual(informe["desconocidos"], 1)
        self.assertEqual(informe["cobertura_porcentaje"], 0)
        self.assertIsNone(informe["media"])

    def test_muestra_completa_y_equivalencia_csv_json(self):
        resumenes = []
        for fuente, nombre in [(FuenteCSV(), "productos.csv"),
                               (FuenteJSON(), "productos.json")]:
            filas = fuente.cargar(ROOT / "data" / nombre)
            estructura = diagnosticar(filas)["estructura_entrada"]
            self.assertEqual(estructura["cantidad_columnas"], 16)
            categorias = estructura["categorias_entrada"]
            self.assertEqual(categorias["envasados"], 500)
            self.assertEqual(
                estructura["unidades_entrada_como_texto"]["energia"],
                {repr("kcal"): 250, repr("kj"): 250},
            )
            tipo = "str" if nombre.endswith("csv") else "float"
            self.assertEqual(estructura["tipos_observados"]["energia"],
                             {tipo: 500})
            productos, _, _ = preparar_productos(filas)
            informe = resumir_validos(productos)
            self.assertEqual(informe["categorias"]["cereales"], 100)
            azucares = informe["nutrientes"]["azucares"]
            self.assertEqual(azucares["conocidos"], 428)
            self.assertEqual(azucares["desconocidos"], 72)
            self.assertAlmostEqual(azucares["cobertura_porcentaje"], 85.6)
            resumenes.append(informe)
        self.assertEqual(resumenes[0], resumenes[1])

    def test_diagnostico_exportado_describe_catalogo_completo(self):
        with tempfile.TemporaryDirectory() as carpeta:
            proceso = subprocess.run(
                [sys.executable, "-m", "src.main", "--salida", carpeta,
                 "--codigos", "0000000000001"],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(proceso.returncode, 0, proceso.stderr)
            ruta = Path(carpeta) / "diagnostico.json"
            informe = json.loads(ruta.read_text(encoding="utf-8"))
            self.assertEqual(informe["estructura_entrada"]["filas"], 500)
            resumen = informe["resumen_validos"]
            self.assertEqual(resumen["total_productos"], 500)
            self.assertEqual(informe["seleccionados"], 1)
