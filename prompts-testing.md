Prompt 1

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Estoy empezando con los tests. ¿Cómo puedo crear un test básico para verificar que la clase Board inicia con las fichas en las posiciones correctas?

Respuesta / Resultado de la IA:
Sugirió crear un test con asserts para comparar las posiciones iniciales esperadas con el estado del tablero luego de su inicialización.

Uso: Usado con modificaciones mínimas.

Archivos afectados:

tests/test_board.py

Prompt 2

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Quiero testear que el método is_empty() funcione bien en Board. ¿Qué tipo de casos debería probar?

Respuesta / Resultado de la IA:
Propuso tres escenarios: punto vacío, punto con una ficha, y punto con varias fichas.

Uso: Usado directamente.

Archivos afectados:

tests/test_board.py

Prompt 3

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Necesito asegurarme de que los valores de los dados estén siempre entre 1 y 6. ¿Cómo escribo ese test sin depender del valor aleatorio?

Respuesta / Resultado de la IA:
Recomendó mockear el método random.randint y verificar los límites permitidos.

Uso: Usado con pequeñas adaptaciones.

Archivos afectados:

tests/test_dice.py

Prompt 4

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Estoy probando Game.roll(). ¿Cómo puedo comprobar que cambia el estado interno del juego y actualiza los valores de los dados?

Respuesta / Resultado de la IA:
Sugirió inicializar un juego, llamar roll() y verificar que los valores retornados sean válidos y diferentes del estado anterior.

Uso: Usado completamente.

Archivos afectados:

tests/test_game.py

Prompt 5

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Me gustaría probar el cambio de turno entre jugadores. ¿Cómo puedo hacer que el test valide que se alterna correctamente?

Respuesta / Resultado de la IA:
Indicó testear el atributo __turn_white__ antes y después de aplicar un movimiento.

Uso: Usado sin cambios.

Archivos afectados:

tests/test_game.py

Prompt 6

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Hay líneas de código que no se cubren en los tests, sobre todo cuando un movimiento no es válido. ¿Cómo puedo testear esos casos?

Respuesta / Resultado de la IA:
Recomendó forzar movimientos fuera de rango o desde casillas vacías para generar errores y cubrir esas ramas condicionales.

Uso: Usado con modificaciones menores.

Archivos afectados:

tests/test_game.py

tests/test_board.py

Prompt 7

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Quiero mejorar la organización de los tests. ¿Es mejor agruparlos por clase (TestBoard, TestGame) o por tipo de funcionalidad?

Respuesta / Resultado de la IA:
Recomendó agrupar por clase principal, manteniendo una estructura clara y fácil de mantener.

Uso: Usado completamente.

Archivos afectados:

tests/test_board.py

tests/test_game.py

Prompt 8

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Estoy agregando asserts en varios tests y algunos no se ejecutan. ¿Por qué podría estar pasando y cómo solucionarlo?

Respuesta / Resultado de la IA:
Explicó que Python detiene la ejecución de un test al primer assert fallido, y sugirió dividir los casos en tests separados.

Uso: Usado sin cambios.

Archivos afectados:

tests/test_board.py

tests/test_game.py

Prompt 9

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

El coverage me marca 88% y no sé qué líneas faltan. ¿Hay alguna forma de ver qué código no está cubierto?

Respuesta / Resultado de la IA:
Explicó cómo usar coverage html para generar un informe visual con las líneas sin probar.

Uso: Usado directamente.

Archivos afectados:

tests/ (general)

Prompt 10

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Quiero automatizar los tests para que se ejecuten con cada commit. ¿Cómo puedo integrar eso en mi flujo de trabajo?

Respuesta / Resultado de la IA:
Sugirió agregar un archivo de configuración de CI con ejecución automática de unittest o pytest en cada push al repositorio.

Uso: Usado parcialmente (solo integración local).

Archivos afectados:

.github/workflows/ci.yml (planificado)

tests/