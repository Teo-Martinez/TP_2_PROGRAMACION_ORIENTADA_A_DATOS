"""Inspección, normalización y validación sin alterar los datos originales."""

import math
import re

from src.diagnostico import resumir_estructura
from src.productos import ProductoNutricional, UNIDADES

CAMPOS = ["codigo", "nombre", "categorias", "base_g"]
for nombre in UNIDADES:
    CAMPOS.extend([nombre, f"{nombre}_unidad"])


def extraer_campos(registro):
    """Adaptar nutrientes anidados al esquema plano sin alterar la entrada."""
    plano = dict(registro)
    if "nutrientes" not in registro:
        return plano
    bloque = plano.pop("nutrientes")
    if not isinstance(bloque, dict):
        raise ValueError("El campo nutrientes debe ser un objeto JSON.")
    for nombre in UNIDADES:
        if nombre in plano or f"{nombre}_unidad" in plano:
            raise ValueError("No mezcles nutrientes planos y anidados.")
        if nombre not in bloque:
            continue
        detalle = bloque[nombre]
        if not isinstance(detalle, dict):
            raise ValueError(f"{nombre}: se requiere un objeto valor/unidad.")
        if "valor" not in detalle or "unidad" not in detalle:
            raise ValueError(f"{nombre}: faltan las claves valor o unidad.")
        plano[nombre] = detalle["valor"]
        plano[f"{nombre}_unidad"] = detalle["unidad"]
    return plano


def es_faltante(valor):
    """Reconocer null y códigos de ausencia; mantener el cero como conocido."""
    return valor is None or (
        isinstance(valor, str)
        and valor.strip().casefold() in {"", "na", "n/a", "null", "none"}
    )


def convertir_numero(valor, campo):
    """Aceptar punto o coma decimal y excluir booleanos, NaN e infinito."""
    if isinstance(valor, bool):
        raise ValueError(f"{campo}: un booleano no es una cantidad.")
    try:
        numero = float(str(valor).strip().replace(",", "."))
    except ValueError as error:
        raise ValueError(f"{campo}: cantidad no numérica.") from error
    if not math.isfinite(numero) or numero < 0:
        raise ValueError(f"{campo}: debe ser finito y no negativo.")
    return numero


def diagnosticar(registros):
    """Cuantificar ausencias y repeticiones antes de aplicar la limpieza."""
    registros = [extraer_campos(registro) for registro in registros]
    faltantes = {campo: 0 for campo in CAMPOS}
    vistos = set()
    duplicados = 0
    for registro in registros:
        for campo in CAMPOS:
            if es_faltante(registro.get(campo)):
                faltantes[campo] += 1
        codigo = str(registro.get("codigo", "")).strip()
        if codigo in vistos:
            duplicados += 1
        vistos.add(codigo)
    return {
        "total_entrada": len(registros),
        "faltantes": faltantes,
        "codigos_repetidos": duplicados,
        "estructura_entrada": resumir_estructura(registros),
    }


def normalizar_ficha(registro):
    """Preparar una ficha con unidades explícitas y base exclusiva de 100 g."""
    registro = extraer_campos(registro)
    codigo = registro["codigo"]
    if not isinstance(codigo, str):
        raise ValueError("El código debe ser texto para conservar los ceros.")
    codigo = codigo.strip()
    if not re.fullmatch(r"(?:[0-9]{8}|[0-9]{13})", codigo):
        raise ValueError("El código debe tener 8 o 13 dígitos ASCII.")
    nombre = registro["nombre"]
    categorias = registro["categorias"]
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre debe ser un texto no vacío.")
    if not isinstance(categorias, str):
        raise ValueError("Las categorías deben ser texto separado por |.")
    categorias = list(dict.fromkeys(
        c.strip().casefold() for c in categorias.split("|") if c.strip()
    ))
    if not categorias:
        raise ValueError("El producto necesita al menos una categoría.")
    if convertir_numero(registro["base_g"], "base_g") != 100:
        raise ValueError("Solo se admiten fichas referidas a 100 gramos.")
    nutrientes = {}
    for campo in UNIDADES:
        valor = registro[campo]
        unidad = registro[f"{campo}_unidad"]
        if not isinstance(unidad, str):
            raise ValueError(f"{campo}: falta la unidad de medida.")
        unidad = unidad.strip().casefold()
        cantidad = None
        if not es_faltante(valor):
            cantidad = convertir_numero(valor, campo)
        nutrientes[campo] = (cantidad, unidad)
    producto = ProductoNutricional(
        codigo, nombre.strip(), categorias, nutrientes
    )
    for campo, unidad in UNIDADES.items():
        cantidad = producto.obtener_nutriente(campo)
        maximo = 1000 if unidad == "kcal" else 100
        if unidad == "mg":
            maximo = 100000
        if cantidad is not None and cantidad > maximo:
            raise ValueError(f"{campo}: supera el rango por cada 100 gramos.")
    azucar = producto.obtener_nutriente("azucares")
    carbohidratos = producto.obtener_nutriente("carbohidratos")
    conocidos = azucar is not None and carbohidratos is not None
    if conocidos and azucar > carbohidratos:
        raise ValueError("Los azúcares superan los carbohidratos.")
    return producto


def describir_cambios(registro, producto, numero):
    """Registrar valores originales y comparables de las fichas aceptadas."""
    final = {"codigo": producto.codigo, "nombre": producto.nombre,
             "categorias": "|".join(producto.categorias), "base_g": 100}
    for campo, unidad in UNIDADES.items():
        final[campo] = producto.obtener_nutriente(campo)
        final[f"{campo}_unidad"] = unidad
    cambios = []
    for campo, valor in final.items():
        if registro[campo] != valor:
            cambios.append({
                "registro": numero, "codigo": producto.codigo, "campo": campo,
                "original": registro[campo], "normalizado": valor,
                "motivo": "Normalización a la comparación por 100 g",
            })
    return cambios


def preparar_productos(registros):
    """Validar esquema, aceptar fichas y registrar cambios y rechazos."""
    if not registros:
        raise ValueError("La entrada no contiene productos.")
    registros = [extraer_campos(registro) for registro in registros]
    for numero, registro in enumerate(registros, start=1):
        faltan = sorted(set(CAMPOS) - set(registro))
        if faltan:
            campos = ", ".join(faltan)
            raise ValueError(f"Registro {numero}: faltan columnas: {campos}")
    productos = []
    rechazos = []
    cambios = []
    vistos = set()
    for numero, registro in enumerate(registros, start=1):
        try:
            producto = normalizar_ficha(registro)
            if producto.codigo in vistos:
                raise ValueError("Código duplicado; se conserva el primero.")
        except ValueError as error:
            rechazos.append({"registro": numero, "codigo": registro["codigo"],
                             "motivo": str(error)})
        else:
            vistos.add(producto.codigo)
            productos.append(producto)
            cambios.extend(describir_cambios(registro, producto, numero))
    return productos, rechazos, cambios
