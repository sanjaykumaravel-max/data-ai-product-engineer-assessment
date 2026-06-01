-- BigQuery Standard SQL
-- Replace the placeholders below with your project and dataset.
-- Example: replace MY_PROJECT with my-gcp-project and MY_DATASET with marketing_pipeline
-- Then run this in BigQuery (the resulting fully-qualified table will be
-- `my-gcp-project.marketing_pipeline.weather_hourly`).

SELECT
  DATE(timestamp_utc) AS event_date,
  COUNT(*) AS hourly_records,
  ROUND(AVG(temperature_c), 2) AS avg_temp_c,
  MAX(temperature_c) AS max_temp_c,
  MIN(temperature_c) AS min_temp_c,
  ROUND(AVG(wind_speed_kmh), 2) AS avg_wind_kmh,
  SUM(CASE WHEN precipitation_mm > 0 THEN 1 ELSE 0 END) AS rainy_hours
FROM `YOUR_PROJECT_ID.YOUR_DATASET.weather_hourly`
GROUP BY event_date
ORDER BY event_date DESC;

-- If your SQL tooling flags the MY_PROJECT.MY_DATASET placeholder or does not
-- understand BigQuery's fully-qualified identifiers, replace the FROM clause
-- with a plain schema.table reference supported by your SQL engine, for example:
-- FROM marketing_pipeline.weather_hourly
