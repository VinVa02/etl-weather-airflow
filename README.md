# Weather ETL Pipeline using Apache Airflow and Astro

## 📌 Project Overview

This project implements an end-to-end ETL (Extract, Transform, Load) pipeline using
Apache Airflow with the Astronomer (Astro) framework.

The pipeline fetches real-time weather data from the Open-Meteo API for a given
geographical location, processes the data, and stores it in a PostgreSQL database.
It demonstrates practical data engineering skills such as workflow orchestration,
API integration, data transformation, and database loading.

---

## ⚙️ ETL Workflow

The pipeline follows a standard ETL architecture:

### 1. Extract
- Fetches current weather data from the Open-Meteo API
- Uses Airflow HTTP connections for API access

### 2. Transform
- Extracts relevant weather fields
- Converts values into consistent data types

### 3. Load
- Creates a PostgreSQL table if it does not exist
- Inserts transformed weather data
- Supports both local PostgreSQL and Amazon RDS

---

## 📊 Data Collected

Each pipeline run stores the following fields:

- Latitude
- Longitude
- Temperature
- Wind Speed
- Wind Direction
- Weather Code
- Timestamp (auto-generated)

The data is stored in a table named `weather_data`.

---

## 🛠️ Tech Stack

- Apache Airflow (TaskFlow API)
- Astronomer (Astro CLI)
- Docker
- PostgreSQL (Local & Amazon RDS)
- Python
- Open-Meteo API

---

## 🚀 Running the Project Locally

### Prerequisites

- Docker Desktop
- Astronomer CLI
- Git

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/VinVa02/etl-weather-airflow.git
cd etl-weather-airflow
2️⃣ Start Airflow
astro dev start
This command starts the following containers:

PostgreSQL (Airflow metadata database)

Scheduler

DAG Processor

API Server (Airflow UI)

Triggerer

The Airflow UI will be available at:

http://localhost:8080
3️⃣ Configure Airflow Connections
Create the following connections in the Airflow UI.

Open-Meteo API Connection
Connection ID: open_meteo_api

Connection Type: HTTP

Host: https://api.open-meteo.com

PostgreSQL Connection
Connection ID: postgres_default

Connection Type: Postgres

Host: postgres (Docker) or RDS endpoint

Port: 5432

Database: postgres

Username: postgres

Password: postgres

4️⃣ Run the Pipeline
Open the Airflow UI

Enable weather_etl_pipeline

Click Trigger DAG

The pipeline will execute:

Extract → Transform → Load
☁️ Cloud Deployment (Optional)
The pipeline can be connected to Amazon RDS by updating the
postgres_default Airflow connection with the RDS endpoint and credentials.
This enables cloud-based storage and deployment.

📅 Scheduling
Current Mode: Manual trigger

Supported: Daily scheduling using @daily

To enable automatic execution, turn the DAG ON in the Airflow UI.

🔍 Monitoring & Logging
Task execution can be monitored using Grid and Graph views

Logs are available for each task instance

XCom is used for passing data between tasks

📈 Future Enhancements
Parameterize latitude and longitude using Airflow Variables

Add data validation and quality checks

Implement alerting for failures

Build a visualization dashboard (Power BI / Streamlit)

Add CI/CD for deployment

👤 Author
Vindhya Vaasini M
GitHub: https://github.com/VinVa02
