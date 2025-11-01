NAZARENO MASETTO

El proyecto Backgammon consiste en la implementación completa del clásico juego de mesa, desarrollado en Python 3 aplicando el paradigma de Programación Orientada a Objetos (OOP).

El sistema permite jugar partidas de Backgammon en dos modalidades:

Modo Testing: para la ejecución de pruebas unitarias y validación de la lógica central del juego.

Modo Juego: disponible tanto en una interfaz de línea de comandos (CLI) como en una interfaz gráfica desarrollada con Pygame.

El diseño separa completamente la lógica del juego (core) de las interfaces de usuario, garantizando modularidad, mantenibilidad y coherencia con los principios SOLID.

🧪 Modo Testing

El modo testing permite verificar el correcto funcionamiento de todas las clases y métodos que componen la lógica del juego.
Se ejecutan pruebas unitarias sobre los módulos principales (Board, Dice, Player, Game, etc.) para asegurar que las reglas del Backgammon se cumplan correctamente.

Además, se mide la cobertura de código, la cual debe superar el 90%, requisito establecido en la consigna oficial del proyecto.

🕹️ Modo Juego

El Backgammon puede jugarse de dos formas:

Interfaz CLI (línea de comandos):
Permite jugar desde la terminal, visualizando los movimientos y turnos mediante texto.

Interfaz Gráfica (Pygame):
Ofrece una experiencia visual completa, con tablero, fichas y dados representados gráficamente.
El jugador puede interactuar con el mouse y el teclado, manteniendo las mismas reglas de juego que en la versión CLI.

Ambas modalidades comparten la misma lógica central, lo que garantiza un comportamiento idéntico y coherente entre ellas.

🐳 Ejecución con Docker

El proyecto puede desplegarse y ejecutarse dentro de un contenedor Docker.
Esto asegura que las pruebas y el juego puedan ejecutarse en cualquier entorno sin conflictos de dependencias.

Se incluyen configuraciones para:

Modo Testing: ejecución de todos los tests automatizados dentro del contenedor.

Modo Juego CLI: ejecución interactiva desde consola.

Modo Juego Pygame: ejecución gráfica (en sistemas que admitan entorno visual).

📁 Estructura del Proyecto

backgammon/
├── core/                # Lógica central del juego
├── cli/                 # Interfaz de línea de comandos
├── pygame_ui/           # Interfaz gráfica (Pygame)
├── tests/               # Pruebas unitarias
├── assets/              # Recursos del juego (imágenes, sonidos, fuentes)
├── Dockerfile           # Configuración Docker
├── requirements.txt     # Dependencias del proyecto
├── CHANGELOG.md
├── JUSTIFICACION.md
└── prompts-desarrollo.md / prompts-testing.md / prompts-documentacion.md
