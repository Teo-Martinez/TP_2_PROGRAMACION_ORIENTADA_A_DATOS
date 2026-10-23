"""Ficha de producto y reglas de conversión por cada 100 gramos."""

UNIDADES = {
    "energia": "kcal",
    "proteinas": "g",
    "carbohidratos": "g",
    "azucares": "g",
    "grasas": "g",
    "sodio": "mg",
}


class ProductoNutricional:
    """Reunir identidad, categorías y valores con sus unidades de origen."""

    def __init__(self, codigo, nombre, categorias, nutrientes):
        self.codigo = codigo
        self.nombre = nombre
        self.categorias = list(categorias)
        self.nutrientes = dict(nutrientes)

    def obtener_nutriente(self, nutriente):
        """Devolver un valor comparable o None si no está disponible."""
        if nutriente not in UNIDADES:
            raise ValueError(f"Nutriente no admitido: {nutriente}")
        valor, unidad = self.nutrientes[nutriente]
        destino = UNIDADES[nutriente]
        permitidas = {"kcal", "kj"} if destino == "kcal" else {"g", "mg"}
        if unidad not in permitidas:
            raise ValueError(f"Unidad no admitida para {nutriente}: {unidad}")
        if valor is None:
            return None
        if unidad == destino:
            return valor
        if destino == "kcal":
            return valor / 4.184
        if destino == "g":
            return valor / 1000
        return valor * 1000
