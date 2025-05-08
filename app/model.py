# app/model.py
import os
import cv2
from ultralytics import YOLO

# --- Load weights file ---
WEIGHTS_PATH = "yolo12s-best.pt"  # ensure this matches your actual filename
print(f"[model] using weights: {WEIGHTS_PATH}, exists: {os.path.isfile(WEIGHTS_PATH)}")

# Initialize YOLO with custom weights
model = YOLO(WEIGHTS_PATH)
model.fuse()
model.to("cpu")

# Pull class names from the loaded model
CLASS_NAMES = model.names
print(f"[model] class names: {CLASS_NAMES}")


def detect(frame, conf_threshold=0.2, imgsz=640):
    """
    Run detection on a single BGR frame.
    Args:
        frame (np.ndarray): HxW BGR image
        conf_threshold (float): confidence threshold for boxes
        imgsz (int): inference image size
    Returns:
        List of (x1, y1, x2, y2, conf, cls)
    """
    # Perform detection; Ultralytics handles resizing internally
    results = model.predict(
        source=frame,
        conf=conf_threshold,
        imgsz=imgsz,
        device="cpu",
        verbose=False
    )[0]

    # Extract boxes, confidences, and class IDs
    boxes = results.boxes.xyxy.cpu().numpy()  # shape Nx4
    confs = results.boxes.conf.cpu().numpy()  # shape N
    clss  = results.boxes.cls.cpu().numpy()   # shape N

    print(f"[detect] found {len(boxes)} boxes at conf>={conf_threshold}")

    detections = []
    for (x1, y1, x2, y2), conf, cls in zip(boxes, confs, clss):
        detections.append((
            int(x1), int(y1), int(x2), int(y2), float(conf), int(cls)
        ))
    return detections
