# ML Model Builder Application

This project is an application that processes CSV data, generates a machine learning model, uploads the model to S3, and saves relevant metadata to a MongoDB instance. The application consists of an ML component, a Flask/MongoDB API, and a main script that orchestrates the entire process.

## Installation

1. Clone the repository:


2. Install dependencies:

pip install -r requirements.txt



3. Set up environment variables:

LOCAL_CSV_FILE: Path to your local CSV file.
TARGET_COLUMN: Name of the target column in the CSV file.
MONGODB_SETTINGS: MongoDB connection string.

4. Running the application
./run_docker.sh

5. Building the Docker Image
docker build -t ml-model-builder-image .

6. Running the Docker Containe
docker run -e LOCAL_CSV_FILE=/path/to/your/csv/file.csv -e TARGET_COLUMN=your_target_column_name  ml-model-builder-image


