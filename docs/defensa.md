# Preparación de la defensa

Autor: Teo Martinez. Usá estas preguntas para estudiar, no para memorizar.

- ¿Qué necesidad resuelve? Comparar nutrientes con base y unidades comunes,
  preservando la diferencia entre dato ausente y cero.
- ¿Qué representa una observación? Una ficha ficticia por cada 100 g.
- ¿De dónde provienen los datos? De scripts/crear_muestra.py; son simulados,
  reproducibles y sin representatividad comercial.
- ¿Por qué cuatro clases? ProductoNutricional reúne ficha y conversiones;
  FuenteDatos define un contrato que implementan FuenteCSV y FuenteJSON.
- ¿Qué verifica la regex? Exactamente 8 o 13 dígitos ASCII. No el dígito EAN.
- ¿Por qué código como texto? Para conservar ceros iniciales.
- ¿Qué hacés con duplicados? Conservo el primero válido y registro los demás.
- ¿Qué validación necesita más que una regex? Rangos, unidades y azúcares respecto
  de carbohidratos se comprueban con lógica adicional.
- ¿Cómo verificás resultados? Conversiones conocidas, inválidos y propiedades:
  conservación de conteos, equivalencia CSV/JSON y repetición sin acumular.
- ¿Por qué no pandas? La biblioteca estándar cubre lectura y operaciones sobre
  500 productos; listas y diccionarios permiten mostrar los conceptos del curso.
- ¿Qué evidencia deja el programa? Comparación, cambios, rechazos y diagnóstico.

Demostración: ejecutar pruebas, listar categorías, comparar dos códigos, abrir
las salidas y explicar una conversión, una clase y una prueba con tus palabras.
No uses el formato de entrevista de la rúbrica de otra materia como si fuera
obligatorio aquí: rige lo que indique esta cátedra.
