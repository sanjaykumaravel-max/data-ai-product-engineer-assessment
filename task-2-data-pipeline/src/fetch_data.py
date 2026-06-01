import logging
import sys
from typing import Any, Dict

import requests

from config import get_settings
from load_bigquery import load_dataframe_to_bigquery
from transform_data import transform_weather_data


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def fetch_weather_data(latitude: float, longitude: float, start_date: str, end_date: str, timezone: str) -> Dict[str, Any]:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m",
        "timezone": timezone,
    }

    logger.info("Requesting Open-Meteo data", extra={"params": params})

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        logger.exception("API request failed")
        raise RuntimeError(f"Failed to fetch weather data: {exc}") from exc

    if "hourly" not in data:
        raise ValueError("Unexpected API response: missing 'hourly' field")

    return data


def main() -> None:
    settings = get_settings()

    logger.info("Starting pipeline run")

    raw_data = fetch_weather_data(
        latitude=settings.latitude,
        longitude=settings.longitude,
        start_date=settings.start_date,
        end_date=settings.end_date,
        timezone=settings.timezone,
    )

    transformed_df = transform_weather_data(raw_data)
    logger.info("Transformed rows: %s", len(transformed_df))

    table_fqn = load_dataframe_to_bigquery(
        transformed_df,
        project_id=settings.google_cloud_project,
        dataset_id=settings.bq_dataset,
        table_id=settings.bq_table,
    )

    logger.info("Loaded data to BigQuery table: %s", table_fqn)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Pipeline failed")
        sys.exit(1)
