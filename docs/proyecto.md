# Problema y alcance

Autor: Teo Martinez.

Una persona que consulta etiquetas necesita comparar nutrientes con unidades y
bases homogéneas, sin confundir información desconocida con cero. La solución
será un catálogo de consola para buscar códigos, seleccionar categorías o varios
productos y exportar una tabla por cada 100 gramos.

La primera versión utilizará 500 productos ficticios y archivos CSV y JSON
locales equivalentes. Incluirá energía, proteínas, carbohidratos, azúcares,
grasas y sodio. Un producto podrá pertenecer a varias categorías.

Preguntas que resolverá:
1. ¿Qué valores nutricionales tiene un producto identificado por su código?
2. ¿Cómo se comparan los nutrientes de los productos elegidos?
3. ¿Qué productos pertenecen a una categoría y qué información les falta?

Quedan fuera: web, fotografías, acceso a una API, prescripción de dietas,
recomendaciones clínicas y productos expresados solo por volumen o porciones
sin masa conocida. La comparación describirá cantidades, no una clasificación
global de alimentos saludables.

## Desarrollo

Se inicia un proyecto nuevo con Git antes de implementar el programa. Se usará
el trabajo anterior como referencia de requisitos; no se modifica su historial.
El código de esta versión se implementará y comprobará en etapas sucesivas.
Los commits registran el trabajo asistido realizado ahora, con fechas actuales.
La autoría académica es Teo Martinez y la autoría técnica de los commits del
asistente se identifica como tal.

## Estructura implementada

| Módulo | Responsabilidad |
|---|---|
| scripts/crear_muestra.py | Generar entradas deterministas |
| src/fuentes.py | FuenteDatos abstracta, FuenteCSV y FuenteJSON |
| src/productos.py | ProductoNutricional y conversión |
| src/preparacion.py | Diagnóstico, normalización, validación y trazabilidad |
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
para opciones; sys para códigos de salida y errores; hashlib para identificar el
archivo original con SHA-256; unittest, tempfile, subprocess, copy y ast para
pruebas, aislamiento de casos y comprobación de sintaxis.

## Flujo y reglas

Leer → diagnosticar → validar esquema → normalizar y validar fichas → seleccionar
→ comparar → mostrar y exportar. La entrada nunca se escribe durante el análisis.
El JSON acordado usa campos planos; una fuente con datos anidados requiere una
adaptación explícita a este contrato. No se afirma importar Open Food Facts.

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
