import chess.engine
import os

ENGINE_PATH = os.path.join("assets/stockfish_WIN", "stockfish")
# ENGINE_PATH = os.path.join("assets/stockfish_MAC", "stockfish")

def get_decent_move(board):
    result = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH).play(board, chess.engine.Limit(depth=2))
    return result.move

def get_good_move(board):
    result = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH).play(board, chess.engine.Limit(depth=4))
    return result.move

def get_bad_move(board):
    result = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH).play(board, chess.engine.Limit(depth=1))
    return result.move

def get_best_move(board):
    if not board.is_valid():
        print("⚠️ Board state is invalid, skipping Stockfish.")
        return None
    if board.king(chess.WHITE) is None or board.king(chess.BLACK) is None:
        print("⚠️ Missing one or both kings. Cannot calculate best move.")
        return None

    try:
        with chess.engine.SimpleEngine.popen_uci(ENGINE_PATH) as engine:
            result = engine.play(board, chess.engine.Limit(time=0.1))
            return result.move
    except Exception as e:
        print(f"❌ Engine error: {e}")
        return None

def quit_engine():
    pass 
