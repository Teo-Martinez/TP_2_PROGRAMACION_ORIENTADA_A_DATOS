# Datos simulados

Responsable del proyecto: Teo Martinez. Preparación: 23/10/2026.
Datos sintéticos elaborados con asistencia de IA para uso educativo, sin fuentes
externas, datos personales ni valores de marcas reales. No corresponde atribuir
una licencia de Open Food Facts ni una fecha de consulta a estos datos propios.
Se autoriza reutilizar la muestra en actividades educativas.

Procedimiento verificable: `python scripts/crear_muestra.py`. Genera 500 fichas
sin azar: cinco familias de 100 productos, con un factor que aumenta 0,001 por
ronda. Guarda las mismas observaciones en CSV y JSON. El archivo completo es
pequeño y se conserva en el repositorio; no se descarga ni se filtra una base mayor.

Unidad de análisis: una ficha ficticia de un producto por cada 100 gramos.
CSV separado por comas, UTF-8, encabezado; JSON como lista de objetos planos o con nutrientes anidados.

| Campos | Tipo y unidad |
|---|---|
| codigo | Texto de 8 o 13 dígitos; los ceros iniciales se conservan |
| nombre | Texto obligatorio |
| categorias | Texto con categorías separadas por barra vertical |
| base_g | Número; 100 gramos |
| energia; energia_unidad | Número o ausencia; kcal o kj |
| proteinas, carbohidratos, azucares, grasas | Número o ausencia; g o mg |
| sodio | Número o ausencia; g o mg |
| Campo terminado en _unidad | Texto con la unidad del nutriente correspondiente |

La muestra incluye unidades mixtas, 72 azúcares ausentes y un sodio cero.
CSV vacío y JSON null representan desconocidos; cero representa cantidad nula.
No se transforman gramos de sal en sodio. Las categorías no son excluyentes.

Limitaciones: datos ilustrativos, distribución artificial, sin representatividad
comercial ni verificación empírica. No sirven para recomendar una dieta. Los
códigos ficticios no garantizan dígito verificador EAN correcto.

## JSON con nutrientes anidados

También se admite un objeto `nutrientes` por ficha, con una entrada por cada
nutriente conocido. Cada entrada tiene las claves `valor` y `unidad`, por ejemplo:

```json
"proteinas": {"valor": 6000, "unidad": "mg"}
```

Ese fragmento pertenece a `nutrientes`; el ejemplo completo y ejecutable está en
`data/ejemplo_anidado.json`, con dos fichas de la misma muestra simulada:

```bash
python -m src.main --archivo data/ejemplo_anidado.json
```

`FuenteJSON` entrega el mismo esquema plano que CSV. La extracción se reutiliza
en `normalizar_ficha`, en el diagnóstico y en la preparación, para admitir
también fichas anidadas recibidas directamente por esas funciones.
No se modifica el objeto original. Los cambios conservan valores originales
y normalizados con los nombres del esquema plano.

Reglas: no mezclar nutrientes planos y anidados en una misma ficha; no se
resuelven conflictos eligiendo un valor arbitrario. El bloque y cada nutriente
deben ser objetos. Todos los nutrientes del esquema deben estar presentes,
incluso si `valor` es null; `unidad` es obligatoria. Si la estructura es incorrecta,
se informa un error de entrada. Las reglas numéricas siguen registrando rechazos
por ficha. Esta adaptación no convierte el programa en un importador genérico
de cualquier API: otros esquemas requieren su propia adaptación.
