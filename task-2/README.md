# Task 2 - Pipeline Building

## Objective
Build a small but complete Python data pipeline that fetches data from a public API, transforms it, and loads it into BigQuery.

## API Choice
- **Open-Meteo** (no API key required)
- Why: stable public endpoint, structured JSON, and clear time-series fields suitable for transformation.

## v1 Pipeline Scope
1. Fetch hourly weather data from Open-Meteo for a configurable location and date range.
2. Transform nested JSON into a tabular dataset.
3. Add derived analytical fields (for example temperature bucket and precipitation flag).
4. Load transformed rows into a BigQuery table.
5. Provide a SQL query for a meaningful summary.

## Project Structure
- `src/config.py` - environment/config handling
- `src/extract.py` - API extraction with logging and error handling
- `src/transform.py` - normalization and derived fields
- `src/load_bigquery.py` - BigQuery table creation and load
- `src/main.py` - orchestration entrypoint
- `sql/summary_query.sql` - analysis query on loaded data
- `requirements.txt` - Python dependencies
- `.env.example` - required environment variables

## How To Run (planned)
1. Create virtual environment and install dependencies.
2. Configure `.env` with BigQuery project/dataset/table values.
3. Run `python src/main.py`.
4. Run `sql/summary_query.sql` in BigQuery.

## Production Thinking (to finalize)
- Scheduling: cron / Cloud Scheduler + Cloud Run/Functions
- Failure detection: structured logs + alerting on run status
- Scale path: partitioned tables, incremental loads, retry/backoff
