# Task 2 - Pipeline Building

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
  - API request failures are caught and raised with clear error context.
  - Unexpected payload shape (missing `hourly`) is validated and rejected.
  - Pipeline exits non-zero on failure for operational visibility.
- Parameterization:
  - Script behavior is driven by environment variables (`.env`) for project, dataset, table, coordinates, and date range.
  - Avoids hardcoded runtime values.
- Logging:
  - Pipeline logs start, transformation row count, and BigQuery load target.
  - Failures are logged with stack traces for debugging.
- Schema Design:
  - Explicit BigQuery schema includes typed fields for timestamp, measures, and derived columns.
  - Field names are clear and analytics-friendly.

## What This Pipeline Does
1. Fetch hourly weather data from Open-Meteo for configurable location/date range.
2. Transform nested JSON into a tabular dataset.
3. Clean nulls and type issues.
4. Add derived fields:
   - `is_rain_hour`
   - `temperature_band`
5. Load transformed rows to BigQuery.
6. Run SQL summary analysis.

## Project Structure
- `src/config.py` - environment/config values
- `src/extract.py` - API extraction with parameterization and error handling
- `src/transform.py` - flattening, cleaning, derived fields
- `src/load_bigquery.py` - dataset/table handling and BigQuery loading
- `src/main.py` - orchestration entrypoint
- `sql/summary_query.sql` - summary analysis query
- `requirements.txt` - dependencies
- `.env.example` - required environment variables

## How To Run
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set your values.
4. Authenticate GCP locally (for example with ADC):
   - `gcloud auth application-default login`
5. Run pipeline:
   - `python src/main.py`
6. Run SQL analysis from `sql/summary_query.sql` in BigQuery.

## BigQuery Setup Notes
- Use BigQuery Sandbox (free) with a Google account.
- Set:
  - `GOOGLE_CLOUD_PROJECT`
  - `BQ_DATASET`
  - `BQ_TABLE`
- The loader creates dataset if it does not exist and appends rows to table.

## SQL Analysis
`sql/summary_query.sql` provides daily record count, average temperature, average wind speed, and rainy-hour totals.

## Production Thinking
- Scheduling:
  - Run on a schedule using Cloud Scheduler + Cloud Run job (or cron for local/server).
- Monitoring:
  - Use structured logs, job run status, and alerts on failed runs.
  - Track row counts and freshness timestamps for data reliability.
- Scaling (10x):
  - Partition BigQuery table by date.
  - Switch to incremental loads using last-success timestamp.
  - Add retry/backoff strategy for API calls.
  - Add data quality checks (row-count thresholds, null-rate checks).
