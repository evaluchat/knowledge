---
type: Concept
id: essays-workflow
lang: es
origin: translation
status: stable
title: 'Flujo de trabajo de ensayos — desbloqueo proporcional de la redacción'
title_local: 'Flujo de trabajo de ensayos — desbloqueo proporcional de la redacción'
description: 'Cómo la función de ensayos de Evaluchat condiciona el soporte de redacción a la contribución dialógica previa (CAMDLE), según lo implementado en Canvas.'
tags: [evaluchat, essays, canvas, camdle, teaching-prototype]
applies_to: 0.5.9
sources:
  - id: camdle-theory
    resource: https://github.com/evaluchat/research/blob/main/theory/camdle.en.md
    title: 'CAMDLE — research question and theory (unproven)'
  - id: threshold-calibration
    resource: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
    title: 'Threshold calibration — research question (open)'
  - id: white-paper
    resource: https://docs.evaluchat.com/research/camdle-white-paper.pdf
    title: 'CAMDLE white paper'
generated:
  by: opencode-go/deepseek-v4-flash
  at: 2026-08-09T14:00:00Z
---

> Este es el source of truth de implementación para el flujo de ensayos / CAMDLE que selecciona el método **ai-assisted-essay** — véase [research-method](research-method.en.md).

# Flujo de trabajo de ensayos — desbloqueo proporcional de la redacción

> **Se aplica a:** Canvas apps/web **0.5.9** (línea de desarrollo), el prototipo de enseñanza de Evaluchat construido sobre el fork de open-canvas. Este concepto documenta la función de ensayos tal como se distribuye en esa versión.

## Visión general

El flujo de trabajo de ensayos es la experiencia de escritura de Evaluchat orientada al estudiante: un chat de IA restringido combinado con un lienzo de redacción. Los estudiantes trabajan en una interfaz de pantalla dividida — un panel de diálogo junto a un documento Markdown editable — que imita deliberadamente los hábitos de interacción de las herramientas de IA de consumo. Es una experiencia familiar, conversacional e impulsada por indicaciones, no un navegador de examen bloqueado.

La restricción central: el modelo no puede generar la asignación completa a partir de una sola indicación. El soporte de redacción se libera de forma condicional, después de que el estudiante haya aportado suficientes ideas, evidencia, preguntas y lenguaje a través del diálogo — el diseño CAMDLE (véase [camdle-theory]). El flujo de trabajo mantiene el trabajo conceptual y lingüístico del estudiante visible y relevante: lo que el estudiante hace en el diálogo determina qué asistencia queda disponible.

## Fases de la sesión

Una sesión avanza por tres fases, controladas en tiempo de ejecución por un valor `phase_state`: `socratic`, `drafting`, `defense`.

### Fase 1 — Puerta socrática

La IA entrevista al estudiante para establecer su comprensión antes de que cualquier texto del ensayo llegue al lienzo. Las peticiones directas de «escríbeme el ensayo» se rechazan; en su lugar, el asistente extrae la intuición inicial del estudiante y la convierte en una tesis estructurada. Tras cada turno, el asistente evalúa la tesis (`assessThesis`); cuando la contribución es suficiente, `phase_state` pasa a `drafting` y la asistencia de redacción queda disponible.

### Fase 2 — Co-creación con hitos

En la fase de redacción, el estudiante trabaja en el lienzo de pantalla dividida con la IA actuando como editor de desarrollo, no como escritor fantasma. El documento registra una línea de tiempo de revisiones («ADN del documento») que distingue el contenido escrito por el estudiante de las ediciones sugeridas por la IA, de modo que quién aportó qué permanece visible. Una vez que existe suficiente material de tesis, la IA puede redactar el texto introductorio o secciones hito en el lienzo para que el estudiante las revise, acepte o modifique.

### Fase 3 — Defensa (viva)

Antes de la entrega, la IA cuestiona un argumento clave del ensayo del estudiante — una defensa de abogado del diablo basada en el chat. La entrega solo se desbloquea después de que el estudiante haya defendido con éxito el argumento.

## Reglas de sesión y asignación

