-- BigQuery Standard SQL
-- Make sure the editor is using Standard SQL, not Legacy SQL.
-- If your BigQuery project differs, replace the dataset/table path with your full project ID.

SELECT
  DATE(timestamp_utc) AS weather_date,
  COUNT(*) AS hourly_records,
  ROUND(AVG(temperature_c), 2) AS avg_temperature_c,
  ROUND(AVG(wind_speed_kmh), 2) AS avg_wind_speed_kmh,
  COUNTIF(precipitation_mm > 0) AS rainy_hours
FROM `marketing_pipeline.weather_hourly`
GROUP BY weather_date
ORDER BY weather_date DESC;

