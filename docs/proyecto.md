# Problema y alcance

Autor: Teo Martinez.

Una persona que consulta etiquetas necesita comparar nutrientes con unidades y
bases homogéneas, sin confundir información desconocida con cero. La solución
es un catálogo de consola para buscar códigos, seleccionar categorías o varios
productos y exportar una tabla por cada 100 gramos.

La versión implementada utiliza 500 productos ficticios y archivos CSV y JSON
locales equivalentes. Incluye energía, proteínas, carbohidratos, azúcares,
grasas y sodio. Un producto puede pertenecer a varias categorías.

Preguntas que resuelve:
1. ¿Qué valores nutricionales tiene un producto identificado por su código?
2. ¿Cómo se comparan los nutrientes de los productos elegidos?
3. ¿Qué productos pertenecen a una categoría y qué información les falta?

Quedan fuera: web, fotografías, acceso a una API, prescripción de dietas,
recomendaciones clínicas y productos expresados solo por volumen o porciones
sin masa conocida. La comparación describe cantidades, no una clasificación
global de alimentos saludables.

## Desarrollo

Git se inicializó antes de implementar el programa. El historial registra ocho
etapas iniciales: alcance, simulación, fuentes, modelo, preparación, consultas,
consola y verificación integral. Después se incorporaron mejoras de JSON anidado,
diagnóstico y comunicación de rechazos. La publicación en GitHub se realizó
después del desarrollo local; se conserva la integración del README remoto.

El código se elaboró con asistencia de IA. El historial distingue la autoría
técnica de los commits y los avances confirmados por el estudiante. Teo Martinez
figura como autor del trabajo. El repositorio publicado y el procedimiento para
identificar la versión evaluada están en [entrega.md](entrega.md).

## Estructura implementada

| Módulo | Responsabilidad |
|---|---|
| scripts/crear_muestra.py | Generar entradas deterministas |
| src/fuentes.py | FuenteDatos abstracta, FuenteCSV y FuenteJSON |
| src/productos.py | ProductoNutricional y conversión |
| src/preparacion.py | Normalización, validación y trazabilidad |
| src/diagnostico.py | Estructura de entrada y estadísticas de fichas válidas |
| src/consultas.py | Índice, búsqueda, categorías, selección y comparación |
| src/salidas.py | Consola y exportaciones |
| src/main.py | Parámetros y coordinación |
| tests/ | Verificaciones unitarias e integrales |

La herencia aporta una operación común `cargar(ruta)` para fuentes diferentes.
El modelo reúne atributos de dominio y un comportamiento: obtener nutrientes en
la unidad de comparación. El índice usa códigos como claves de diccionario.
Se usan funciones pequeñas y listas/diccionarios; no se requieren pandas ni web.

Bibliotecas estándar: abc para abstracción; csv/json para archivos; re para el
patrón de código; math para excluir NaN e infinito; pathlib para rutas; argparse
para opciones; statistics para la media de valores conocidos; sys para errores;
hashlib para identificar el
archivo original con SHA-256; unittest, tempfile, subprocess, copy y ast para
pruebas, aislamiento de casos y comprobación de sintaxis.

## Flujo y reglas

Leer → diagnosticar → validar esquema → normalizar y validar fichas → seleccionar
→ comparar → mostrar y exportar. La entrada nunca se escribe durante el análisis.
El JSON admite campos planos o nutrientes anidados con valor y unidad.
`extraer_campos` adapta esa estructura al contrato común sin modificar la
entrada. No se afirma importar cualquier esquema de Open Food Facts.

1. Encabezados únicos y filas CSV con igual cantidad de campos. JSON debe ser
   una lista de objetos. Fallas de apertura y JSON malformado se informan.
2. Todos los campos definidos deben existir; una tabla sin esquema o vacía
   detiene la ejecución. Una ficha inválida se rechaza y se continúa con otras.
3. Código siempre texto, sin espacios externos; regex con re.fullmatch:
   `(?:[0-9]{8}|[0-9]{13})`. Valida longitud y dígitos ASCII, no dígito de control
   ni existencia comercial. No se pierden ceros iniciales.
4. Nombre obligatorio. Categorías y unidades se normalizan con strip/casefold.
   Categorías duplicadas en una ficha se unifican; se filtra por coincidencia
   exacta con cualquiera. Un producto puede contarse en más de una categoría.
5. Base igual a 100 g; no se equipara un volumen a una masa. kJ / 4.184 da kcal;
   mg / 1000 da g; g * 1000 da mg. No se confunde sal con sodio.
6. Ausencias: null, celda vacía y textos NA, N/A, null o None (sin distinguir
   mayúsculas). Se conservan como None; se comunican como No disponible. Las
   unidades siguen siendo obligatorias. Cero no es ausencia.
7. Valores finitos y no negativos; booleanos inválidos. Máximos de control:
   1000 kcal, 100 g por nutriente y 100000 mg de sodio por cada 100 g. Estos son
   límites técnicos, no umbrales de salud. Un extremo válido no se elimina por
   ser infrecuente. Azúcares no puede superar carbohidratos si ambos se conocen.
