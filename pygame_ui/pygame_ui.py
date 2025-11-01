import sys, os, pygame, random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.board import Board
from core.dice import Dice
from core.player import Player
from core.game import Game

# === COLORES ===
BEIGE = (245, 235, 215)
BROWN_LIGHT = (210, 170, 125)
BROWN_DARK = (110, 75, 50)
BOARD_OUTLINE = (70, 50, 35)
WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
ACCENT = (150, 0, 40)
HEADER_BG = (250, 240, 220)
BUTTON_BG = (240, 210, 175)
BUTTON_HOVER = (255, 235, 200)
BUTTON_BORDER = (90, 65, 45)
SHADOW = (150, 130, 100)
HUD_PANEL_BG = (250, 245, 235)
HUD_PANEL_BORDER = (120, 90, 60)
HUD_HIGHLIGHT = (200, 80, 40)
BOARD_PLAY_BG = (235, 220, 195)
WOOD_STRIPE = (255, 255, 255, 22)
HIGHLIGHT_SELECTED = (255, 210, 90, 160)
HIGHLIGHT_MOVE = (110, 200, 180, 130)
HIGHLIGHT_HOVER_SOURCE = (255, 255, 210, 170)
HIGHLIGHT_HOVER_DEST = (255, 160, 100, 190)

MARGIN = 30
FPS = 60
HUD_WIDTH = 260


