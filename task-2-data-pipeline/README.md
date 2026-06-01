# Task 2 - Data Pipeline

## Objective
Build a small but complete Python pipeline that uses a public API, transforms the data, loads it into BigQuery, and supports SQL analysis.

## Technical Workflow
`API -> Python -> Clean Data -> BigQuery -> SQL`

## Public API Choice
- API: Open-Meteo
- Why this API for v1:
  - Free
  - No API key required
  - Simple JSON response
  - Easy to transform into tabular data

## Engineering Thinking
- Error Handling:
  - API request failures are caught and raised with clear context.
  - Unexpected payload shape (`hourly` missing) is validated and rejected.
  - Pipeline exits non-zero on failure.
- Parameterization:
  - Runtime behavior uses environment variables for project, dataset, table, coordinates, and dates.
- Logging:
  - Logs pipeline start, transformed row count, and target BigQuery table.
  - Logs failures with stack traces.
- Schema Design:
  - Explicit BigQuery schema with typed fields and clear names.

## Project Structure
- `src/fetch_data.py`
- `src/transform_data.py`
- `src/load_bigquery.py`
- `src/config.py`
- `queries/summary_query.sql`
- `requirements.txt`
- `sample_output/`

## How To Run
1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables:
   - `GOOGLE_CLOUD_PROJECT`
   - `BQ_DATASET`
   - `BQ_TABLE`
   - `LATITUDE`
   - `LONGITUDE`
   - `START_DATE`
   - `END_DATE`
   - `TIMEZONE`
4. Authenticate GCP locally: `gcloud auth application-default login`
5. Run pipeline: `python src/fetch_data.py`
6. Run SQL from `queries/summary_query.sql` in BigQuery.

## Production Thinking
- Scheduling:
  - Cloud Scheduler + Cloud Run job (or cron for local/server).
- Monitoring:
  - Structured logs, job status checks, and failure alerts.
- Scaling (10x):
  - Partition BigQuery tables by date.
  - Use incremental loads based on last successful timestamp.
  - Add retries/backoff and data quality checks.
