import base64
import requests
from PIL import Image, ImageDraw, ImageFont
import chess

image_path = "board.png"
output_image_path = "annotated_debug.png"
API_KEY = "0GZwVsB4wlDoIK7lDggb"
MODEL_ID = "chessboarddetection-m4ei0"
MODEL_VERSION = "5"
CONFIDENCE = 0.3
OVERLAP = 0.3
BOARD_SIZE_PX = 720 

def get_detection_results(image_path):
    """
    Envia uma imagem para o Roboflow e obtém as deteções de peças.

    Args:
        image_path (str): Caminho para a imagem PNG do tabuleiro.

    Returns:
        dict | None: Dicionário com resultados da API ou None em caso de erro.
    """
    print(f"📤 Sending '{image_path}' to Roboflow...")
    url = f"https://detect.roboflow.com/{MODEL_ID}/{MODEL_VERSION}"
    params = {
        "api_key": API_KEY,
        "confidence": CONFIDENCE,
        "overlap": OVERLAP
    }

    with open(image_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode("utf-8")

    resp = requests.post(
        url, params=params, data=encoded_image,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if resp.status_code != 200:
        print(f"Roboflow error: {resp.status_code}, {resp.text}")
        return None

    data = resp.json()
    print(f"Roboflow returned {len(data.get('predictions', []))} detections.")
    return data

def pixel_to_square_label(x_center, y_center):
    """
    Converte coordenadas em pixeis para uma notação de casa (ex: 'e4').

    Args:
        x_center (float): Coordenada X do centro.
        y_center (float): Coordenada Y do centro.

    Returns:
        str: Casa do tabuleiro em notação algebraica (ex: 'g5').
    """
    square_size = BOARD_SIZE_PX // 8
    col = int(x_center // square_size)
    row = int(y_center // square_size)
    row = 7 - row  # Corrigir para coordenadas de xadrez
    col = max(0, min(7, col))
    row = max(0, min(7, row))
    return chess.square_name(chess.square(col, row))

def annotate_with_squares(image_path, predictions, output_path):
    """
    Desenha anotações visuais (caixas e etiquetas) sobre uma imagem de tabuleiro.

    Args:
        image_path (str): Caminho para a imagem original.
        predictions (list[dict]): Lista de deteções da API Roboflow.
        output_path (str): Caminho para guardar a imagem anotada.
    """
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        font = ImageFont.load_default()

    for pred in predictions:
        x = pred["x"]
        y = pred["y"]
        w = pred["width"]
        h = pred["height"]
        label = pred["class"]
        conf = pred["confidence"]
        square = pixel_to_square_label(x, y)

        x0 = x - w / 2
        y0 = y - h / 2
        x1 = x + w / 2
        y1 = y + h / 2

        draw.rectangle([x0, y0, x1, y1], outline="red", width=2)
        draw.text((x0, y0 - 12), f"{label} @ {square}", fill="red", font=font)

    image.save(output_path)
    print(f"Annotated debug image saved to: {output_path}")

if __name__ == "__main__":
    data = get_detection_results(image_path)
    if data and "predictions" in data:
        annotate_with_squares(image_path, data["predictions"], output_image_path)
