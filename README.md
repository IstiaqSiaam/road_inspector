# 🛣️ Road Inspector

Road Inspector is a web-based application that processes uploaded road videos to detect and highlight potholes and garbage using a **YOLOv12s** object-detection model. The application is containerized with **Docker** for easy deployment and scalability.

## 🚀 Features

- Upload road videos through a user-friendly web interface.  
- Process videos to detect potholes and garbage using YOLOv12s.  
- Display processed videos with bounding boxes highlighting detected objects.  
- Containerized with Docker for consistent deployment across environments.

## 🛠️ Installation

**Prerequisites**  
Ensure you have **Docker** installed on your system.

**Building the Docker image**

git clone https://github.com/IstiaqSiaam/road-inspector.git
cd road-inspector
docker build -t road-inspector .


**Running the Docker container**

docker run -p 8000:80 road-inspector

This maps port **80** inside the container to port **8000** on your host machine.

## 📈 Usage

1. Open your browser and navigate to `http://localhost:8000`.  
2. Upload a road video using the provided interface.  
3. The application will process the video and display it with potholes and garbage highlighted.
