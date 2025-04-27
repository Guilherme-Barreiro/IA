import base64
import requests

# Configuration variables
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

with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

response = requests.post(url, params=params, data=encoded_image, headers={"Content-Type": "application/x-www-form-urlencoded"})

print("Status Code:", response.status_code)
print("Response:", response.json())