# === FUNCIONES DE DIBUJO ===
def draw_triangle(screen, x, y, width, height, color, direction="up"):
    points = (
        [(x, y + height), (x + width // 2, y), (x + width, y + height)]
        if direction == "up"
        else [(x, y), (x + width // 2, y + height), (x + width, y)]
    )
    pygame.draw.polygon(screen, color, points)


def draw_checker(screen, x, y, color, radius=22):
    pygame.draw.circle(screen, SHADOW, (x + 3, y + 3), radius)
    pygame.draw.circle(screen, color, (x, y), radius)
    pygame.draw.circle(screen, (60, 60, 60), (x, y), radius, 1)


def render_board(screen, font, board_width, HEIGHT, HEADER_HEIGHT):
    """Dibuja el tablero con numeración clásica (1–12 abajo, 13–24 arriba)."""
    board_top = HEADER_HEIGHT + MARGIN
    board_height = HEIGHT - HEADER_HEIGHT - 2 * MARGIN
    col_width = (board_width - 2 * MARGIN) // 12
    tri_height = board_height // 2

    pygame.draw.rect(
        screen, BOARD_OUTLINE,
        (MARGIN - 5, board_top - 5, board_width - 2 * (MARGIN - 5), board_height + 10),
        6, border_radius=12
    )

    for i in range(12):
        color = BROWN_DARK if i % 2 == 0 else BROWN_LIGHT
        draw_triangle(screen, MARGIN + i * col_width, board_top, col_width, tri_height, color, "down")
    for i in range(12):
        color = BROWN_LIGHT if i % 2 == 0 else BROWN_DARK
        draw_triangle(screen, MARGIN + i * col_width, board_top + tri_height, col_width, tri_height, color, "up")

    pygame.draw.line(screen, BOARD_OUTLINE, (MARGIN, board_top + tri_height), (board_width - MARGIN, board_top + tri_height), 3)

    # Numeración
    for i in range(12):
        num = font.render(str(24 - i), True, BOARD_OUTLINE)
        screen.blit(num, (MARGIN + (11 - i) * col_width + col_width // 2 - 7, board_top - 25))
    for i in range(12):
        num = font.render(str(i + 1), True, BOARD_OUTLINE)
        screen.blit(num, (MARGIN + i * col_width + col_width // 2 - 7, board_top + board_height + 10))


def draw_button(screen, text, rect, font, mouse_pos):
    hover = rect.collidepoint(mouse_pos)
    color = BUTTON_HOVER if hover else BUTTON_BG
    pygame.draw.rect(screen, SHADOW, rect.move(3, 3), border_radius=10)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, BUTTON_BORDER, rect, 2, border_radius=10)
    txt = font.render(text, True, BUTTON_BORDER)
    screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))


def animate_dice(screen, board_width, HEIGHT, HEADER_HEIGHT, clock, center_x):
    """Animación rápida de dados."""
    font = pygame.font.SysFont("segoeui", 28, bold=True)
    for _ in range(10):
        val1, val2 = random.randint(1, 6), random.randint(1, 6)
        draw_board_background(screen, board_width, HEIGHT, HEADER_HEIGHT)
        render_board(screen, font, board_width, HEIGHT, HEADER_HEIGHT)
        draw_dice(screen, (val1, val2), center_x, HEIGHT - 220)
        pygame.display.flip()
        clock.tick(30)


def draw_dice(screen, dice_values, center_x, y, size=60):
    spacing = 20
    x1 = center_x - size - spacing // 2
    x2 = center_x + spacing // 2
    for x, val in [(x1, dice_values[0]), (x2, dice_values[1])]:
        rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(screen, WHITE, rect, border_radius=8)
        pygame.draw.rect(screen, BUTTON_BORDER, rect, 2, border_radius=8)
        font = pygame.font.SysFont("segoeui", 28, bold=True)
        txt = font.render(str(val), True, BOARD_OUTLINE)
        screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))


def draw_checkers_from_board(screen, board, board_width, HEIGHT, HEADER_HEIGHT):
    board_top = HEADER_HEIGHT + MARGIN
    board_height = HEIGHT - HEADER_HEIGHT - 2 * MARGIN
    col_width = (board_width - 2 * MARGIN) // 12
    radius = 20
    offset_y = 40

    for point in range(24):
        stack = board.get_point(point)
        if point < 12:
            x_center = MARGIN + point * col_width + col_width // 2
            for i, ficha in enumerate(stack):
                y = HEIGHT - MARGIN - offset_y - (i * (radius * 2 + 2))
                color = WHITE if ficha.get_color() == "white" else BLACK
                draw_checker(screen, x_center, y, color)
        else:
            x_center = MARGIN + (23 - point) * col_width + col_width // 2
            for i, ficha in enumerate(stack):
                y = board_top + (i * (radius * 2 + 2)) + offset_y
                color = WHITE if ficha.get_color() == "white" else BLACK
                draw_checker(screen, x_center, y, color)


def point_from_position(pos, board_width, HEIGHT, HEADER_HEIGHT):
    x, y = pos
    if not (MARGIN <= x <= board_width - MARGIN):
        return None

    board_top = HEADER_HEIGHT + MARGIN
    tri_height = (HEIGHT - HEADER_HEIGHT - 2 * MARGIN) // 2
    if tri_height <= 0:
        return None

    col_width = (board_width - 2 * MARGIN) // 12
    if col_width <= 0:
        return None

    if board_top < y < board_top + tri_height:
        index = int((x - MARGIN) // col_width)
        index = max(0, min(11, index))
        return 23 - index
    elif board_top + tri_height < y < HEIGHT - MARGIN:
        index = int((x - MARGIN) // col_width)
        index = max(0, min(11, index))
        return index
    return None


def draw_board_background(screen, board_width, HEIGHT, HEADER_HEIGHT):
    board_area_height = HEIGHT - HEADER_HEIGHT
    pygame.draw.rect(screen, BOARD_PLAY_BG, (0, HEADER_HEIGHT, board_width, board_area_height))
    overlay = pygame.Surface((board_width, board_area_height), pygame.SRCALPHA)
    for i in range(0, board_width, 80):
        pygame.draw.rect(overlay, WOOD_STRIPE, (i, 0, 40, board_area_height))
    screen.blit(overlay, (0, HEADER_HEIGHT))


def draw_point_highlight(screen, point, board_width, HEIGHT, HEADER_HEIGHT, color_rgba):
    board_top = HEADER_HEIGHT + MARGIN
    board_height = HEIGHT - HEADER_HEIGHT - 2 * MARGIN
    col_width = (board_width - 2 * MARGIN) // 12
    tri_height = board_height // 2
    if col_width <= 0 or tri_height <= 0:
        return

    if point is None or point < 0 or point > 23:
        return

    if point < 12:
        x = MARGIN + point * col_width
        y = board_top + tri_height
        surface = pygame.Surface((col_width, tri_height), pygame.SRCALPHA)
        pygame.draw.polygon(surface, color_rgba, [(0, tri_height), (col_width // 2, 0), (col_width, tri_height)])
        screen.blit(surface, (x, y))
    else:
        x = MARGIN + (23 - point) * col_width
        y = board_top
        surface = pygame.Surface((col_width, tri_height), pygame.SRCALPHA)
        pygame.draw.polygon(surface, color_rgba, [(0, 0), (col_width // 2, tri_height), (col_width, 0)])
        screen.blit(surface, (x, y))


def draw_highlights(screen, board_width, HEIGHT, HEADER_HEIGHT, selected_point, destinations):
    if selected_point is not None and selected_point >= 0:
        draw_point_highlight(screen, selected_point, board_width, HEIGHT, HEADER_HEIGHT, HIGHLIGHT_SELECTED)

    for dest in destinations:
        draw_point_highlight(screen, dest, board_width, HEIGHT, HEADER_HEIGHT, HIGHLIGHT_MOVE)


def compute_valid_destinations(game, selected_point):
    moves = game.get_available_moves()
    if not moves:
        return []

    board = game.get_board()
    color = game.current_player().get_color()
    bar_count = board.get_bar_count(color)

    entry_destinations = []
    if bar_count > 0:
        entry_points = range(0, 6) if color == "white" else range(18, 24)
        for dest in entry_points:
            if not board.can_land(dest, color):
                continue
            dist = (dest + 1) if color == "white" else (24 - dest)
            if dist in moves or any(v >= dist for v in moves):
                entry_destinations.append(dest)
        if selected_point is None or selected_point == -1:
            return sorted(entry_destinations)
        return []

    if selected_point is None:
        return []

    stack = board.get_point(selected_point)
    if stack is None or len(stack) == 0 or stack[-1].get_color() != color:
        return []

    destinations = set()
    for move in moves:
        if color == "white":
            dest = selected_point + move
        else:
            dest = selected_point - move
        if 0 <= dest <= 23 and board.can_land(dest, color):
            destinations.add(dest)
        elif dest < 0 or dest > 23:
            if board.all_in_home(color):
                destinations.add(dest)
    return sorted(destinations)


def draw_wrapped_text(screen, font, text, color, x, y, max_width, line_spacing=4):
    words = text.split()
    if not words:
        return y
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line in lines:
        surf = font.render(line, True, color)
        screen.blit(surf, (x, y))
        y += surf.get_height() + line_spacing
    return y


def draw_hud(screen, hud_rect, title_font, text_font, small_font, game, player_white, player_black, current_turn, dice_values):
    board = game.get_board()
    current_player = game.current_player()

    # Fondo del panel con leve sombra
    pygame.draw.rect(screen, SHADOW, hud_rect.move(4, 4), border_radius=18)
    pygame.draw.rect(screen, HUD_PANEL_BG, hud_rect, border_radius=18)
    pygame.draw.rect(screen, HUD_PANEL_BORDER, hud_rect, 2, border_radius=18)

    y = hud_rect.top + 20
    title = title_font.render("Panel de juego", True, HUD_PANEL_BORDER)
    screen.blit(title, (hud_rect.centerx - title.get_width() // 2, y))
    y += title.get_height() + 24

    # Turno actual
    turn_label = text_font.render("Turno actual", True, HUD_HIGHLIGHT)
    screen.blit(turn_label, (hud_rect.left + 24, y))
    y += turn_label.get_height() + 8

    circle_color = WHITE if current_player.get_color() == "white" else BLACK
    pygame.draw.circle(screen, circle_color, (hud_rect.left + 36, y + 10), 10)
    pygame.draw.circle(screen, BUTTON_BORDER, (hud_rect.left + 36, y + 10), 10, 1)
    turn_text = text_font.render(current_turn, True, (60, 35, 20))
    screen.blit(turn_text, (hud_rect.left + 56, y))
    y += turn_text.get_height() + 20

    # Información de dados
    dice_str = "—" if dice_values == (0, 0) else f"{dice_values[0]} y {dice_values[1]}"
    dice_text = text_font.render("Dados:", True, (80, 50, 30))
    screen.blit(dice_text, (hud_rect.left + 24, y))
    dice_value_text = text_font.render(dice_str, True, (80, 50, 30))
    screen.blit(dice_value_text, (hud_rect.left + 24, y + dice_text.get_height()))
    y += dice_text.get_height() + dice_value_text.get_height() + 8

    direction_title = text_font.render("Dirección de juego", True, HUD_HIGHLIGHT)
    screen.blit(direction_title, (hud_rect.left + 24, y))
    y += direction_title.get_height() + 6
    y = draw_wrapped_text(
        screen,
        small_font,
        "◀ Negras: fila inferior hacia la izquierda; fila superior hacia la derecha.",
        (100, 70, 40),
        hud_rect.left + 24,
        y,
        hud_rect.width - 48,
        line_spacing=2
    )
    y += 4
    y = draw_wrapped_text(
        screen,
        small_font,
        "▶ Blancas: fila inferior hacia la derecha; fila superior hacia la izquierda.",
        (100, 70, 40),
        hud_rect.left + 24,
        y,
        hud_rect.width - 48,
        line_spacing=2
    )
    y += 12

    pygame.draw.line(screen, (200, 180, 150), (hud_rect.left + 18, y), (hud_rect.right - 18, y), 2)
    y += 18

    # Estadísticas por jugador
    stats = [
        ("Blancas", player_white, "white"),
        ("Negras", player_black, "black"),
    ]

    for title_txt, player, color in stats:
        title_color = WHITE if color == "white" else BLACK
        pygame.draw.circle(screen, title_color, (hud_rect.left + 32, y + 12), 10)
        pygame.draw.circle(screen, BUTTON_BORDER, (hud_rect.left + 32, y + 12), 10, 1)
        is_active = player.get_name() == current_turn
        text_color = HUD_HIGHLIGHT if is_active else (70, 45, 25)
        name_block = f"{title_txt}: {player.get_name()}"
        y = draw_wrapped_text(
            screen,
            text_font,
            name_block,
            text_color,
            hud_rect.left + 52,
            y,
            hud_rect.width - 70,
            line_spacing=2
        )
        y += 4

        bar_count = board.get_bar_count(color)
        home_count = board.get_home_count(color)
        bar_text = small_font.render(f"• En barra: {bar_count}", True, (100, 80, 60))
        home_text = small_font.render(f"• Fuera: {home_count}", True, (100, 80, 60))
        screen.blit(bar_text, (hud_rect.left + 52, y))
        y += bar_text.get_height() + 2
        screen.blit(home_text, (hud_rect.left + 52, y))
        y += home_text.get_height() + 14


def show_winner(screen, WIDTH, HEIGHT, winner_name):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(180)
    screen.blit(overlay, (0, 0))
    font_big = pygame.font.SysFont("segoeui", 80, bold=True)
    text = font_big.render(f"🏆 ¡{winner_name} GANA!", True, (255, 215, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))
    font_small = pygame.font.SysFont("segoeui", 30)
    subtext = font_small.render("Presiona cualquier tecla para reiniciar", True, WHITE)
    screen.blit(subtext, (WIDTH // 2 - subtext.get_width() // 2, HEIGHT // 2 + 40))
    pygame.display.flip()


# === MAIN ===
def main():
    pygame.init()
    pygame.display.set_caption("Backgammon (Pygame)")
    info = pygame.display.Info()
    WIDTH, HEIGHT = int(info.current_w * 0.9), int(info.current_h * 0.9)
    HEADER_HEIGHT = 160
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoeui", 20, bold=True)
    hud_title_font = pygame.font.SysFont("segoeui", 26, bold=True)
    hud_font = pygame.font.SysFont("segoeui", 20)
    hud_small_font = pygame.font.SysFont("segoeui", 15)

    board = Board()
    dice = Dice()
    player_white = Player("Jugador Blanco", "white")
    player_black = Player("Jugador Negro", "black")
    game = Game(board, dice, player_white, player_black)
    game.start()

    board_width = WIDTH - HUD_WIDTH
    board_center_x = board_width // 2
    hud_rect = pygame.Rect(board_width + 24, HEADER_HEIGHT + 32, HUD_WIDTH - 48, HEIGHT - HEADER_HEIGHT - 64)

    dice_values = (0, 0)
    current_turn = game.current_player().get_name()
    selected_point = None
    message = ""
    winner = None

    btn_width, btn_height = 180, 50
    buttons = {
        "roll": pygame.Rect(board_center_x - btn_width - 20, 40, btn_width, btn_height),
        "new": pygame.Rect(board_center_x + 20, 40, btn_width, btn_height),
    }

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif winner and e.type == pygame.KEYDOWN:
                game.start()
                winner = None
                dice_values = (0, 0)
                current_turn = game.current_player().get_name()
                selected_point = None
                message = "🆕 Nuevo juego iniciado"
            elif e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not winner:
                if buttons["roll"].collidepoint(mouse_pos):
                    animate_dice(screen, board_width, HEIGHT, HEADER_HEIGHT, clock, board_center_x)
                    dice_values = game.roll()
                    current_turn = game.current_player().get_name()
                    selected_point = None
                    if not game.has_any_valid_move():
                        game.end_turn()
                        current_turn = game.current_player().get_name()
                        dice_values = (0, 0)
                        message = f"⛔ Sin movimientos posibles. Turno de {current_turn}"
                    else:
                        message = f"🎲 Dados: {dice_values}"

                elif buttons["new"].collidepoint(mouse_pos):
                    game.start()
                    dice_values = (0, 0)
                    current_turn = game.current_player().get_name()
                    selected_point = None
                    message = "🆕 Nuevo juego iniciado"
                else:
                    point = point_from_position(mouse_pos, board_width, HEIGHT, HEADER_HEIGHT)
                    if point is None:
                        continue
                    color = game.current_player().get_color()
                    bar_count = board.get_bar_count(color)
                    if selected_point is None:
                        if bar_count > 0:
                            success = game.apply_move(-1, point)
                            if success:
                                message = f"✔ Reingresada en punto {point+1}"
                                winner = game.has_winner()
                                if winner:
                                    name = winner.get_name()
                                    message = f"🏆 {name} gana la partida!"
                                elif len(game.get_available_moves()) == 0:
                                    game.end_turn()
                                    current_turn = game.current_player().get_name()
                                    dice_values = (0, 0)
                                    message += f" | 🔄 Turno de {current_turn}"
                                selected_point = None
                            else:
                                message = "❌ No puedes reingresar en ese punto"
                        else:
                            stack = board.get_point(point)
                            if not stack or stack[-1].get_color() != color:
                                message = "❌ Selecciona una ficha propia"
                                continue
                            selected_point = point
                            message = f"Seleccionado punto {point+1}"
                    else:
                        success = game.apply_move(selected_point, point)
                        if success:
                            message = f"✔ Movimiento {selected_point+1} → {point+1}"
                            winner = game.has_winner()
                            if winner:
                                name = winner.get_name()
                                message = f"🏆 {name} gana la partida!"
                            elif len(game.get_available_moves()) == 0:
                                game.end_turn()
                                current_turn = game.current_player().get_name()
                                dice_values = (0, 0)
                                message += f" | 🔄 Turno de {current_turn}"
                            selected_point = None
                        else:
                            message = "❌ Movimiento inválido"
                            selected_point = None

        # === RENDER ===
        screen.fill(BEIGE)
        pygame.draw.rect(screen, HEADER_BG, (0, 0, board_width, HEADER_HEIGHT))
        pygame.draw.rect(screen, HUD_PANEL_BG, (board_width, 0, HUD_WIDTH, HEIGHT))
        draw_board_background(screen, board_width, HEIGHT, HEADER_HEIGHT)
        turn_font = pygame.font.SysFont("segoeui", 30, bold=True)
        turn_text = turn_font.render(f"Turno: {current_turn}", True, (120, 0, 0))
        turn_y = 40 + btn_height + 16
        screen.blit(turn_text, (board_center_x - turn_text.get_width() // 2, turn_y))

        for key, rect in buttons.items():
            draw_button(screen,
                        "🎲 Tirar Dados" if key == "roll" else
                        "🆕 Nuevo Juego",
                        rect, font, mouse_pos)

        render_board(screen, font, board_width, HEIGHT, HEADER_HEIGHT)

        destinations = compute_valid_destinations(game, selected_point if selected_point is not None else (-1 if board.get_bar_count(game.current_player().get_color()) > 0 else None))
        draw_highlights(screen, board_width, HEIGHT, HEADER_HEIGHT, selected_point, destinations)

        hover_point = point_from_position(mouse_pos, board_width, HEIGHT, HEADER_HEIGHT)
        if hover_point is not None:
            color = game.current_player().get_color()
            if selected_point is None:
                if board.get_bar_count(color) > 0:
                    if hover_point in destinations:
                        draw_point_highlight(screen, hover_point, board_width, HEIGHT, HEADER_HEIGHT, HIGHLIGHT_HOVER_DEST)
                else:
                    stack = board.get_point(hover_point)
                    if stack and stack[-1].get_color() == color:
                        draw_point_highlight(screen, hover_point, board_width, HEIGHT, HEADER_HEIGHT, HIGHLIGHT_HOVER_SOURCE)
            elif hover_point in destinations:
                draw_point_highlight(screen, hover_point, board_width, HEIGHT, HEADER_HEIGHT, HIGHLIGHT_HOVER_DEST)

        draw_checkers_from_board(screen, board, board_width, HEIGHT, HEADER_HEIGHT)
        draw_hud(screen, hud_rect, hud_title_font, hud_font, hud_small_font, game, player_white, player_black, current_turn, dice_values)
        if dice_values != (0, 0):
            draw_dice(screen, dice_values, board_center_x, HEIGHT - 220)

        msg_font = pygame.font.SysFont("segoeui", 22)
        draw_wrapped_text(
            screen,
            msg_font,
            message,
            (50, 20, 20),
            MARGIN,
            HEIGHT - 50,
            board_width - 2 * MARGIN,
            line_spacing=2
        )

        if winner:
            show_winner(screen, WIDTH, HEIGHT, winner.get_name())

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
