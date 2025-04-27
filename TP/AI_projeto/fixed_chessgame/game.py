import chess
from engine import get_best_move

def print_board(board):
    """
    Prints the current state of the board.
    """
    print(board)

def player_move(board):
    """
    Handles the player's move input and updates the board.
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
    Gets the engine's best move and updates the board.
    """
    move = get_best_move(board)
    if move:
        board.push(move)
        print(f"Engine plays: {move}")
    else:
        print("Engine could not determine a move.")

def play_game():
    """
    Manages the game loop.
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
