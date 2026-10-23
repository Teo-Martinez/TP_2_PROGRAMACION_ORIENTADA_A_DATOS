# Entrega del trabajo práctico

Autor: Teo Martinez.

## Repositorio publicado

[Comparador de etiquetas nutricionales](https://github.com/Teo-Martinez/TP_2_PROGRAMACION_ORIENTADA_A_DATOS)

El proyecto está publicado en la rama main. Conserva los ocho commits del
desarrollo inicial, la integración del README inicial de GitHub y las
correcciones posteriores. Git se utilizó localmente desde la definición del
alcance; la publicación en GitHub se realizó después. Las fechas y autorías
registradas por Git se conservan. El código se elaboró con asistencia de IA;
la explicación y defensa individual corresponden al estudiante.

## Verificar antes de entregar

Desde la raíz del proyecto, en Windows:

```bash
py -m unittest discover -s tests -v
git status
git log --oneline --graph --all
```

Deben aprobarse las 49 pruebas. Revisar que no queden cambios del proyecto sin
confirmar y que el último commit se haya enviado al remoto. Las salidas dentro
de outputs/ están excluidas mediante .gitignore: se regeneran al ejecutar.

Demostración de uso:

```bash
py -m src.main --listar-categorias
py -m src.main --codigos 0000000000001 0000000000002
py -m src.main --archivo data/ejemplo_anidado.json
```

En equipos donde el comando disponible sea python, reemplazar py por python.
No se requiere instalar dependencias externas.

## Identificar la versión evaluada

Después de confirmar y subir el último cambio que se quiera entregar:

```bash
git rev-parse HEAD
```

Entregar en el medio indicado por la cátedra:

- El enlace al repositorio publicado.
- El identificador completo que devuelve el comando anterior.

El commit identifica una versión fija aunque luego main avance. No agregar ese
mismo identificador al contenido de un nuevo commit: usarlo en la entrega de EVA
o en el mensaje que acompañe al enlace. La alternativa es una etiqueta de Git,
pero no es necesaria si se entrega el identificador.

## Acceso y reproducción

Mantener el repositorio accesible para la cátedra durante toda la evaluación.
Si es privado, conceder acceso a la cuenta indicada por el profesor.

Para obtener una copia nueva, desde una ubicación donde no exista la carpeta
comparador-nutricional:

```bash
git clone https://github.com/Teo-Martinez/TP_2_PROGRAMACION_ORIENTADA_A_DATOS.git comparador-nutricional
cd comparador-nutricional
py -m unittest discover -s tests -v
```

## Defensa individual

Preparar una demostración breve y explicar problema, simulación, unidades,
limpieza, clases, regex, pruebas y desarrollo registrado en Git. La guía está en
[defensa.md](defensa.md). El formato y las fechas son los de esta materia en EVA.
Si corresponde recuperar la exposición del TP1, preparar también las preguntas
sobre ese trabajo que prevé la consigna.
