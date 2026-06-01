from google.api_core.exceptions import NotFound
from google.cloud import bigquery


def _ensure_dataset(client: bigquery.Client, project_id: str, dataset_id: str) -> None:
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    try:
        client.get_dataset(dataset_ref)
    except NotFound:
        client.create_dataset(bigquery.Dataset(dataset_ref))


def load_dataframe_to_bigquery(df, project_id: str, dataset_id: str, table_id: str) -> str:
    client = bigquery.Client(project=project_id)

    _ensure_dataset(client, project_id, dataset_id)

    table_ref = bigquery.DatasetReference(project_id, dataset_id).table(table_id)

    schema = [
        bigquery.SchemaField("timestamp_utc", "TIMESTAMP"),
        bigquery.SchemaField("temperature_c", "FLOAT64"),
        bigquery.SchemaField("precipitation_mm", "FLOAT64"),
        bigquery.SchemaField("wind_speed_kmh", "FLOAT64"),
        bigquery.SchemaField("relative_humidity_pct", "FLOAT64"),
        bigquery.SchemaField("is_rain_hour", "INT64"),
        bigquery.SchemaField("temperature_band", "STRING"),
    ]

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_APPEND",
    )

    load_job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    load_job.result()

    return f"{project_id}.{dataset_id}.{table_id}"