- Una sesión activa por estudiante y asignación.
- Estados de sesión: `not_started`, `in_progress`, `submitted`, `abandoned`.
- La selección del hilo activo prefiere el hilo incompleto no abandonado; después, el hilo entregado no abandonado; los hilos abandonados se omiten. Abrir una asignación se adjunta a ese hilo en lugar de crear duplicados.
- `/student` lista las asignaciones del estudiante con acciones según su estado (reanudar, revisar, empezar).

Las asignaciones se resuelven a partir de dos fuentes:

1. **Asignaciones personalizadas** — asignaciones propiedad del docente, creadas y listadas en el lado del profesor y asignadas a estudiantes concretos.
2. **Catálogo de semillas** — plantillas iniciales compartidas que se cargan en tiempo de ejecución desde un archivo JSON (`data/teaching/seed-assignments.json`), no incrustadas en el paquete de la aplicación. Las semillas aparecen en `/student` solo cuando están registradas para ese estudiante.

## Evidencia de proceso

Un agregador de seguimiento del lado del cliente recoge señales de proceso y emite eventos `session_summary` compactos (~300 bytes) periódicamente y al cerrar la sesión — no tráfico API por cada pulsación de tecla. Los resúmenes incluyen:

- pulsaciones de teclas y ráfagas de escritura (grupos de pulsaciones muy próximas, recuento de palabras y duración de las ráfagas)
- eventos de pegar, copiar y cortar (volumen de pegado, contenido copiado o cortado)
- ediciones del lienzo (inserciones, eliminaciones, reemplazos)
- recuentos de foco y desenfoque, eventos de visibilidad oculta

Los docentes lo ven como **Métricas de participación** en la vista de entrega. Una proporción alta de pegado (p. ej., más de ~30 % pegado) puede aparecer como una insignia descriptiva — un punto de partida para la conversación, no un veredicto.

**Límite: la evidencia de proceso no es detección de autoría.** Son observaciones mecánicas sobre cómo se construyó el trabajo; no demuestran quién escribió una frase ni si hubo aprendizaje. Evaluchat no produce ninguna puntuación de integridad, ni marca de «trampa», ni ningún veredicto automatizado de integridad. Las señales son contexto para el juicio humano: los docentes las leen junto con la transcripción, el borrador y el contexto de la asignación, y deciden si hay algo que merezca la pena comentar con el estudiante. Métricas de participación, no indicadores de integridad; señales de proceso, no indicadores de trampa. El producto no realiza supervisión (sin cámara web, bloqueo del sistema ni grabación de pantalla) y no puede detectar comportamientos fuera del dispositivo o mediados, como volver a teclear, el dictado, las notas en papel o la asistencia desde un segundo dispositivo.

## Andamiaje proporcional y umbral de desbloqueo

El soporte de redacción se libera de forma condicional según la contribución dialógica — andamiaje proporcional. La cantidad de contribución necesaria para desbloquear la asistencia (el umbral) es una **variable empírica**, no un valor establecido: qué cuenta como contribución suficiente y cómo varía según el tipo de tarea, el nivel de competencia, la lengua de origen y la estrategia del alumno es una pregunta de investigación abierta ([threshold-calibration]). El propósito del mecanismo es exigir tiempo e interacción con el material antes de que se desbloquee la generación; si eso produce resultados de aprendizaje es una hipótesis en investigación, no una afirmación de producto.

## Estado y versionado

Este concepto fija `applies_to: 0.5.9` — la versión de Canvas apps/web en la línea de desarrollo en el momento de redactarse (0.5.8 era el despliegue de producción). Describe el comportamiento tal como se distribuye en esa versión; las versiones más recientes pueden cambiar el comportamiento. Considere este concepto **obsoleto** una vez que la versión fijada quede superada por una versión más reciente que cambie el comportamiento aquí descrito.

Cuando la versión fijada quede superada, actualice este concepto mediante una pull request al repositorio de conocimiento: actualice `applies_to` a la nueva versión, ajuste el cuerpo para reflejar el comportamiento más reciente y anote el cambio. Mantenga `status: stable` solo mientras la descripción coincida con una versión distribuida.

[camdle-theory]: https://github.com/evaluchat/research/blob/main/theory/camdle.en.md
[threshold-calibration]: https://github.com/evaluchat/research/blob/main/theory/threshold-calibration.en.md
