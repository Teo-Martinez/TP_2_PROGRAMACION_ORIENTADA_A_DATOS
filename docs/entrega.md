# Entrega y publicación

Este es un proyecto nuevo, desarrollado ahora con Git local desde la definición
inicial. No es la rama reconstruida del proyecto anterior. El historial conserva
fechas actuales y autoría técnica Codex (asistente), sin atribuir acciones de Git
al estudiante. Teo Martinez figura como autor académico. Revisá las reglas de la
cátedra sobre asistencia y asegurate de poder explicar cada parte.

## Comprobar el historial

Descomprimir el ZIP en una carpeta nueva. Conservar .git. No superponerlo sobre
el repositorio anterior. Desde comparador-nutricional:

```bash
git status
git log --oneline --reverse
python -m unittest discover -s tests -v
```

Cada commit incorpora trabajo de su etapa con verificaciones disponibles en ese
momento: alcance, simulación, lectores, modelo, limpieza, consultas, consola y
verificación integral/documentación. El primer commit no incluye código terminado.

## Subir sin mezclar historiales

Crear un repositorio nuevo y completamente vacío en GitHub (sin README, licencia
ni gitignore inicial). Reemplazar URL_NUEVA por la URL real, no usar ese marcador
literalmente:

```bash
git remote add origin URL_NUEVA
git push -u origin main
```

No se publicó desde este entorno. El repositorio anterior sigue intacto. No usar
push forzado para sustituirlo sin decidir expresamente qué historial conservar.

Si se exige usar exactamente la URL anterior, primero hay que acordar cómo se
conserva el trabajo ya publicado. No importar la rama desarrollo reconstruida
sobre esta implementación nueva.

## Identificar la versión entregada

```bash
git rev-parse HEAD
```

Entregar enlace y commit, con acceso público o concedido a la cátedra.
Para nuevos commits propios, configurar tu nombre y correo reales en Git,
revisar git status y git diff y probar antes de confirmar.
