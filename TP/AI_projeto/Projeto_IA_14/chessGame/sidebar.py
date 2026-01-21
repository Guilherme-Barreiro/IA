import pygame
import chess

SIDEBAR_BG = (46, 46, 46)
TEXT_COLOR = (240, 240, 240)
HIGHLIGHT_COLOR = (102, 255, 178)
EXPLANATION_COLOR = (255, 255, 153)
LINE_COLOR = (80, 80, 80)
BORDER_RADIUS = 12

PIECE_UNICODE = {
    "N": "♞", "B": "♝", "R": "♜", "Q": "♛", "K": "♚", "P": "♟",
    "n": "♘", "b": "♗", "r": "♖", "q": "♕", "k": "♔", "p": "♙"
}

def draw_sidebar(screen, font, moves, turn, time_elapsed, board_size, suggested_move, explanation=""):
    """
    Desenha a barra lateral com informações do jogo, sugestões e explicações.

    Args:
        screen (pygame.Surface): Superfície principal da aplicação.
        font (pygame.font.Font): Fonte a usar para o texto.
        moves (list[str]): Lista dos últimos lances efetuados.
        turn (bool): Indica de quem é o turno (True = White, False = Black).
        time_elapsed (int): Tempo de jogo em segundos.
        board_size (int): Tamanho do tabuleiro.
        suggested_move (chess.Move): Lance sugerido pelo motor.
        explanation (str, optional): Texto explicativo sobre o lance sugerido.
    """
    x_offset = board_size + 10
    width = 280
    height = screen.get_height() - 20

    sidebar_rect = pygame.Rect(x_offset - 5, 5, width, height)
    pygame.draw.rect(screen, SIDEBAR_BG, sidebar_rect, border_radius=BORDER_RADIUS)

    y = 20

    def draw_line():
        nonlocal y
        pygame.draw.line(screen, LINE_COLOR, (x_offset, y), (x_offset + width - 20, y), 1)
        y += 10

    screen.blit(font.render(f"Turn: {'White' if turn else 'Black'}", True, TEXT_COLOR), (x_offset, y))
    y += 30
    screen.blit(font.render(f"Time: {time_elapsed}s", True, TEXT_COLOR), (x_offset, y))
    y += 30
    draw_line()

    screen.blit(font.render("Moves:", True, TEXT_COLOR), (x_offset, y))
    y += 25
    for move in moves[-10:]:
        screen.blit(font.render(move, True, (200, 200, 200)), (x_offset, y))
        y += 20

    y += 10
    draw_line()

    screen.blit(font.render("Suggested Move:", True, TEXT_COLOR), (x_offset, y))
    y += 25
    if suggested_move:
        move_san = str(suggested_move)
        move_uci = suggested_move.uci()
        piece_symbol = PIECE_UNICODE.get(move_san[0], "") if len(move_san) > 1 else "•"
        uci_text = f"{piece_symbol} {move_uci[:2]} → {move_uci[2:]}"
        move_box = pygame.Rect(x_offset, y, 200, 28)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, move_box, border_radius=8)
        screen.blit(font.render(uci_text, True, (0, 0, 0)), (x_offset + 8, y + 5))
        y += 40

    y += 10
    draw_line()

    screen.blit(font.render("Why this move?", True, EXPLANATION_COLOR), (x_offset, y))
    y += 25
    for line in wrap_text(explanation, font, width - 20):
        screen.blit(font.render(line, True, TEXT_COLOR), (x_offset, y))
        y += 20

    hint_text = "Press SPACE to Re-Analyze Board"
    hint_font = pygame.font.SysFont("Arial", 15, bold=True)

    hint_box = pygame.Rect(x_offset, screen.get_height() - 55, width - 10, 40)
    pygame.draw.rect(screen, (102, 255, 178), hint_box, border_radius=10)
    pygame.draw.rect(screen, (40, 40, 40), hint_box, width=2, border_radius=10)

    text_surface = hint_font.render(hint_text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=hint_box.center)
    screen.blit(text_surface, text_rect)

def wrap_text(text, font, max_width):
    """
    Quebra uma string longa em várias linhas para caber na sidebar.

    Args:
        text (str): Texto completo a ser quebrado.
        font (pygame.font.Font): Fonte usada para medir o tamanho.
        max_width (int): Largura máxima da linha.

    Returns:
        list[str]: Lista de linhas formatadas.
    """
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test_line = current + word + " "
        if font.size(test_line)[0] <= max_width:
            current = test_line
        else:
            lines.append(current.strip())
            current = word + " "
    lines.append(current.strip())
    return lines
