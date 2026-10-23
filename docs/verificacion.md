# Verificación técnica

Se ejecutaron las pruebas disponibles antes de confirmar cada implementación.
La prueba de sintaxis final usa la gramática de Python 3.10. La ejecución real se
comprobó con Python 3.12; eso no equivale a ejecutar en todas las versiones.

```bash
python -m unittest discover -s tests -v
```

Resultado: 49 pruebas correctas. Incluyen generación determinista, lectores,
conversiones, faltantes frente a cero, EAN con ceros iniciales, rangos,
duplicados, trazabilidad, conservación de conteos, consultas, ordenamiento,
exportación, protección de entrada y equivalencia integral entre CSV y JSON.
La muestra tiene 500 fichas válidas y 72 azúcares ausentes. Cero rechazos se
informa explícitamente; los errores se prueban en entradas separadas.

Se revisó PEP 8 con pycodestyle (reglas predeterminadas, 79 columnas). Esta
herramienta es de revisión y no es una dependencia para ejecutar la aplicación.
Para reproducir esa revisión opcional: instalar pycodestyle y ejecutar
`python -m pycodestyle src scripts tests`.

La primera corrección agrega siete pruebas de JSON anidado: conversión conocida,
entrada intacta, contrato común del lector, equivalencia de 500 fichas, ausencias
frente a cero, estructuras inválidas y exportación desde la consola.

La segunda corrección añade ocho pruebas de diagnóstico: dimensiones y tipos,
ejemplos sin modificar entradas, valores inválidos como texto, estadísticas
con unidades mixtas y ceros, exclusión de rechazos/duplicados, casos sin valores,
equivalencia CSV/JSON y diagnóstico exportado sobre todo el catálogo.

La tercera corrección añade cuatro pruebas del listado de categorías: aviso con
rechazos mixtos y duplicados, detalle cuando todas las fichas son inválidas,
ausencia de avisos en entradas válidas y preservación de reportes existentes.