8. Duplicados: conservar el primer registro válido por código y rechazar los
   siguientes. No se mezclan fichas ni se selecciona una actualización sin fecha.
9. Código solicitado ausente y opciones incompatibles dan error antes de escribir
   salidas. Categoría sin coincidencias es una consulta válida con tabla vacía.
10. Ordenamiento con unidades convertidas, desconocidos al final y desempate
    estable según orden de selección. No se altera el catálogo al ordenar.

## Diagnóstico y trazabilidad

`diagnostico.json` cuantifica entradas, ausencias previas, códigos repetidos,
válidos, rechazados, seleccionados y registros/campos modificados. Incluye SHA-256
del archivo original. CSV y JSON tienen distinta huella aunque sean equivalentes.
`cambios.csv` conserva número de registro, código, campo, valor original,
normalizado y motivo para fichas aceptadas. `rechazos.csv` registra el primer
motivo por ficha rechazada. Registro 1 es el primer producto, no el encabezado.
Tipos de texto a número también cuentan como normalización; por eso el número
de cambios puede diferir entre CSV y JSON sin cambiar el resultado nutricional.

La muestra genera 500 válidos, cero rechazos y 72 azúcares ausentes; los rechazos
se ejercitan con casos separados en tests. Válidos + rechazados debe ser igual
a entradas. No se imputan faltantes ni se descartan extremos dentro de rango.
Las salidas se reemplazan: no se acumulan filas. Una consulta inválida preserva
salidas anteriores. No hay transacción atómica entre varios archivos frente a
fallos de disco. Se conservan decimales internos y se muestran dos en consola.

## Interpretación de un resultado

Los códigos 0000000000001 y 0000000000002 tienen 10 g y 6 g de proteínas por
100 g, respectivamente. El segundo registra 292.88 kJ y la comparación muestra
70 kcal. El primero no tiene azúcar disponible: no se interpreta como cero.
Esto describe los productos simulados; no demuestra qué alimento real conviene
consumir ni permite generalizar a marcas o a una población.

## Diagnóstico ampliado

`estructura_entrada` en diagnostico.json describe la tabla adaptada al esquema
común, antes de convertir tipos o rechazar fichas. Incluye filas, columnas, tipos
de Python observados por campo, campos estructuralmente ausentes, frecuencias
de categorías y unidades, y hasta tres ejemplos como texto. CSV presenta
cantidades como str y JSON normalmente como int/float: es una diferencia de
formato, no un error por sí sola. Un campo ausente no es igual a un campo
presente con null; la sección faltantes conserva el conteo general de ausencias.
Los ejemplos y unidades originales se muestran con repr, como texto, incluso
si contienen cantidades inválidas. Las categorías de entrada se cuentan una vez
por fila y categoría, conservando las filas que después podrían rechazarse.

`resumen_validos` usa todas las fichas aceptadas, antes de filtrar una consulta.
Incluye frecuencias de categorías y, para cada nutriente, unidad, base de 100 g,
conocidos, desconocidos, cobertura porcentual, mínimo, máximo y media. Estas
estadísticas se calculan después de validar y convertir unidades; no se mezclan
g y mg ni se incorporan fichas rechazadas o duplicadas. Cero participa como
valor conocido. Una ausencia nunca se reemplaza por cero para calcular la media.

La cobertura es 100 * conocidos / total de productos válidos. Si no hay productos,
la cobertura es null. Si hay productos pero ningún valor del nutriente, la
cobertura es 0 y mínimo/máximo/media son null. Las categorías no son excluyentes,
por lo que sumar sus frecuencias no da necesariamente el número de productos.

En la muestra: 500 filas, 16 columnas, cinco familias de 100 productos y categoría
compartida envasados con 500. Azúcares tiene 428 valores conocidos, 72 desconocidos
y cobertura de 85,6 %. La energía de entrada se reparte en 250 kcal y 250 kJ.
CSV y JSON producen el mismo resumen nutricional; sus tipos originales difieren.
Esta evidencia permite justificar la conversión y el tratamiento de faltantes.

## Rechazos durante el listado de categorías

`--listar-categorias` informa por la salida de errores (stderr) cuántos registros
fueron rechazados, junto con número de registro, código y primer motivo de
rechazo de cada ficha. Los conteos de categorías (stdout) usan solo productos
válidos, sin contar duplicados descartados. Si hay fichas válidas, la consulta
termina con código 0 y el aviso permite reconocer que el catálogo fue depurado.
Si todas las fichas se rechazan, muestra sus motivos y termina con código 1.
Si ninguna se rechaza, no muestra una advertencia innecesaria.

El listado no crea ni modifica comparaciones, rechazos, cambios o diagnósticos
previos. Para guardar esos reportes se debe ejecutar una comparación. Los errores
de estructura o lectura siguen deteniendo la entrada con un mensaje explícito.
