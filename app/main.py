# app/main.py
import os
import shutil
import uuid
import subprocess
import cv2
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model import detect, CLASS_NAMES

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    # 1) Save upload
    vid_id = str(uuid.uuid4())
    in_path = os.path.join(UPLOAD_DIR, f"{vid_id}.mp4")
    out_path = os.path.join(PROCESSED_DIR, f"{vid_id}_out.mp4")
    with open(in_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 2) Run detection and write raw MP4
    cap = cv2.VideoCapture(in_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS) or 20.0

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")   # raw container
    writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Failed to open video writer")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        for x1,y1,x2,y2,conf,cls in detect(frame, conf_threshold=0.2):
            label = f"{CLASS_NAMES[cls]} {conf:.2f}"
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(frame, label, (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        writer.write(frame)

    cap.release()
    writer.release()

    # 3) Re-encode with H.264 for browser compatibility
    tmp_path = out_path.replace(".mp4", "_h264.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", out_path,
        "-c:v", "libx264",
        "-crf", "23",
        "-preset", "medium",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        tmp_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.replace(tmp_path, out_path)

    # 4) Return final video
    return FileResponse(out_path, media_type="video/mp4", filename="result.mp4")
