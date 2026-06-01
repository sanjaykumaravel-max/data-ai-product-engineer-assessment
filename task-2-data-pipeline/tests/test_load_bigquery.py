import os
import sys
from unittest import mock

import pandas as pd


# Ensure the src directory is importable for tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import load_bigquery as loader


def test_load_dataframe_to_bigquery_calls_bigquery(monkeypatch):
    # Prepare a small DataFrame
    df = pd.DataFrame({"timestamp_utc": ["2026-06-01T00:00:00Z"], "temperature_c": [20.0]})

    # Create a fake client and job
    fake_client = mock.Mock()
    fake_job = mock.Mock()
    fake_job.job_id = "fake-job-id"
    fake_job.result.return_value = None

    # Configure the client mocks: get_dataset/get_table -> raise NotFound to trigger creation
    from google.api_core.exceptions import NotFound

    fake_client.get_dataset.side_effect = NotFound("not found")
    fake_client.create_dataset.return_value = None
    fake_client.get_table.side_effect = NotFound("not found")
    fake_client.create_table.return_value = None
    fake_client.load_table_from_dataframe.return_value = fake_job

    # Patch the Client constructor in google.cloud.bigquery to return our fake client
    import google.cloud.bigquery as gcbq

    monkeypatch.setattr(gcbq, "Client", lambda project=None: fake_client)

    # Execute the load function
    fq = loader.load_dataframe_to_bigquery(df, project_id="proj", dataset_id="ds", table_id="tbl")

    # Assertions: ensure the dataset and table creation paths were invoked and load called
    fake_client.get_dataset.assert_called()
    fake_client.create_dataset.assert_called()
    fake_client.get_table.assert_called()
    fake_client.create_table.assert_called()
    fake_client.load_table_from_dataframe.assert_called_with(df, mock.ANY, job_config=mock.ANY)
    assert fq == "proj.ds.tbl"
