FROM python:3.9-slim

# install OpenCV dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
       libgl1-mesa-glx \
       libglib2.0-0 \
       ffmpeg \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY yolo12s-best.pt ./app/

WORKDIR /app/app
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
