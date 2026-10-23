"""Verificar JSON anidado sin cambiar el contrato de las fuentes."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.crear_muestra import crear_registros
from src.consultas import comparar_etiquetas
from src.fuentes import FuenteJSON
from src.preparacion import (
    diagnosticar,
    extraer_campos,
    normalizar_ficha,
    preparar_productos,
)
from src.productos import UNIDADES

ROOT = Path(__file__).resolve().parents[1]


def anidar(fila):
    """Preparar una entrada de prueba independiente de la extracción."""
    registro = {campo: fila[campo] for campo in (
        "codigo", "nombre", "categorias", "base_g"
    )}
    registro["nutrientes"] = {
        nombre: {"valor": fila[nombre], "unidad": fila[f"{nombre}_unidad"]}
        for nombre in UNIDADES
    }
    return registro


class TestJSONAnidado(unittest.TestCase):
    def test_normalizar_y_convertir(self):
        fila = crear_registros()[1]
        producto = normalizar_ficha(anidar(fila))
        self.assertAlmostEqual(producto.obtener_nutriente("energia"), 70)
        self.assertAlmostEqual(producto.obtener_nutriente("sodio"), 50)
        self.assertEqual(producto.codigo, "0000000000002")

    def test_extraccion_no_modifica_original(self):
        registro = anidar(crear_registros()[0])
        original = deepcopy(registro)
        self.assertEqual(extraer_campos(registro), crear_registros()[0])
        self.assertEqual(registro, original)

    def test_fuente_json_entrega_campos_comunes(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "anidado.json"
            fila = crear_registros()[0]
            ruta.write_text(json.dumps([anidar(fila)]), encoding="utf-8")
            self.assertEqual(FuenteJSON().cargar(ruta), [fila])

    def test_equivalencia_de_500_fichas(self):
        planos = crear_registros()
        anidados = [anidar(fila) for fila in planos]
        p_plano, r_plano, c_plano = preparar_productos(planos)
        p_anidado, r_anidado, c_anidado = preparar_productos(anidados)
        self.assertEqual(len(p_anidado), 500)
        self.assertEqual(r_anidado, r_plano)
        self.assertEqual(c_anidado, c_plano)
        self.assertEqual(comparar_etiquetas(p_plano),
                         comparar_etiquetas(p_anidado))
        self.assertEqual(diagnosticar(anidados)["faltantes"]["azucares"], 72)

    def test_faltante_distinto_de_cero(self):
        fila = anidar(dict(crear_registros()[0], sodio=0))
        producto = normalizar_ficha(fila)
        self.assertIsNone(producto.obtener_nutriente("azucares"))
        self.assertEqual(producto.obtener_nutriente("sodio"), 0)

    def test_estructuras_invalidas_y_ambiguas(self):
        for bloque in [None, [], {"energia": 20},
                       {"energia": {"valor": 20}}]:
            with self.subTest(bloque=bloque):
                fila = anidar(crear_registros()[0])
                fila["nutrientes"] = bloque
                with self.assertRaises(ValueError):
                    extraer_campos(fila)
        fila = anidar(crear_registros()[0])
        fila["energia"] = 999
        with self.assertRaises(ValueError):
            extraer_campos(fila)
        del fila["energia"]
        del fila["nutrientes"]["sodio"]
        with self.assertRaises(ValueError):
            preparar_productos([fila])

    def test_exportacion_equivalente_desde_consola(self):
        with tempfile.TemporaryDirectory() as carpeta:
            base = Path(carpeta)
            fila = crear_registros()[:2]
            entradas = [fila, [anidar(registro) for registro in fila]]
            resultados = []
            for numero, registros in enumerate(entradas):
                ruta = base / f"entrada_{numero}.json"
                salida = base / f"salida_{numero}"
                ruta.write_text(json.dumps(registros), encoding="utf-8")
                proceso = subprocess.run(
                    [sys.executable, "-m", "src.main", "--archivo", str(ruta),
                     "--salida", str(salida)],
                    cwd=ROOT, capture_output=True, text=True,
                )
                self.assertEqual(proceso.returncode, 0, proceso.stderr)
                resultados.append((salida / "comparacion.csv").read_bytes())
            self.assertEqual(resultados[0], resultados[1])
