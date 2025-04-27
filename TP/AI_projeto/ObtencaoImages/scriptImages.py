import chess
import chess.svg
import cairosvg
import random
import os

def random_board():
    # os.makedirs("images", exist_ok=True)
    os.makedirs("a", exist_ok=True)
    board = chess.Board()
    board.clear_board()
    pieces = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    colors = [chess.WHITE, chess.BLACK]

    for _ in range(random.randint(5, 20)):
        piece = random.choice(pieces)
        color = random.choice(colors)
        square = random.choice(list(chess.SQUARES))
        if board.piece_at(square): continue
        board.set_piece_at(square, chess.Piece(piece, color))

    return board

for i in range(200, 202):
    board = random_board()
    svg = chess.svg.board(board=board)
    # cairosvg.svg2png(bytestring=svg, write_to=f"images/board_{i}.png")
    cairosvg.svg2png(bytestring=svg, write_to=f"a/board_{i}.png")

