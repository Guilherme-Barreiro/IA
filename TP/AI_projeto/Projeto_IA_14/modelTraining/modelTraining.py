from ultralytics import YOLO

# Treinar modelo versão 2 diretamente a partir do yolov8n.pt (sem o carregar antes)
YOLO("yolov8n.pt").train(
    data="../../Dataset_IA_14/noDataAgm/data.yaml",
    epochs=30,
    project="noDataAgm",
    name="runs",
    exist_ok=True
)

# Treinar modelo versão 5 diretamente a partir do yolov8n.pt (sem o carregar antes)
YOLO("yolov8n.pt").train(
    data="../../Dataset_IA_14/dataAgmBlur/data.yaml",
    epochs=30,
    project="dataAgmBlur",
    name="runs",
    exist_ok=True
)

# Após treino, carregar os modelos best.pt gerados e avaliar/predizer
model_v1 = YOLO("noDataAgm/runs/weights/best.pt")
model_v2 = YOLO("dataAgmBlur/runs/weights/best.pt")

metrics_v1 = model_v1.val()
metrics_v2= model_v2.val()

print("\n📊 Métricas para noDataAgm (sem augmentation):", metrics_v1)
print("\n📈 Métricas para dataAgmBlur (com augmentation):", metrics_v2)

model_v1.predict("test_image.png", save=True)
model_v2.predict("test_image.png", save=True)
