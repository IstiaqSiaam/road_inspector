🛣️ Road Inspector
Road Inspector is a web-based application that processes uploaded road videos to detect and highlight potholes and garbage using a YOLOv12s object detection model. The application is containerized using Docker for easy deployment and scalability.

🚀 Features
Upload road videos through a user-friendly web interface.

Process videos to detect potholes and garbage using YOLOv12s.

Display processed videos with bounding boxes highlighting detected objects.

Containerized with Docker for consistent deployment across environments.

🛠️ Installation
Prerequisites
Ensure you have the following installed on your system:

Docker

Building the Docker Image
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/road-inspector.git
cd road-inspector
Build the Docker image:

bash
Copy
Edit
docker build -t road-inspector .
Running the Docker Container
Run the Docker container with the following command:

bash
Copy
Edit
docker run -p 8000:80 road-inspector
This maps port 80 inside the container to port 8000 on your host machine.

📈 Usage
Open your web browser and navigate to http://localhost:8000.

Upload a road video using the provided interface.

The application will process the video and display it with detected potholes and garbage highlighted.