Prompt 1

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Estoy por empezar mi proyecto Backgammon en Python. ¿Cómo puedo organizar las carpetas (core, cli, pygame_ui, tests) para mantener la lógica separada y cumplir con buenas prácticas de OOP?

Respuesta / Resultado de la IA:
Propuso una estructura modular con separación entre lógica central y presentación, junto con descripciones de cada carpeta y sus responsabilidades.

Uso: Usado con modificaciones menores en los nombres de carpetas.

Archivos afectados:

core/__init__.py

cli/__init__.py

pygame_ui/__init__.py

Prompt 2

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Estoy creando la clase Board. Necesito representar los 24 puntos del tablero con listas o diccionarios, ¿qué estructura me conviene para poder mover fichas fácilmente?

Respuesta / Resultado de la IA:
Sugirió usar una lista de 24 elementos donde cada índice representa un punto, con listas internas para almacenar las fichas de cada color.

Uso: Usado con modificaciones propias.

Archivos afectados:

core/board.py

Prompt 3

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Me da error de importación circular entre Game y Board. ¿Cómo puedo resolverlo sin romper la arquitectura orientada a objetos?

Respuesta / Resultado de la IA:
Recomendó usar importaciones absolutas (from core.board import Board) y aislar dependencias para evitar referencias cruzadas.

Uso: Usado sin cambios.

Archivos afectados:

core/game.py

core/board.py

Prompt 4

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Quiero que la clase Dice maneje tiradas dobles correctamente. ¿Cómo puedo implementar eso sin repetir código?

Respuesta / Resultado de la IA:
Propuso un método roll() que devuelva una lista con los valores de los dados, duplicando los valores si se obtiene un doble.

Uso: Usado con pequeñas adaptaciones.

Archivos afectados:

core/dice.py

Prompt 5

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Estoy implementando Game.apply_move() y quiero evitar que se muevan fichas de puntos vacíos. ¿Cómo puedo validar eso de forma elegante?

Respuesta / Resultado de la IA:
Sugirió crear un método auxiliar is_empty() dentro de Board para comprobar si un punto está vacío antes de permitir el movimiento.

Uso: Usado directamente.

Archivos afectados:

core/game.py

core/board.py

Prompt 6

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Necesito manejar el cambio de turno entre jugadores. ¿Qué estructura me conviene usar para alternar el turno entre fichas blancas y negras?

Respuesta / Resultado de la IA:
Propuso usar un atributo booleano __turn_white__ en la clase Game que cambie de estado al finalizar cada movimiento.

Uso: Usado sin cambios.

Archivos afectados:

core/game.py

Prompt 7

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Estoy empezando a integrar Pygame. ¿Cómo puedo dibujar el tablero y las fichas respetando las posiciones de Board?

Respuesta / Resultado de la IA:
Sugirió crear funciones de renderizado que lean la información del objeto Board y dibujen cada punto según su contenido.

Uso: Usado con adaptaciones visuales.

Archivos afectados:

pygame_ui/main_pygame.py

Prompt 8

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

No sé cómo capturar clicks en Pygame para mover fichas. ¿Qué función debería usar para detectar los clics del mouse y convertirlos en movimientos válidos?

Respuesta / Resultado de la IA:
Recomendó usar pygame.MOUSEBUTTONDOWN y calcular el punto seleccionado a partir de la posición del clic.

Uso: Usado con modificaciones para ajustar coordenadas.

Archivos afectados:

pygame_ui/main_pygame.py

Prompt 9

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Quiero mejorar la estética del tablero. ¿Cómo puedo usar colores y fuentes personalizadas en Pygame sin que el rendimiento baje?

Respuesta / Resultado de la IA:
Indicó usar variables globales de color, pre-renderizar fuentes y evitar recargar imágenes en cada frame.

Uso: Usado parcialmente.

Archivos afectados:

pygame_ui/main_pygame.py

Prompt 10

Modelo / Herramienta usada: ChatGPT (GPT-5)

Texto del prompt:

Estoy haciendo limpieza de código. ¿Cómo puedo aplicar principios SOLID de forma simple dentro del proyecto Backgammon?

Respuesta / Resultado de la IA:
Explicó cómo dividir responsabilidades, aplicar encapsulamiento y reducir acoplamiento entre Game, Board y Player.

Uso: Usado completamente.

Archivos afectados:

core/game.py

core/player.py

core/board.py