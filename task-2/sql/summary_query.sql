SELECT
  DATE(timestamp_utc) AS event_date,
  COUNT(*) AS hourly_records,
  ROUND(AVG(temperature_c), 2) AS avg_temp_c,
  ROUND(AVG(wind_speed_kmh), 2) AS avg_wind_kmh,
  SUM(CASE WHEN precipitation_mm > 0 THEN 1 ELSE 0 END) AS rainy_hours
FROM `your-project-id.marketing_pipeline.weather_hourly`
GROUP BY event_date
ORDER BY event_date DESC;
