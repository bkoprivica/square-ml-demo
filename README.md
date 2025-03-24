# Square ML Demo

This repository demonstrates a minimal machine learning pipeline that mirrors key responsibilities of a Senior Machine Learning Engineer. The project includes:

- **Churn Prediction**: Training a logistic regression model on synthetic data.
- **Product Recommendations**: A static endpoint that returns product recommendations.
- **Generative AI**: A text-generation endpoint using DistilGPT2.

## Project Structure

square-ml-demo/ 
├── README.md # Project overview and setup instructions 
├── requirements.txt # Python dependencies 
├── train_churn_model.py # Script to train and save the churn model 
├── app.py # Flask API providing endpoints for predictions, recommendations, and text generation 
├── Dockerfile # Docker image build configuration 
├── k8s/ 
│ ├── deployment.yaml # Kubernetes deployment manifest 
│ └── service.yaml # Kubernetes LoadBalancer service manifest (using MetalLB) 
└── .github/ 
          └── workflows/ 
		           └── deploy.yml # GitHub Actions CI/CD pipeline configuration

## Local Development Setup

### Prerequisites

- **WSL2 with Ubuntu 22.04**
- **Visual Studio Code with the Remote - WSL extension**
- **Git**: Install via `sudo apt update && sudo apt install git -y`
- **Python 3 and pip**: Check with `python3 --version`; if needed, install using `sudo apt install python3 python3-venv python3-pip -y`
- **Docker**: Install with:
`sudo apt update` 
`sudo apt install docker.io -y`
`sudo systemctl start docker` 
`sudo systemctl enable docker`
`sudo usermod -aG docker $USER`
- **Killercoda Access**: Obtain a Kubernetes cluster, a kubeconfig file, and the MetalLB IP range from your Killercoda setup.
- **GitHub Account**: This project is hosted at [github.com/bkoprivica](https://github.com/bkoprivica).

### Steps to Run Locally

1. **Clone the Repository**
- **Killercoda Access**: Obtain a Kubernetes cluster, a kubeconfig file, and the MetalLB IP range from your Killercoda setup.
- **GitHub Account**: This project is hosted at [github.com/bkoprivica](https://github.com/bkoprivica).

### Steps to Run Locally

1. **Clone the Repository**
git clone [https://github.com/bkoprivica/square-ml-demo.git](https://github.com/bkoprivica/square-ml-demo.git) 
cd square-ml-demo

2. **Create and Activate a Virtual Environment**
python3 -m venv venv 
source venv/bin/activate

3. **Install Dependencies**
pip install -r requirements.txt

4. **Train the ML Model**
python train_churn_model.py

5. **Run the Flask API**
python app.py
The API will be available at [http://localhost:5000](http://localhost:5000).

## API Endpoints

- **POST `/predict`**: Accepts a JSON payload with `feature1`, `feature2`, and `feature3` to return a churn prediction.
- **GET `/recommend`**: Returns a static list of product recommendations.
- **POST `/generate`**: Accepts a JSON payload with a `prompt` and returns generated text.

## Docker Instructions

- **Build the Docker Image**
docker build -t square-ml-demo .

- **Run the Docker Container**
docker run -p 5000:5000 square-ml-demo

## Kubernetes Deployment on Killercoda

1. **Set Up GitHub Secrets**  
 In your GitHub repository settings, add:
 - `KUBE_CONFIG_DATA`: The full kubeconfig file from your Killercoda cluster.
 - `METALLB_IP_RANGE`: The IP range provided by Killercoda for MetalLB (e.g., `192.168.1.240-192.168.1.250`).

2. **GitHub Actions Pipeline**  
 The workflow defined in `.github/workflows/deploy.yml` will:
 - Build and push the Docker image to GitHub Container Registry (`ghcr.io/bkoprivica/square-ml-demo:latest`).
 - Configure `kubectl` using your kubeconfig.
 - Deploy MetalLB in your cluster and apply the provided IP range.
 - Deploy the application using Kubernetes manifests.

3. **Access the Application**  
 After deployment, run:
kubectl get svc square-ml-demo
Use the external IP assigned by MetalLB to access the service (e.g., `http://<external-ip>:5000`).

## License

MIT
