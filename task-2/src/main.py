import logging

from config import get_settings
from extract import fetch_weather_data
from transform import transform_weather_data
from load_bigquery import load_dataframe_to_bigquery


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


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
    main()
