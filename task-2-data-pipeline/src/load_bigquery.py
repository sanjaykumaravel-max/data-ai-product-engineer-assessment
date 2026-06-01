import logging
from typing import List, Optional

import pandas as pd
from google.api_core.exceptions import GoogleAPIError, NotFound
from google.cloud import bigquery


# Basic logging configuration for beginner-friendly output
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def _ensure_dataset(client: bigquery.Client, project_id: str, dataset_id: str) -> None:
    """Ensure the BigQuery dataset exists; create it if it does not.

    This function is idempotent and safe to call multiple times.
    """
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    try:
        client.get_dataset(dataset_ref)
        logger.info("Dataset exists: %s.%s", project_id, dataset_id)
    except NotFound:
        logger.info("Dataset not found, creating: %s.%s", project_id, dataset_id)
        client.create_dataset(bigquery.Dataset(dataset_ref))


def _ensure_table(client: bigquery.Client, project_id: str, dataset_id: str, table_id: str, schema: Optional[List[bigquery.SchemaField]] = None) -> None:
    """Ensure the BigQuery table exists; create it with the given schema if missing.

    If `schema` is None, the table will be created without an explicit schema
    and BigQuery's auto-detection can be used when loading.
    """
    table_ref = bigquery.DatasetReference(project_id, dataset_id).table(table_id)
    try:
        client.get_table(table_ref)
        logger.info("Table exists: %s.%s.%s", project_id, dataset_id, table_id)
    except NotFound:
        logger.info("Table not found, creating: %s.%s.%s", project_id, dataset_id, table_id)
        table = bigquery.Table(table_ref)
        if schema:
            table.schema = schema
        client.create_table(table)


def load_dataframe_to_bigquery(
    df: pd.DataFrame,
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema: Optional[List[bigquery.SchemaField]] = None,
    write_disposition: str = "WRITE_APPEND",
) -> str:
    """Load a pandas DataFrame into BigQuery.

    Args:
        df: DataFrame to upload.
        project_id: GCP project id.
        dataset_id: BigQuery dataset id.
        table_id: BigQuery table id.
        schema: Optional explicit schema (list of `bigquery.SchemaField`).
        write_disposition: One of BigQuery write dispositions, e.g. 'WRITE_APPEND'.

    Returns:
        The fully-qualified table name written to.

    Notes:
        - Requires Google Cloud credentials to be configured in the environment.
        - If `schema` is None, BigQuery's schema autodetection will be used during load.
    """
    client = bigquery.Client(project=project_id)

    # Ensure dataset and table exist
    try:
        _ensure_dataset(client, project_id, dataset_id)
        _ensure_table(client, project_id, dataset_id, table_id, schema=schema)
    except GoogleAPIError as exc:
        logger.exception("Failed to ensure dataset/table: %s", exc)
        raise

    table_ref = bigquery.DatasetReference(project_id, dataset_id).table(table_id)

    # If no explicit schema provided, allow BigQuery to auto-detect during load.
    job_config = bigquery.LoadJobConfig(
        schema=schema or [],
        autodetect=(schema is None),
        write_disposition=write_disposition,
    )

    try:
        logger.info("Starting load job to %s.%s.%s (rows=%d)", project_id, dataset_id, table_id, len(df))
        load_job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        load_job.result()  # Wait for job to complete
        logger.info("Load job finished: %s", load_job.job_id)
    except GoogleAPIError as exc:
        logger.exception("BigQuery load failed: %s", exc)
        raise
    except Exception as exc:  # broad catch to make beginner debugging easier
        logger.exception("Unexpected error during BigQuery load: %s", exc)
        raise

    return f"{project_id}.{dataset_id}.{table_id}"


def _parse_args():
    import argparse

    p = argparse.ArgumentParser(description="Load a CSV file into BigQuery using pandas DataFrame")
    p.add_argument("--input", "-i", required=True, help="Path to input CSV file")
    p.add_argument("--project", "-p", required=True, help="GCP project id")
    p.add_argument("--dataset", "-d", required=True, help="BigQuery dataset id")
    p.add_argument("--table", "-t", required=True, help="BigQuery table id")
    p.add_argument("--write-disposition", "-w", default="WRITE_APPEND", help="BigQuery write disposition (default: WRITE_APPEND)")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    try:
        # Read CSV into DataFrame (simple, beginner-friendly)
        df = pd.read_csv(args.input)
    except Exception as exc:
        logger.exception("Failed to read input CSV: %s", exc)
        raise SystemExit(1)

    try:
        fq_table = load_dataframe_to_bigquery(df, project_id=args.project, dataset_id=args.dataset, table_id=args.table, write_disposition=args.write_disposition)
        logger.info("Successfully loaded data to %s", fq_table)
        print(fq_table)
    except Exception as exc:
        logger.exception("Failed to load DataFrame to BigQuery: %s", exc)
        raise SystemExit(1)
