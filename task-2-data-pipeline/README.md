# Task 2 - Data Pipeline

## Objective
Build a small Python pipeline that fetches data from a public API, transforms it into clean tabular data, loads it into BigQuery, and provides a SQL summary query.

## Technical Workflow
`API -> Python -> Clean Data -> BigQuery -> SQL`

## Public API Choice
- API: Open-Meteo
- Why this API for v1: free, no API key required, simple JSON response, easy to transform into rows.

## Engineering Thinking
- Error handling: API errors, timeouts, invalid JSON, missing fields, and pipeline failures are handled with clear exceptions.
- Parameterization: latitude, longitude, date range, timezone, project, dataset, and table are environment-driven.
- Logging: scripts log API calls, transformation row counts, BigQuery targets, and failures.
- Schema design: BigQuery fields use clear names and stable analytical types.

## Project Structure
- `src/fetch_data.py` - fetches structured JSON from Open-Meteo.
- `src/transform_data.py` - cleans/reshapes data and can run the pipeline.
- `src/load_bigquery.py` - creates dataset/table if needed and loads data.
- `src/config.py` - reads environment configuration.
- `queries/summary_query.sql` - BigQuery summary analysis.
- `requirements.txt` - Python dependencies.
- `sample_output/` - example output from the summary query.

## How To Run
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables:
   - `GOOGLE_CLOUD_PROJECT`
   - `BQ_DATASET`
   - `BQ_TABLE`
   - `LATITUDE`
   - `LONGITUDE`
   - `START_DATE`
   - `END_DATE`
   - `TIMEZONE`
3. Authenticate GCP locally: `gcloud auth application-default login`
4. Test fetch + transform only: `python src/transform_data.py --dry-run`
5. Run full pipeline to BigQuery: `python src/transform_data.py`
6. Run SQL from `queries/summary_query.sql` in BigQuery.

## BigQuery Notes
- BigQuery Sandbox can be used for this task.
- The loader creates the dataset/table if missing.
- The table is append-only in this v1 implementation.

## SQL Analysis
The summary query returns daily record counts, average temperature, min/max temperature, average wind speed, and rainy-hour totals.

## Production Thinking
- Scheduling: Cloud Scheduler + Cloud Run job, or cron for a simple server-based setup.
- Monitoring: structured logs, non-zero exit codes, job failure alerts, row-count checks, and freshness checks.
- Scaling: partition BigQuery by date, load incrementally, add API retry/backoff, and add data quality checks before loading.
