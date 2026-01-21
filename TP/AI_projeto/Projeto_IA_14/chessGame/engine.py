import chess.engine
import os

# Caminho local para o executável do Stockfish
ENGINE_PATH = os.path.join("assets/stockfish", "stockfish")

def get_decent_move(board):
    """
    Calcula um lance razoável utilizando o motor Stockfish com profundidade 2.

    Args:
        board (chess.Board): O estado atual do tabuleiro.

    Returns:
        chess.Move: Um lance calculado pelo motor.
    """
    result = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH).play(board, chess.engine.Limit(depth=2))
    return result.move

def get_good_move(board):
    """
    Calcula um bom lance utilizando profundidade 4 no Stockfish.

    Args:
        board (chess.Board): O estado atual do tabuleiro.

    Returns:
        chess.Move: Um lance melhor avaliado.
    """
    result = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH).play(board, chess.engine.Limit(depth=4))
    return result.move

def get_bad_move(board):
    """
    Calcula um lance fraco usando profundidade 1 (útil para gerar jogadas menos precisas).

    Args:
        board (chess.Board): O estado atual do tabuleiro.

    Returns:
        chess.Move: Um lance calculado rapidamente.
    """
    result = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH).play(board, chess.engine.Limit(depth=1))
    return result.move

def get_best_move(board):
    """
    Calcula o melhor lance possível dentro de 0.1 segundos de tempo de CPU.

    Valida o tabuleiro antes de tentar calcular o lance.

    Args:
        board (chess.Board): O estado atual do tabuleiro.

    Returns:
        chess.Move | None: O melhor lance calculado ou None se inválido ou com erro.
    """
    if not board.is_valid():
        print("Board state is invalid, skipping Stockfish.")
        return None
    if board.king(chess.WHITE) is None or board.king(chess.BLACK) is None:
        print("Missing one or both kings. Cannot calculate best move.")
        return None

    try:
        with chess.engine.SimpleEngine.popen_uci(ENGINE_PATH) as engine:
            result = engine.play(board, chess.engine.Limit(time=0.1))
            return result.move
    except Exception as e:
        print(f"Engine error: {e}")
        return None

def quit_engine():
    """
    Placeholder para encerramento manual do motor, se necessário.
    """
    pass
