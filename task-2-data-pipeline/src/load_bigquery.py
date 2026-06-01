import logging
from typing import List, Optional

import pandas as pd
from google.api_core.exceptions import GoogleAPIError, NotFound
from google.cloud import bigquery


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


DEFAULT_WEATHER_SCHEMA = [
    bigquery.SchemaField("timestamp_utc", "TIMESTAMP"),
    bigquery.SchemaField("temperature_c", "FLOAT64"),
    bigquery.SchemaField("precipitation_mm", "FLOAT64"),
    bigquery.SchemaField("wind_speed_kmh", "FLOAT64"),
    bigquery.SchemaField("relative_humidity_pct", "FLOAT64"),
    bigquery.SchemaField("is_rain_hour", "INT64"),
    bigquery.SchemaField("temperature_band", "STRING"),
]


def _ensure_dataset(client: bigquery.Client, project_id: str, dataset_id: str) -> None:
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    try:
        client.get_dataset(dataset_ref)
        logger.info("Dataset exists: %s.%s", project_id, dataset_id)
    except NotFound:
        logger.info("Dataset not found, creating: %s.%s", project_id, dataset_id)
        client.create_dataset(bigquery.Dataset(dataset_ref))


def _ensure_table(
    client: bigquery.Client,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema: List[bigquery.SchemaField],
) -> None:
    table_ref = bigquery.DatasetReference(project_id, dataset_id).table(table_id)
    try:
        client.get_table(table_ref)
        logger.info("Table exists: %s.%s.%s", project_id, dataset_id, table_id)
    except NotFound:
        logger.info("Table not found, creating: %s.%s.%s", project_id, dataset_id, table_id)
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)


def load_dataframe_to_bigquery(
    df: pd.DataFrame,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema: Optional[List[bigquery.SchemaField]] = None,
    write_disposition: str = "WRITE_APPEND",
) -> str:
    """Load a pandas DataFrame into BigQuery using a stable weather schema."""
    selected_schema = schema or DEFAULT_WEATHER_SCHEMA
    client = bigquery.Client(project=project_id)

    try:
        _ensure_dataset(client, project_id, dataset_id)
        _ensure_table(client, project_id, dataset_id, table_id, schema=selected_schema)
    except GoogleAPIError as exc:
        logger.exception("Failed to ensure dataset/table: %s", exc)
        raise

    table_ref = bigquery.DatasetReference(project_id, dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig(
        schema=selected_schema,
        write_disposition=write_disposition,
    )

    try:
        logger.info("Starting load job to %s.%s.%s (rows=%d)", project_id, dataset_id, table_id, len(df))
        load_job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        load_job.result()
        logger.info("Load job finished: %s", load_job.job_id)
    except GoogleAPIError as exc:
        logger.exception("BigQuery load failed: %s", exc)
        raise
    except Exception as exc:
        logger.exception("Unexpected error during BigQuery load: %s", exc)
        raise

    return f"{project_id}.{dataset_id}.{table_id}"
