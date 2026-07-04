"""PKLot veri setiyle eğitilmiş YOLO26 (best.pt) yükleme ve çıkarım katmanı."""
import time

import numpy as np
import streamlit as st
from PIL import Image

from smartpark.config import YOLO_WEIGHTS, YOLO_IMG_SIZE, YOLO_DEFAULT_CONF


@st.cache_resource
def load_yolo_model():
    """
    PKLot veri setiyle eğitilmiş YOLO26 modelini yükler.
    Sınıflar: 0 -> space-empty (boş park yeri), 1 -> space-occupied (dolu park yeri)
    """
    from ultralytics import YOLO
    try:
        return YOLO(str(YOLO_WEIGHTS))
    except Exception as e:
        st.error(f"YOLO modeli ({YOLO_WEIGHTS.name}) yüklenirken hata oluştu: {e}")
        return None


def run_yolo_detection(model, image: Image.Image, conf: float = YOLO_DEFAULT_CONF):
    """
    Park yeri tespiti yapar; boş ve dolu kutuları ayrı listeler halinde döndürür.
    """
    img_np = np.array(image.convert("RGB"))

    start_time = time.time()
    results = model.predict(img_np, imgsz=YOLO_IMG_SIZE, conf=conf, verbose=False)
    inference_time_ms = (time.time() - start_time) * 1000

    empty_boxes, occupied_boxes = [], []
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            coords = tuple(int(v) for v in box.xyxy[0])
            (empty_boxes if cls_id == 0 else occupied_boxes).append(coords)

    return empty_boxes, occupied_boxes, inference_time_ms
