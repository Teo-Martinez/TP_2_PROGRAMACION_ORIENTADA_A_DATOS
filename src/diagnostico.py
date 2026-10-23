"""Describir estructura de entrada y nutrientes de fichas ya validadas."""

from statistics import mean

from src.consultas import listar_categorias
from src.productos import UNIDADES


def resumir_estructura(registros):
    """Inspeccionar campos y tipos de Python antes de convertir cantidades."""
    columnas = set()
    for registro in registros:
        columnas.update(registro)
    columnas = sorted(columnas)
    tipos = {campo: {} for campo in columnas}
    ausentes = {campo: 0 for campo in columnas}
    for registro in registros:
        for campo in columnas:
            if campo not in registro:
                ausentes[campo] += 1
            else:
                tipo = type(registro[campo]).__name__
                tipos[campo][tipo] = tipos[campo].get(tipo, 0) + 1
    categorias = {}
    unidades = {nutriente: {} for nutriente in UNIDADES}
    for registro in registros:
        texto = registro.get("categorias", "")
        if isinstance(texto, str):
            nombres = {c.strip().casefold() for c in texto.split("|")}
            for nombre in sorted(nombres):
                if nombre:
                    categorias[nombre] = categorias.get(nombre, 0) + 1
        for nutriente in UNIDADES:
            unidad = registro.get(f"{nutriente}_unidad")
            etiqueta = repr(unidad)
            conteos = unidades[nutriente]
            conteos[etiqueta] = conteos.get(etiqueta, 0) + 1
    ejemplos = []
    for registro in registros[:3]:
        # repr permite mostrar incluso entradas erróneas sin exportar NaN JSON.
        ejemplo = {campo: repr(valor) for campo, valor in registro.items()}
        ejemplos.append(ejemplo)
    return {
        "filas": len(registros),
        "cantidad_columnas": len(columnas),
        "columnas": columnas,
        "tipos_observados": tipos,
        "categorias_entrada": dict(sorted(categorias.items())),
        "unidades_entrada_como_texto": unidades,
        "campos_ausentes": ausentes,
        "ejemplos_como_texto": ejemplos,
    }


def resumir_nutrientes(productos):
    """Calcular cobertura y estadísticas con valores conocidos por 100 g."""
    resumen = {}
    for nutriente, unidad in UNIDADES.items():
        conocidos = []
        for producto in productos:
            valor = producto.obtener_nutriente(nutriente)
            if valor is not None:
                conocidos.append(valor)
        cantidad = len(conocidos)
        cobertura = None
        if productos:
            cobertura = 100 * cantidad / len(productos)
        resumen[nutriente] = {
            "unidad": unidad,
            "base_g": 100,
            "conocidos": cantidad,
            "desconocidos": len(productos) - cantidad,
            "cobertura_porcentaje": cobertura,
            "minimo": min(conocidos) if conocidos else None,
            "maximo": max(conocidos) if conocidos else None,
            "media": mean(conocidos) if conocidos else None,
        }
    return resumen


def resumir_validos(productos):
    """Resumir el catálogo aceptado antes de filtrar la consulta."""
    return {
        "total_productos": len(productos),
        "categorias": listar_categorias(productos),
        "nutrientes": resumir_nutrientes(productos),
    }
