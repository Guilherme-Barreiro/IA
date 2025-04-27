from sidebar import draw_sidebar
import pygame
import chess
import cairosvg
import chess.svg
from io import BytesIO
from engine import get_best_move
from roboflow_integration import get_detected_board
from ai_move_explainer import explain_move_with_groq

def render_board(board, board_size):
    svg_data = chess.svg.board(board=board, size=board_size)
    png_bytes = cairosvg.svg2png(bytestring=svg_data)
    image = pygame.image.load(BytesIO(png_bytes))
    return pygame.transform.scale(image, (board_size, board_size))

def get_square_from_mouse(pos, board_size):
    square_size = board_size // 8
    x, y = pos
    file = x // square_size
    rank = 7 - (y // square_size)
    return chess.square(file, rank)

def capture_board_from_screen(surface, board_size, save_path="board.png"):
    board_surface = surface.subsurface(pygame.Rect(0, 0, board_size, board_size))
    pygame.image.save(board_surface, save_path)
    print(f"📸 Captured current board as '{save_path}'")

def launch_main_gui(existing_board=None):
    pygame.init()
    pygame.font.init()

    board_size = 720
    sidebar_width = 300
    screen_width = board_size + sidebar_width
    screen = pygame.display.set_mode((screen_width, board_size))
    pygame.display.set_caption("AI Chess Assistant")

    font = pygame.font.SysFont("Arial", 18)
    board = existing_board if existing_board and board.is_valid() else chess.Board()
    surface = render_board(board, board_size)

    selected_square = None
    dragging = False
    moves = []
    explanation = ""
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    running = True
    suggested_move = get_best_move(board)

    if suggested_move:
        move_san = board.san(suggested_move)
        board_fen = board.fen()
        explanation = explain_move_with_groq(move_san, board_fen, "Black")
        print(f"💡 {move_san}: {explanation}")

    while running:
        time_elapsed = (pygame.time.get_ticks() - start_time) // 1000

        screen.fill((0, 0, 0))
        screen.blit(surface, (0, 0))
        draw_sidebar(screen, font, moves, board.turn, time_elapsed, board_size, suggested_move, explanation)

        

        pygame.display.flip()

        image_path = "board.png"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                try:
                    capture_board_from_screen(surface, board_size)
                    detected_board = get_detected_board(image_path)
                    if detected_board and detected_board.is_valid():
                        board = detected_board
                        suggested_move = get_best_move(board)
                        surface = render_board(board, board_size)

                        if suggested_move:
                            move_san = board.san(suggested_move)
                            board_fen = board.fen()
                            explanation = explain_move_with_groq(move_san, board_fen, "Black")
                            print(f"💡 {move_san}: {explanation}")
                        else:
                            explanation = "No valid move."

                        print("✅ Board reanalyzed and updated from image.")
                except Exception as e:
                    print(f"⚠️ Re-detection error: {e}")
                    suggested_move = None
                    explanation = "Move suggestion failed."

            elif event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] < board_size and board.turn == chess.WHITE:
                square = get_square_from_mouse(event.pos, board_size)
                piece = board.piece_at(square)
                if piece and piece.color == chess.WHITE:
                    selected_square = square
                    dragging = True

            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                target_square = get_square_from_mouse(event.pos, board_size)
                move = chess.Move(selected_square, target_square)
                if move in board.legal_moves:
                    move_san = board.san(move)
                    board.push(move)
                    moves.append(f"White: {move_san}")
                    surface = render_board(board, board_size)

                    if board.turn == chess.BLACK:
                        engine_move = get_best_move(board)
                        if engine_move and engine_move in board.legal_moves:
                            engine_move_san = board.san(engine_move)
                            board.push(engine_move)
                            moves.append(f"Black: {engine_move_san}")
                            surface = render_board(board, board_size)

                            board_fen = board.fen()
                            explanation = explain_move_with_groq(engine_move_san, board_fen, "Black")

                selected_square = None
                dragging = False

        clock.tick(60)

    pygame.quit()
