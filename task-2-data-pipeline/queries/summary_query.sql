-- BigQuery Standard SQL
-- Uses the default selected GCP project.
-- If needed, change the FROM clause to: `your-project-id.marketing_pipeline.weather_hourly`

SELECT
  DATE(timestamp_utc) AS event_date,
  COUNT(*) AS hourly_records,
  ROUND(AVG(temperature_c), 2) AS avg_temp_c,
  MAX(temperature_c) AS max_temp_c,
  MIN(temperature_c) AS min_temp_c,
  ROUND(AVG(wind_speed_kmh), 2) AS avg_wind_kmh,
  COUNTIF(precipitation_mm > 0) AS rainy_hours
FROM `marketing_pipeline.weather_hourly`
GROUP BY event_date
ORDER BY event_date DESC;
