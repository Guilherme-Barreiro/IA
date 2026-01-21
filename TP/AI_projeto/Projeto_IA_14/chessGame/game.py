import chess
from engine import get_best_move

def print_board(board):
    """
    Imprime o estado atual do tabuleiro de xadrez.

    Args:
        board (chess.Board): O objeto tabuleiro do jogo.
    """
    print(board)

def player_move(board):
    """
    Solicita ao jogador que introduza um lance e atualiza o tabuleiro se o lance for válido.

    Args:
        board (chess.Board): O objeto tabuleiro a ser atualizado.
    """
    move_uci = input("Your move (in UCI format, e.g., e2e4): ")
    try:
        move = chess.Move.from_uci(move_uci)
        if move in board.legal_moves:
            board.push(move)
        else:
            print("Illegal move. Try again.")
            player_move(board)
    except ValueError:
        print("Invalid move format. Use UCI format, e.g., e2e4.")
        player_move(board)

def engine_move(board):
    """
    Obtém o melhor lance do motor de xadrez e atualiza o tabuleiro.

    Args:
        board (chess.Board): O objeto tabuleiro a ser atualizado.
    """
    move = get_best_move(board)
    if move:
        board.push(move)
        print(f"Engine plays: {move}")
    else:
        print("Engine could not determine a move.")

def play_game():
    """
    Controla o ciclo principal do jogo entre o jogador e o motor.

    Corre até o jogo terminar (checkmate, empate, etc).
    """
    board = chess.Board()
    while not board.is_game_over():
        print_board(board)
        player_move(board)
        if board.is_game_over():
            break
        engine_move(board)
    print_board(board)
    print("Game over.")
