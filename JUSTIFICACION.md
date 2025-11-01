El proyecto Backgammon fue desarrollado en Python 3 aplicando los principios del paradigma orientado a objetos (OOP).
La arquitectura está dividida en módulos independientes que separan la lógica central del juego (carpeta core/) de las interfaces de usuario (cli/ y pygame_ui/).

Esta separación garantiza que la funcionalidad principal del juego no dependa de la interfaz, permitiendo mantener el código modular, reutilizable y fácil de extender.

🧱 Justificación de las Clases

Game:
Coordina el flujo general del juego. Administra turnos, tiradas de dados, movimientos válidos y condición de victoria.
Es la clase principal que conecta Board, Dice y Player.

Board:
Representa el tablero con sus 24 puntos. Gestiona la posición de las fichas, los movimientos válidos y las reglas de reingreso desde la barra.
Incluye métodos auxiliares como is_empty() para verificar casillas vacías.

Player:
Representa a cada jugador, almacenando color, fichas y estado de turno.
Contiene métodos para validar jugadas y actualizar su estado durante la partida.

Dice:
Modela los dos dados de seis caras.
Contiene el método roll() y maneja la lógica de tiradas dobles o repetidas según las reglas del Backgammon.

Checker:
Representa una ficha individual del tablero.
Se usa internamente en Board para gestionar la cantidad y el color de las fichas en cada punto.

CLI:
Implementa una interfaz textual que permite jugar desde la consola.
Fue desarrollada para garantizar accesibilidad en entornos sin soporte gráfico.

PygameUI:
Implementa la interfaz visual del juego, utilizando la biblioteca Pygame.
Presenta tablero, fichas y botones, manteniendo sincronía con la lógica interna del core.

⚙️ Justificación de los Atributos

Todos los atributos siguen la convención exigida por la consigna:
__atributo__, con prefijo y sufijo de doble guion bajo.
Esto asegura encapsulamiento y claridad de lectura.

Cada clase contiene únicamente los atributos necesarios para cumplir su responsabilidad, evitando duplicaciones o dependencias innecesarias.

Ejemplos:

Game: __board__, __dice__, __white__, __black__, __available__, __turn_white__

Player: __color__, __checkers__

Dice: __values__

Board: __points__, __bar__, __home__

🧠 Decisiones de Diseño Relevantes

Separación de capas:
Se decidió aislar la lógica (core/) de la presentación (cli/ y pygame_ui/), para cumplir el principio de independencia entre módulos.

Diseño modular:
Cada clase tiene una única responsabilidad bien definida, cumpliendo el principio SRP (Single Responsibility).

Simplicidad del flujo de juego:
Game centraliza el manejo de turnos, evitando duplicar lógica en Player o Board.

Pruebas unitarias exhaustivas:
Se desarrollaron tests para todas las clases, garantizando un comportamiento predecible y estable.

Diseño extendible:
Se dejó preparada la estructura para incluir almacenamiento en Redis (opcional según el PDF) sin alterar la arquitectura principal.

⚠️ Excepciones y Manejo de Errores

Se implementaron validaciones internas para movimientos inválidos, posiciones fuera de rango y tiradas incorrectas.

Los errores se manejan mediante excepciones personalizadas y mensajes descriptivos que facilitan el debugging.

El flujo de errores sigue una jerarquía clara:

InvalidMoveError

InvalidDiceError

OutOfRangeError

🧪 Estrategia de Testing y Cobertura

Las pruebas unitarias fueron desarrolladas con el módulo estándar unittest.
Se diseñaron tests para cada clase, cubriendo casos normales, excepciones y límites.

El objetivo fue alcanzar una cobertura total superior al 90%, utilizando la herramienta Coverage.py.
Los tests se ejecutan automáticamente en cada commit mediante integración continua (CI) y se organizan por módulos dentro de la carpeta tests/.

Ejemplos de casos testeados:

Tiradas válidas y dobles (Dice).

Movimientos y reingresos desde la barra (Board).

Cambios de turno (Game).

Estados de victoria (Player).

🧩 Principios SOLID Aplicados

S - Single Responsibility: cada clase cumple un rol único (ej. Game coordina, Board gestiona el tablero).

O - Open/Closed: las clases están abiertas a extensión pero cerradas a modificación.

L - Liskov Substitution: todas las clases pueden reemplazarse por subtipos sin alterar el funcionamiento.

I - Interface Segregation: separación clara entre lógica del juego y presentación.

D - Dependency Inversion: las capas superiores (CLI, PygameUI) dependen de abstracciones, no de implementaciones concretas.

Nazareno Masetto
Backgammon – Computación 2025
Universidad de Mendoza – Facultad de Ingeniería