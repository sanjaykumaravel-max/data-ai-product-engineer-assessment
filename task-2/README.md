# Task 2 - Pipeline Building

## Objective
Build a small but complete Python pipeline that uses a public API, transforms the data, loads it into BigQuery, and supports SQL analysis.

## Technical Workflow
`API -> Python -> Clean Data -> BigQuery -> SQL`

## Public API Choice
- API: Open-Meteo
- Reason: free, no API key required, structured hourly time-series response.

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
  - Run on schedule using Cloud Scheduler + Cloud Run job (or cron for local/server).
- Failure Detection:
  - Structured logs, non-zero exit on failure, alert on job failures.
- 10x Scale Plan:
  - Partition BigQuery table by date.
  - Move to incremental loads by last successful timestamp.
  - Add retries with exponential backoff for API calls.
  - Add data quality checks (row count thresholds, null-rate checks).
