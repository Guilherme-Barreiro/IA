from ultralytics import YOLO
import chess
import os
from pathlib import Path

MODEL_NAME = "best_NoDataAgm.pt"
MODEL_PATH = Path(__file__).resolve().parent / "assets/models" / MODEL_NAME
CONFIDENCE_THRESHOLD = 0.2

LABELS = {
    0: "Bishop_Black", 1: "Bishop_white", 2: "King_black", 3: "King_white",
    4: "Knight_black", 5: "Knight_white", 6: "Pawn_black", 7: "Pawn_white",
    8: "Queen_black", 9: "Queen_white", 10: "Rook_black", 11: "Rook_white"
}

def label_to_symbol(label):
    """
    Converte um rótulo YOLO em um símbolo FEN para xadrez.

    Args:
        label (str): Nome da peça no formato "Piece_Color" (ex: "Knight_white").

    Returns:
        str | None: Símbolo FEN correspondente ou None se inválido.
    """
    try:
        piece_str, color_str = label.split('_', 1)
    except ValueError:
        return None

    letter_map = {
        "pawn":   "p", "knight": "n", "bishop": "b",
        "rook":   "r", "queen": "q", "king": "k"
    }
    piece_letter = letter_map.get(piece_str.lower())
    return piece_letter.upper() if color_str.lower() == "white" else piece_letter.lower()

def pixel_to_square(x_center, y_center, image_size=720):
    """
    Converte coordenadas em pixeis para uma casa do tabuleiro.

    Args:
        x_center (float): Coordenada X do centro da peça.
        y_center (float): Coordenada Y do centro da peça.
        image_size (int): Tamanho total da imagem (default 720).

    Returns:
        int: Índice da casa no formato `chess.square()`.
    """
    square_size = image_size // 8
    col = int(x_center // square_size)
    row = 7 - int(y_center // square_size)
    col = max(0, min(7, col))
    row = max(0, min(7, row))
    return chess.square(col, row)

def build_board_from_detections(boxes_obj, image_size=720):
    """
    Constrói um tabuleiro de xadrez a partir das deteções YOLO.

    Args:
        boxes_obj: Objeto com as bounding boxes e classes do modelo.
        image_size (int): Tamanho da imagem original (default 720).

    Returns:
        chess.Board: Objeto do tabuleiro com as peças detetadas.
    """
    board = chess.Board(None)  # Cria um tabuleiro vazio
    for i in range(len(boxes_obj)):
        conf = boxes_obj.conf[i].item()
        if conf < CONFIDENCE_THRESHOLD:
            continue

        cls_id = int(boxes_obj.cls[i].item())
        label = LABELS.get(cls_id)
        x_center, y_center = boxes_obj.xywh[i][:2].tolist()

        symbol = label_to_symbol(label)
        if symbol:
            square = pixel_to_square(x_center, y_center, image_size)
            board.set_piece_at(square, chess.Piece.from_symbol(symbol))
    return board

def get_detected_board(image_path):
    """
    Processa uma imagem para obter um tabuleiro detetado com peças YOLO.

    Args:
        image_path (str): Caminho para a imagem PNG do tabuleiro.

    Returns:
        chess.Board | None: Tabuleiro detetado ou None se inválido ou sem deteções.
    """
    if not os.path.exists(MODEL_PATH):
        print(f"Model not found at {MODEL_PATH}")
        return None

    model = YOLO(str(MODEL_PATH))
    result = model(image_path, conf=CONFIDENCE_THRESHOLD)[0]

    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        print("No detections found.")
        return None

    board = build_board_from_detections(boxes)
    if not board.is_valid():
        print("Board built but is not valid.")
        print(board)
        return None

    print("Board built successfully.")
    return board
