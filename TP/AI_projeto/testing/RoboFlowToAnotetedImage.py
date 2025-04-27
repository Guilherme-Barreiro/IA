import base64
import requests
from PIL import Image, ImageDraw, ImageFont

# Configuration variables
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

with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

response = requests.post(url, params=params, data=encoded_image, headers={"Content-Type": "application/x-www-form-urlencoded"})

if response.status_code == 200:
    result = response.json()
    print("Inference successful. Processing results...")

    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        font = ImageFont.load_default()

    for prediction in result['predictions']:
        x = prediction["x"]
        y = prediction["y"]
        w = prediction["width"]
        h = prediction["height"]
        label = prediction["class"]

        x0 = x - w / 2
        y0 = y - h / 2
        x1 = x + w / 2
        y1 = y + h / 2

        draw.rectangle([x0, y0, x1, y1], outline="red", width=2)
        draw.text((x0, y0 - 10), label, fill="red", font=font)

    output_image_path = "annotated_image.png"
    image.save(output_image_path)
    print(f"Annotated image saved as {output_image_path}")

else:
    print(f"Error: {response.status_code}, {response.text}")
