from google.cloud import bigquery


def load_dataframe_to_bigquery(df, project_id: str, dataset_id: str, table_id: str) -> str:
    client = bigquery.Client(project=project_id)

    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    table_ref = dataset_ref.table(table_id)

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")

    load_job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    load_job.result()

    return f"{project_id}.{dataset_id}.{table_id}"
