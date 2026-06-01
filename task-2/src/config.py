from dataclasses import dataclass
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    google_cloud_project: str
    bq_dataset: str
    bq_table: str
    latitude: float
    longitude: float
    start_date: str
    end_date: str
    timezone: str


def get_settings() -> Settings:
    return Settings(
        google_cloud_project=os.getenv("GOOGLE_CLOUD_PROJECT", ""),
        bq_dataset=os.getenv("BQ_DATASET", "marketing_pipeline"),
        bq_table=os.getenv("BQ_TABLE", "weather_hourly"),
        latitude=float(os.getenv("LATITUDE", "12.9716")),
        longitude=float(os.getenv("LONGITUDE", "77.5946")),
        start_date=os.getenv("START_DATE", "2026-05-25"),
        end_date=os.getenv("END_DATE", "2026-05-31"),
        timezone=os.getenv("TIMEZONE", "auto"),
    )
