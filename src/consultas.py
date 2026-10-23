"""Búsqueda y comparación independientes del formato de entrada."""

from src.productos import UNIDADES


def indexar_productos(productos):
    """Construir un índice sobre fichas que ya pasaron la limpieza."""
    return {producto.codigo: producto for producto in productos}


def buscar_producto(indice, codigo):
    """Devolver la ficha o None cuando el código no existe."""
    return indice.get(codigo.strip())


def listar_categorias(productos):
    """Contar pertenencias sin considerar las categorías excluyentes."""
    cantidades = {}
    for producto in productos:
        for categoria in producto.categorias:
            cantidades[categoria] = cantidades.get(categoria, 0) + 1
    return dict(sorted(cantidades.items()))


def seleccionar_productos(productos, codigos=None, categoria=None):
    """Seleccionar códigos o coincidencias exactas de categoría."""
    if codigos is not None and categoria is not None:
        raise ValueError("Elegí códigos o categoría, no ambos filtros.")
    if codigos is not None:
        indice = indexar_productos(productos)
        seleccion = []
        vistos = set()
        for codigo in codigos:
            codigo = codigo.strip()
            producto = buscar_producto(indice, codigo)
            if producto is None:
                raise ValueError(f"No existe el producto con código {codigo}.")
            if codigo not in vistos:
                seleccion.append(producto)
                vistos.add(codigo)
        return seleccion
    if categoria is not None:
        categoria = categoria.strip().casefold()
        if not categoria:
            raise ValueError("La categoría no puede estar vacía.")
        return [p for p in productos if categoria in p.categorias]
    return list(productos)


def ordenar_productos(productos, nutriente, descendente=False):
    """Ordenar cantidades convertidas; desconocidos siempre al final."""
    if nutriente not in UNIDADES:
        raise ValueError("El nutriente para ordenar no está disponible.")
    conocidos = []
    desconocidos = []
    for producto in productos:
        if producto.obtener_nutriente(nutriente) is None:
            desconocidos.append(producto)
        else:
            conocidos.append(producto)
    conocidos.sort(key=lambda p: p.obtener_nutriente(nutriente),
                   reverse=descendente)
    return conocidos + desconocidos


def comparar_etiquetas(productos):
    """Construir una tabla homogénea, conservando las ausencias como None."""
    tabla = []
    for producto in productos:
        fila = {"codigo": producto.codigo, "nombre": producto.nombre}
        for nutriente, unidad in UNIDADES.items():
            columna = f"{nutriente}_{unidad}_100g"
            fila[columna] = producto.obtener_nutriente(nutriente)
        tabla.append(fila)
    return tabla
