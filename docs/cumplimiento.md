# Revisión de requisitos

Autor: Teo Martinez.

| Paso de la consigna | Evidencia del proyecto |
|---|---|
| 1. Problema y alcance | docs/proyecto.md: usuario, necesidad, solución, tres preguntas y límites |
| 2. Datos y procedencia | data/README.md y generador: 500 fichas simuladas, variables, unidades, condiciones de uso y limitaciones |
| 3. Flujo reproducible | Lectura CSV/JSON plano o anidado, diagnóstico previo, validación, limpieza, comparación y cuatro salidas |
| 4. Conceptos del curso | Funciones separadas, ProductoNutricional, FuenteDatos abstracta, FuenteCSV/FuenteJSON y regex EAN |
| 5. Verificaciones | 49 pruebas: casos conocidos e inválidos, conversiones, equivalencia entre formatos, conteos y repetición |
| 6. Git/GitHub | Git desde el alcance inicial, ocho commits de desarrollo y correcciones posteriores; repositorio publicado |
| 7. Documentación y defensa | README de ejecución, documentación enlazada, ejemplos interpretados, guía de defensa y entrega identificada por commit |

Repositorio: [TP_2_PROGRAMACION_ORIENTADA_A_DATOS](https://github.com/Teo-Martinez/TP_2_PROGRAMACION_ORIENTADA_A_DATOS).

## Consideraciones de la opción 9

- Códigos conservados como texto, incluidos los ceros iniciales.
- Patrón de 8 o 13 dígitos ASCII; no se comprueba el dígito verificador EAN.
- Nutrientes convertidos a kcal, g o mg por cada 100 gramos.
- Categorías múltiples con selección por coincidencia exacta en cualquiera.
- Datos desconocidos como None, mostrados como No disponible, distintos de cero.
- Extracción de nutrientes anidados mediante el contrato documentado de JSON.
- Cambios y rechazos trazables; el listado de categorías también informa descartes.

## Criterios aplicables de la rúbrica adjunta

Se documenta la fuente concreta: una simulación permitida por la consigna.
Open Food Facts es una posibilidad, no una obligación. La muestra tiene un
procedimiento reproducible y sirve para verificar la aplicación; no ofrece
fiabilidad empírica sobre etiquetas comerciales reales.

El diagnóstico muestra dimensiones, campos, tipos, frecuencias, ejemplos y
faltantes antes de limpiar; después resume fichas válidas en unidades comunes,
con cobertura, mínimo, máximo y media. Hay reglas justificadas de limpieza,
registros de acciones y conteos antes/después. Los rechazos se prueban con casos
separados cuando la muestra principal arroja cero. Los originales se conservan
y las ejecuciones no acumulan registros. Se interpretan resultados con sus
unidades y limitaciones.

No se trasladan requisitos propios del otro trabajo: R, SQLite, JOIN,
transacciones, Colab, cuatro tablas relacionales o gráficos obligatorios.
La consigna de esta materia admite una tabla como resultado. El README breve
responde a la indicación del profesor y enlaza el resto de la documentación.

## Aspectos de la entrega y defensa

La publicación está realizada. Al entregar, comprobar acceso para la cátedra e
identificar el commit final según [entrega.md](entrega.md). El estudiante debe
poder explicar el proceso y defender decisiones individuales. El historial
muestra desarrollo asistido registrado; no sustituye esa comprensión.
La revisión técnica no determina una calificación ni acredita requisitos de
presentación o fechas que solo la cátedra puede comunicar por EVA.
