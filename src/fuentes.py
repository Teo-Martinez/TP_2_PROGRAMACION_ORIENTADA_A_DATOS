"""Fuentes intercambiables que entregan una lista de diccionarios."""

from abc import ABC, abstractmethod
import csv
import json


class FuenteDatos(ABC):
    """Contrato común de lectura para la aplicación."""

    @abstractmethod
    def cargar(self, ruta):
        """Leer registros sin normalizar sus valores."""


class FuenteCSV(FuenteDatos):
    """Leer CSV sin convertir códigos a números."""

    def cargar(self, ruta):
        with open(ruta, encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)
            encabezado = lector.fieldnames
            if not encabezado:
                raise ValueError("El CSV está vacío o no tiene encabezado.")
            if len(encabezado) != len(set(encabezado)):
                raise ValueError("El CSV tiene nombres de columnas repetidos.")
            registros = list(lector)
        for numero, registro in enumerate(registros, start=1):
            if None in registro or None in registro.values():
                raise ValueError(f"Registro {numero}: cantidad de campos errónea.")
        return registros


class FuenteJSON(FuenteDatos):
    """Leer una lista JSON de fichas con campos planos."""

    def cargar(self, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            registros = json.load(archivo)
        if not isinstance(registros, list):
            raise ValueError("El JSON debe contener una lista de productos.")
        if not all(isinstance(registro, dict) for registro in registros):
            raise ValueError("Cada producto JSON debe ser un objeto.")
        return registros
