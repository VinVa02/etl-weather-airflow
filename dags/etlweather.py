from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Location: London
LATITUDE = 41.2900 
LONGITUDE = -72.9571

POSTGRES_CONN_ID = "postgres_default"
API_CONN_ID = "open_meteo_api"

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="weather_etl_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 2, 10),  # pick a fixed date (safer than days_ago)
    schedule="@daily",
    catchup=False,
    tags=["etl", "weather"],
) as dag:

    @task
    def extract_weather_data() -> dict:
        """Extract weather data from Open-Meteo API using Airflow Connection."""
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method="GET")

        # base_url from connection + endpoint below
        endpoint = (
            f"/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"
        )

        response = http_hook.run(endpoint)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch weather data: {response.status_code} {response.text}")

        return response.json()

    @task
    def transform_weather_data(weather_data: dict) -> dict:
        """Transform the extracted weather data."""
        current_weather = weather_data.get("current_weather", {})
        return {
            "latitude": float(LATITUDE),
            "longitude": float(LONGITUDE),
            "temperature": float(current_weather["temperature"]),
            "windspeed": float(current_weather["windspeed"]),
            "winddirection": float(current_weather["winddirection"]),
            "weathercode": int(current_weather["weathercode"]),
        }

    @task
    def load_weather_data(transformed_data: dict) -> None:
        """Load transformed data into PostgreSQL."""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        create_sql = """
        CREATE TABLE IF NOT EXISTS weather_data (
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            winddirection FLOAT,
            weathercode INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        insert_sql = """
        INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
        VALUES (%s, %s, %s, %s, %s, %s);
        """

        pg_hook.run(create_sql)
        pg_hook.run(
            insert_sql,
            parameters=(
                transformed_data["latitude"],
                transformed_data["longitude"],
                transformed_data["temperature"],
                transformed_data["windspeed"],
                transformed_data["winddirection"],
                transformed_data["weathercode"],
            ),
        )

    weather = extract_weather_data()
    transformed = transform_weather_data(weather)
    load_weather_data(transformed)
