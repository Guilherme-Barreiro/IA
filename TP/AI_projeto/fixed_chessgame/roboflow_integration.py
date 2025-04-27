from ultralytics import YOLO
import chess
import os
from pathlib import Path

# Caminho para o modelo treinado
MODEL_PATH = Path(__file__).resolve().parent.parent / "modelTraining/ChessBoardDetection-2/runs/weights/best.pt"
CONFIDENCE_THRESHOLD = 0.2

# Nomes das classes (index -> label)
LABELS = {
    0: "Bishop_Black", 1: "Bishop_white", 2: "King_black", 3: "King_white",
    4: "Knight_black", 5: "Knight_white", 6: "Pawn_black", 7: "Pawn_white",
    8: "Queen_black", 9: "Queen_white", 10: "Rook_black", 11: "Rook_white"
}

def label_to_symbol(label):
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
    square_size = image_size // 8
    col = int(x_center // square_size)
    row = 7 - int(y_center // square_size)
    col = max(0, min(7, col))
    row = max(0, min(7, row))
    return chess.square(col, row)

def build_board_from_detections(boxes_obj, image_size=720):
    board = chess.Board(None)  # tabuleiro vazio
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
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model not found at {MODEL_PATH}")
        return None

    model = YOLO(str(MODEL_PATH))
    result = model(image_path, conf=CONFIDENCE_THRESHOLD)[0]

    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        print("❌ No detections found.")
        return None

    board = build_board_from_detections(boxes)
    if not board.is_valid():
        print("⚠️ Board built but is not valid.")
        print(board)
        return None

    print("✅ Board built successfully.")
    return board
