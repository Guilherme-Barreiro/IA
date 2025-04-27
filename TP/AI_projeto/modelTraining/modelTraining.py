# YOLOv8 - Grupo 14 AI
# Treino com e sem data augmentation

from roboflow import Roboflow
from ultralytics import YOLO

# API Key
rf = Roboflow(api_key="0GZwVsB4wlDoIK7lDggb")

# Dataset V2: sem data augmentation
project = rf.workspace("grupo14ai").project("chessboarddetection-m4ei0")
version_v2 = project.version(2)
dataset_v2 = version_v2.download("yolov8")

# Dataset V5: com data augmentation
version_v5 = project.version(5)
dataset_v5 = version_v5.download("yolov8")

# Treinar modelo V2 e guardar na pasta do dataset
model_v2 = YOLO("yolov8n.pt")
model_v2.train(
    data="/Users/antoniosilva/Desktop/AI/modelTraining/ChessBoardDetection-2/data.yaml",
    epochs=30,
    project="ChessBoardDetection-2",
    name="runs",
    exist_ok=True
)

# Treinar modelo V5 e guardar na pasta do dataset
model_v5 = YOLO("yolov8n.pt")
model_v5.train(
    data="/Users/antoniosilva/Desktop/AI/modelTraining/ChessBoardDetection-5/data.yaml",
    epochs=30,
    project="ChessBoardDetection-5",
    name="runs",
    exist_ok=True
)

# Avaliar modelos
metrics_v2 = model_v2.val()
metrics_v5 = model_v5.val()

print("\n📊 Metrics for version 2 (sem augmentation):", metrics_v2)
print("\n📈 Metrics for version 5 (com augmentation):", metrics_v5)

# Testar previsões em imagem de teste
model_v2.predict("test_image.png", save=True)
model_v5.predict("test_image.png", save=True)
