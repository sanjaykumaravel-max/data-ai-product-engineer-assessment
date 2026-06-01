"""Integrated pipeline: fetch -> transform -> load (optional)

This script ties together the `fetch_weather`, `transform_weather`, and
`load_bigquery` helpers in a simple CLI so the whole pipeline can run from
one place. It keeps logic explicit and beginner-friendly.
"""

from typing import Optional
import argparse
import json
import logging
import sys

import pandas as pd

from .fetch_weather import fetch_weather
from .transform_weather import transform_weather
from .load_bigquery import load_dataframe_to_bigquery


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def run_pipeline(
    project: Optional[str],
    dataset: Optional[str],
    table: Optional[str],
    lat: Optional[float],
    lon: Optional[float],
    input_json: Optional[str],
    hourly: str = "temperature_2m",
    timezone: str = "UTC",
    dry_run: bool = False,
):
    """Run end-to-end pipeline.

    If `input_json` is provided, the script will read the JSON produced by
    `fetch_weather.py`. Otherwise it will call the Open-Meteo API for the
    provided `lat`/`lon`.
    """
    if input_json:
        logger.info("Loading input JSON from %s", input_json)
        with open(input_json, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    else:
        if lat is None or lon is None:
            raise ValueError("Latitude and longitude must be provided when not using --input")
        raw = fetch_weather(latitude=lat, longitude=lon, hourly=hourly, timezone=timezone)

    logger.info("Transforming weather data")
    df = transform_weather(raw)

    logger.info("Transformed DataFrame: %d rows, %d cols", len(df), len(df.columns))

    if dry_run:
        # Print a short preview and exit
        print(df.head().to_string(index=False))
        return df

    # If load parameters are provided, attempt to load to BigQuery
    if project and dataset and table:
        logger.info("Loading DataFrame to BigQuery: %s.%s.%s", project, dataset, table)
        fq_table = load_dataframe_to_bigquery(df, project_id=project, dataset_id=dataset, table_id=table)
        logger.info("Load complete: %s", fq_table)
        return fq_table

    logger.warning("No BigQuery destination provided; pipeline completed without loading.")
    return df


def _parse_args():
    p = argparse.ArgumentParser(description="Run weather fetch -> transform -> load pipeline")
    input_group = p.add_mutually_exclusive_group(required=False)
    input_group.add_argument("--input", "-i", help="Path to input JSON (structured output from fetch) ")
    input_group.add_argument("--latlon", "-ll", nargs=2, type=float, metavar=("LAT", "LON"), help="Latitude and longitude to fetch from Open-Meteo")

    p.add_argument("--hourly", default="temperature_2m", help="Hourly fields to request (comma separated)")
    p.add_argument("--timezone", default="UTC", help="Timezone for API results")
    p.add_argument("--project", help="GCP project id for BigQuery load")
    p.add_argument("--dataset", help="BigQuery dataset id")
    p.add_argument("--table", help="BigQuery table id")
    p.add_argument("--dry-run", action="store_true", help="Do not load to BigQuery; print preview instead")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    lat = lon = None
    if args.latlon:
        lat, lon = args.latlon

    try:
        result = run_pipeline(
            project=args.project,
            dataset=args.dataset,
            table=args.table,
            lat=lat,
            lon=lon,
            input_json=args.input,
            hourly=args.hourly,
            timezone=args.timezone,
            dry_run=args.dry_run,
        )

        if isinstance(result, pd.DataFrame):
            logger.info("Pipeline finished: DataFrame returned (rows=%d)", len(result))
        else:
            logger.info("Pipeline finished: %s", str(result))

    except Exception as exc:
        logger.exception("Pipeline failed: %s", exc)
        sys.exit(1)
