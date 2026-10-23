# Comparador de etiquetas nutricionales

Autor: Teo Martinez. TP2 de Programación Orientada a Datos.

Consulta y compara nutrientes por cada 100 g. Incluye 500 productos ficticios.
Requiere Python 3.10 o posterior, sin instalar bibliotecas externas.

Abrí la terminal en la raíz del proyecto:

```bash
python -m src.main --listar-categorias
python -m src.main --codigos 0000000000001 0000000000002
python -m src.main --categoria cereales --ordenar proteinas --descendente
python -m src.main --archivo data/productos.json --categoria lacteos
```

Sin filtros compara todo el catálogo. `--help` muestra las opciones.
En Windows podés usar `py` en lugar de `python`.

Cada comparación válida reemplaza cuatro archivos en `outputs/`:
`comparacion.csv`, `rechazos.csv`, `cambios.csv` y `diagnostico.json`.
`--salida otra_carpeta` permite conservar ejecuciones por separado.
Los faltantes aparecen como "No disponible". Listar categorías no escribe archivos.

Pruebas:

```bash
python -m unittest discover -s tests -v
```

Datos y formato: [data/README.md](data/README.md).
Problema y diseño: [docs/proyecto.md](docs/proyecto.md).
