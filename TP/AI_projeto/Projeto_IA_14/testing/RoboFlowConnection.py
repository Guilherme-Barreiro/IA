import base64
import requests

image_path = "board.png"
model_id = "chessboarddetection-m4ei0"
model_version = "2"
api_key = "0GZwVsB4wlDoIK7lDggb"
confidence = 0.6
overlap = 0.3

url = f"https://detect.roboflow.com/{model_id}/{model_version}"
params = {
    "api_key": api_key,
    "confidence": confidence,
    "overlap": overlap
}

def send_image_to_roboflow(image_path, url, params):
    """
    Envia uma imagem codificada em base64 para a API Roboflow e devolve o JSON com os resultados.

    Args:
        image_path (str): Caminho para a imagem (formato PNG ou JPG).
        url (str): URL da API do modelo Roboflow.
        params (dict): Parâmetros de chamada à API (chave, confiança, etc).

    Returns:
        dict: Resposta JSON com as previsões ou erro.
    """
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    response = requests.post(
        url,
        params=params,
        data=encoded_image,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    print("Status Code:", response.status_code)
    try:
        return response.json()
    except Exception as e:
        print(f"Erro ao processar resposta JSON: {e}")
        return {}

if __name__ == "__main__":
    result = send_image_to_roboflow(image_path, url, params)
    print("Resposta JSON:", result)
