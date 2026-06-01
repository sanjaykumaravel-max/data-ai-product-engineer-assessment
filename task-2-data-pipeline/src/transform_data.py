"""Transform Open-Meteo JSON into clean tabular weather data."""

import argparse
import logging
import sys
from typing import Optional

import pandas as pd

from config import get_settings
from fetch_data import fetch_weather_data
from load_bigquery import load_dataframe_to_bigquery


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def transform_weather_data(raw_data: dict) -> pd.DataFrame:
    """Flatten Open-Meteo hourly JSON and add analytical fields."""
    hourly = raw_data.get("hourly", {})

    df = pd.DataFrame(
        {
            "timestamp_utc": hourly.get("time", []),
            "temperature_c": hourly.get("temperature_2m", []),
            "precipitation_mm": hourly.get("precipitation", []),
            "wind_speed_kmh": hourly.get("wind_speed_10m", []),
            "relative_humidity_pct": hourly.get("relative_humidity_2m", []),
        }
    )

    if df.empty:
        raise ValueError("No hourly data returned from API")

    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], errors="coerce")
    numeric_cols = ["temperature_c", "precipitation_mm", "wind_speed_kmh", "relative_humidity_pct"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["timestamp_utc"]).fillna(0)

    # Derived fields add simple analytical value beyond the raw API response.
    df["is_rain_hour"] = (df["precipitation_mm"] > 0).astype(int)
    df["temperature_band"] = pd.cut(
        df["temperature_c"],
        bins=[-100, 15, 25, 35, 100],
        labels=["cool", "mild", "warm", "hot"],
    ).astype(str)

    return df


def run_pipeline(dry_run: bool = False) -> Optional[str]:
    """Run fetch -> transform -> optional BigQuery load using environment config."""
    settings = get_settings()

    raw_data = fetch_weather_data(
        latitude=settings.latitude,
        longitude=settings.longitude,
        start_date=settings.start_date,
        end_date=settings.end_date,
        timezone=settings.timezone,
    )
    df = transform_weather_data(raw_data)
    logger.info("Transformed rows: %s", len(df))

    if dry_run:
        print(df.head().to_string(index=False))
        return None

    table_name = load_dataframe_to_bigquery(
        df,
        project_id=settings.google_cloud_project,
        dataset_id=settings.bq_dataset,
        table_id=settings.bq_table,
    )
    logger.info("Loaded data to BigQuery table: %s", table_name)
    return table_name


def main() -> None:
    parser = argparse.ArgumentParser(description="Transform Open-Meteo data and optionally load to BigQuery")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and transform only; do not load to BigQuery")
    args = parser.parse_args()

    try:
        run_pipeline(dry_run=args.dry_run)
    except Exception:
        logger.exception("Pipeline failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
