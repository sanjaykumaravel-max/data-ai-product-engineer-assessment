-- BigQuery Standard SQL
-- Replace the placeholders below with your project and dataset if needed.
-- Example: replace MY_PROJECT with my-gcp-project and MY_DATASET with marketing_pipeline
-- Then run this in BigQuery (the resulting fully-qualified table will be
-- `my-gcp-project.marketing_pipeline.weather_hourly`).

SELECT
  DATE(timestamp_utc) AS event_date,
  COUNT(*) AS hourly_records,
  ROUND(AVG(temperature_c), 2) AS avg_temp_c,
  ROUND(MAX(temperature_c), 2) AS max_temp_c,
  ROUND(MIN(temperature_c), 2) AS min_temp_c,
  ROUND(AVG(wind_speed_kmh), 2) AS avg_wind_kmh,
  SUM(CASE WHEN precipitation_mm > 0 THEN 1 ELSE 0 END) AS rainy_hours
-- BigQuery: use per-component backtick quoting to satisfy linters/editors that
-- don't recognize fully-backticked identifiers. This is valid in BigQuery.
FROM `weather-data-project`.marketing_pipeline.weather_hourly
GROUP BY event_date
ORDER BY event_date DESC;

-- If your SQL tooling flags the MY_PROJECT.MY_DATASET placeholder or does not
-- understand BigQuery's fully-qualified identifiers, replace the FROM clause
-- with a plain schema.table reference supported by your SQL engine, for example:
-- FROM marketing_pipeline.weather_hourly
