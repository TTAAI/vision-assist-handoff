from fastapi import FastAPI, File, Request, UploadFile
from ultralytics import YOLO
import cv2
import numpy as np
import time


app = FastAPI(title="Vision Assist Server")
model = YOLO("yolo11n.pt")

CN = {
    "person": "行人",
    "bicycle": "自行车",
    "car": "汽车",
    "motorcycle": "摩托车",
    "bus": "公交车",
    "truck": "货车",
    "traffic light": "交通灯",
    "chair": "椅子",
    "bench": "长椅",
    "backpack": "背包",
    "suitcase": "行李箱",
}

RISK_CLASSES = {
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "bus",
    "truck",
    "chair",
    "bench",
    "backpack",
    "suitcase",
}


def position_name(x1: float, x2: float, width: int) -> str:
    cx = (x1 + x2) / 2
    if cx < width / 3:
        return "左前方"
    if cx > width * 2 / 3:
        return "右前方"
    return "正前方"


def analyze_image_bytes(data: bytes) -> dict:
    started = time.time()
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if img is None:
        return {"level": "error", "message": "图像解析失败", "speak": "图像解析失败", "objects": []}

    h, w = img.shape[:2]
    result = model.predict(img, imgsz=640, conf=0.35, device=0, verbose=False)[0]

    objects = []
    warnings = []

    for box in result.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls_id]
        x1, y1, x2, y2 = [float(v) for v in box.xyxy[0]]
        pos = position_name(x1, x2, w)
        area_ratio = ((x2 - x1) * (y2 - y1)) / float(w * h)

        item = {
            "label": label,
            "name": CN.get(label, label),
            "confidence": round(conf, 3),
            "position": pos,
            "area_ratio": round(area_ratio, 4),
        }
        objects.append(item)

        if label in RISK_CLASSES and area_ratio > 0.03:
            warnings.append(f"{pos}有{CN.get(label, label)}")

    if warnings:
        level = "warning"
        speak = warnings[0] + "，请注意"
    elif objects:
        level = "info"
        first = objects[0]
        speak = f"检测到{first['position']}有{first['name']}"
    else:
        level = "clear"
        speak = "前方暂未发现明显障碍"

    return {
        "level": level,
        "message": speak,
        "speak": speak,
        "latency_ms": int((time.time() - started) * 1000),
        "objects": objects[:10],
    }


@app.get("/health")
def health():
    return {"ok": True, "model": "yolo11n", "device": "cuda:0"}


@app.post("/analyze")
async def analyze(request: Request, file: UploadFile | None = File(default=None)):
    if file is not None:
        data = await file.read()
    else:
        data = await request.body()
    return analyze_image_bytes(data)

