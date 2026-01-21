import base64
import requests
from PIL import Image, ImageDraw, ImageFont

image_path = "board.png"
model_id = "chessboarddetection-m4ei0"
model_version = "5"
api_key = "0GZwVsB4wlDoIK7lDggb"
confidence = 0.3
overlap = 0.3

url = f"https://detect.roboflow.com/{model_id}/{model_version}"
params = {
    "api_key": api_key,
    "confidence": confidence,
    "overlap": overlap
}

def send_image(image_path, url, params):
    """
    Envia uma imagem codificada para a API do Roboflow.

    Args:
        image_path (str): Caminho para a imagem PNG.
        url (str): URL da API Roboflow.
        params (dict): Parâmetros da requisição (API key, confiança, overlap).

    Returns:
        dict | None: Resposta JSON com as previsões ou None se falhar.
    """
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    response = requests.post(
        url,
        params=params,
        data=encoded_image,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if response.status_code == 200:
        print("Inference successful. Processing results...")
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def annotate_predictions(image_path, predictions, output_path="annotated_image.png"):
    """
    Desenha bounding boxes e rótulos sobre a imagem original com base nas previsões.

    Args:
        image_path (str): Caminho da imagem original.
        predictions (list[dict]): Lista de previsões da API Roboflow.
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

        x0 = x - w / 2
        y0 = y - h / 2
        x1 = x + w / 2
        y1 = y + h / 2

        draw.rectangle([x0, y0, x1, y1], outline="red", width=2)
        draw.text((x0, y0 - 10), label, fill="red", font=font)

    image.save(output_path)
    print(f"Annotated image saved as {output_path}")

if __name__ == "__main__":
    result = send_image(image_path, url, params)
    if result and "predictions" in result:
        annotate_predictions(image_path, result["predictions"])
