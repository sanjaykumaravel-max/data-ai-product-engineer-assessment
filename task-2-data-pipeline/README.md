# Weather Data Pipeline

## Project overview

This repository contains a lightweight Python pipeline to fetch weather data from Open-Meteo, transform it into a clean tabular format using pandas, and optionally load it into Google BigQuery. The project is intended as a production-ready reference implementation that is simple to understand and extend.

Key components:

- `src/fetch_weather.py` — fetches hourly forecasts from the Open-Meteo API.
- `src/transform_weather.py` — flattens and cleans Open-Meteo JSON into a tidy `pandas.DataFrame` and derives analytics columns.
- `src/load_bigquery.py` — loads a DataFrame to BigQuery with dataset/table creation and safe config.
- `src/transform_data.py` — convenience CLI that ties fetch → transform → load (or dry-run).
- `sql/daily_risk_query.sql` — production-style BigQuery query for daily averages and risk analysis.

## API selection reasoning

Open-Meteo was chosen for this project because:

- It provides free, programmatic hourly forecasts with a simple, well-documented REST API.
- No authentication is required for basic forecast retrieval, simplifying onboarding and CI tests.
- The API returns structured JSON ideal for direct ingestion and transformation with minimal parsing.

For production systems requiring higher SLAs or enterprise features, swap in a paid provider or a cached aggregation layer.

## Architecture overview

1. Fetch: call Open-Meteo (hourly variables) for a coordinate pair.
2. Transform: flatten the `hourly` arrays into a tidy DataFrame, coerce types, handle nulls, add derived columns (e.g., `temperature_category`, `weather_risk_level`).
3. Load (optional): write to BigQuery using `google-cloud-bigquery` with dataset/table creation and configurable write-disposition.
4. Analysis: run `sql/daily_risk_query.sql` in BigQuery for daily averages and high-risk day detection.

This design keeps compute close to the data and leverages BigQuery for analytics and storage.

## Setup instructions

Prerequisites

- Python 3.9+.
- Google Cloud SDK and Application Default Credentials (if loading to BigQuery).
- (Optional) A BigQuery project and billing account.

Local setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
```

2. Install dependencies:

```bash
pip install -r task-2-data-pipeline/requirements.txt
```

Note: The repository already includes `requests`, `pandas`, and `google-cloud-bigquery` in `task-2-data-pipeline/requirements.txt`.

## How to run the pipeline

Dry-run (fetch + transform only):

```bash
python task-2-data-pipeline/src/transform_data.py --latlon 51.5072 -0.1276 --dry-run
```

Fetch, transform, and load to BigQuery:

```bash
python task-2-data-pipeline/src/transform_data.py \
  --latlon 51.5072 -0.1276 \
  --project YOUR_PROJECT --dataset YOUR_DATASET --table YOUR_TABLE
```

Or, if you already have a JSON response captured by `fetch_weather.py`:

```bash
python task-2-data-pipeline/src/transform_data.py --input /path/to/fetch_output.json --project ...
```

## BigQuery setup

1. Enable the BigQuery API and ensure billing is configured for your GCP project.
2. Grant the service account or user the `roles/bigquery.dataEditor` and `roles/bigquery.dataOwner` as needed.
3. Ensure Application Default Credentials are available locally or in the environment where the pipeline runs:

```bash
gcloud auth application-default login
```

4. Table design guidance:

- Partition by `DATE(timestamp_utc)` (ingestion or event) to reduce query costs and improve pruning.
- Use clustering (e.g., on `temperature_category` or `location_id`) for common filter patterns.
- Use meaningful column names and stable types; prefer `TIMESTAMP` for time-of-event fields and numeric types for sensors.

## SQL analysis query

An example production-style query is provided at `task-2-data-pipeline/sql/daily_risk_query.sql`.
It computes:

- Daily average temperature, min/max, and standard deviation.
- A transparent per-hour `risk_score` and aggregated daily `avg_risk_score`.
- `top_risk_timestamp` and `top_risk_score` per day to identify the worst hours.
- Percent of high-risk hours and 7-day rolling average for trend context.

Usage: replace `project.dataset.weather_table` in the SQL file and run in BigQuery.

## Production scaling considerations

- Data volume and cadence: For high-frequency ingestion (sub-hourly or many locations), consider batching and using a message bus (Pub/Sub) for ingestion.
- Batch vs streaming: Streaming ingest into BigQuery is possible (streaming inserts) but incurs cost and requires careful idempotency handling; for many use-cases, micro-batches (5–15 min) are a good compromise.
- Partitioning & clustering: Partition on date, and cluster on high-cardinality filter columns to optimize scan costs and performance.
- Schema evolution: Use explicit schema migrations and compatibility checks; avoid schema-on-write anti-patterns without governance.
- Cost controls: enforce partition expiration, use table decorators for backfilling, and monitor query costs.

## Monitoring and scheduling ideas

- Scheduling: use Cloud Scheduler + Cloud Functions or Airflow (Cloud Composer) to schedule pipeline runs. For local/CI testing, `cron` or task schedulers suffice.
- Observability: emit structured logs (INFO/ERROR) and expose metrics:
  - `rows_ingested`, `load_duration_seconds`, `last_success_timestamp`, `error_count`.
- Alerts: set up alerts for job failures, high error rates, or sudden drops in data volume (e.g., with Cloud Monitoring).
- Tracing: add request IDs and correlate logs across fetch → transform → load stages to simplify root cause analysis.

## Testing, CI/CD, and security

- Unit tests: mock external API and BigQuery clients to validate transform and load logic (there is a sample test for the loader in `task-2-data-pipeline/tests`).
- CI: run linters, unit tests, and a smoke dry-run in CI; avoid running live BigQuery loads in PR pipelines unless using a test project.
- Secrets: do not store credentials in the repo. Use Secret Manager or environment-managed credentials in CI/CD.

## Next steps / extensions

- Add location metadata (city, region) and store per-location tables with a `location_id` key.
- Add more derived metrics (heat index, wind chill) and translate business rule thresholds into a config file.
- Introduce a dashboard (Looker/Looker Studio) that consumes the BigQuery table for visual monitoring and reporting.

---

If you want, I can also open a PR with this README, add CI pipeline examples, or create a Helm/Cloud Run deployment manifest to run the pipeline serverlessly. What would you like next?
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
