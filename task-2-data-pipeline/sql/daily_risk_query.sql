-- Production-style BigQuery SQL: daily temperature + highest-risk weather insight
-- Replace `project.dataset.weather_table` with your table
WITH hourly AS (
  SELECT
    TIMESTAMP(timestamp_utc) AS timestamp_utc,
    DATE(TIMESTAMP(timestamp_utc)) AS day,
    SAFE_CAST(temperature_c AS FLOAT64)         AS temperature_c,
    COALESCE(SAFE_CAST(precipitation_mm AS FLOAT64), 0.0) AS precipitation_mm,
    COALESCE(SAFE_CAST(wind_speed_kmh AS FLOAT64), 0.0)   AS wind_speed_kmh,
    SAFE_CAST(relative_humidity_pct AS FLOAT64) AS relative_humidity_pct,
    LOWER(COALESCE(temperature_category, 'unknown')) AS temperature_category,
    LOWER(COALESCE(weather_risk_level, 'low'))       AS weather_risk_level
  FROM `project.dataset.weather_table`
  WHERE timestamp_utc IS NOT NULL
),

-- Compute a simple normalized risk score per hour
-- Weights: precipitation (50%), wind (30%), temperature extremes (20%)
hourly_risk AS (
  SELECT
    *,
    -- normalize precipitation: 0..1 for 0mm..10mm (cap at 1)
    LEAST(1.0, precipitation_mm / 10.0) AS norm_precip,
    -- normalize wind: 0..1 for 0km/h..30km/h (cap at 1)
    LEAST(1.0, wind_speed_kmh / 30.0)     AS norm_wind,
    -- temperature extreme flag (1 if hot/cold, else 0)
    CASE WHEN temperature_category IN ('hot','cold') THEN 1.0 ELSE 0.0 END AS temp_extreme_flag
  FROM hourly
),

hourly_with_score AS (
  SELECT
    timestamp_utc,
    day,
    temperature_c,
    precipitation_mm,
    wind_speed_kmh,
    relative_humidity_pct,
    temperature_category,
    weather_risk_level,
    -- weighted risk score between 0 and 1
    ROUND(0.50 * norm_precip + 0.30 * norm_wind + 0.20 * temp_extreme_flag, 4) AS risk_score,
    -- mark if this hour is considered 'high' by derived label or by score threshold
    CASE
      WHEN weather_risk_level = 'high' THEN 1
      WHEN 0.50 * norm_precip + 0.30 * norm_wind + 0.20 * temp_extreme_flag >= 0.6 THEN 1
      ELSE 0
    END AS is_high_risk_hour
  FROM hourly_risk
),

-- Aggregate to daily level and capture the single highest-risk hour for the day
daily_agg AS (
  SELECT
    day,
    COUNT(1) AS hours_observed,
    ROUND(AVG(temperature_c), 2) AS avg_temp_c,
    ROUND(STDDEV_POP(temperature_c), 2) AS temp_stddev_c,
    ROUND(MAX(temperature_c), 2) AS max_temp_c,
    ROUND(MIN(temperature_c), 2) AS min_temp_c,
    ROUND(SUM(precipitation_mm), 2) AS total_precip_mm,
    ROUND(MAX(wind_speed_kmh), 2) AS max_wind_kmh,
    SUM(is_high_risk_hour) AS high_risk_hours,
    ROUND(100.0 * SAFE_DIVIDE(SUM(is_high_risk_hour), COUNT(1)), 2) AS pct_high_risk_hours,
    ROUND(AVG(risk_score), 4) AS avg_risk_score,
    -- identify the single highest-risk hour (timestamp + score) for the day
    (ARRAY_AGG(STRUCT(timestamp_utc AS ts, risk_score) ORDER BY risk_score DESC, timestamp_utc ASC LIMIT 1))[OFFSET(0)].ts AS top_risk_timestamp,
    (ARRAY_AGG(STRUCT(timestamp_utc AS ts, risk_score) ORDER BY risk_score DESC, timestamp_utc ASC LIMIT 1))[OFFSET(0)].risk_score AS top_risk_score
  FROM hourly_with_score
  GROUP BY day
),

-- Add day-over-day temperature change and a seven-day rolling average for context
daily_final AS (
  SELECT
    day,
    hours_observed,
    avg_temp_c,
    temp_stddev_c,
    max_temp_c,
    min_temp_c,
    total_precip_mm,
    max_wind_kmh,
    high_risk_hours,
    pct_high_risk_hours,
    avg_risk_score,
    top_risk_timestamp,
    top_risk_score,
    ROUND(avg_temp_c - LAG(avg_temp_c) OVER (ORDER BY day), 2) AS avg_temp_change_c,
    ROUND(100.0 * SAFE_DIVIDE(avg_temp_c - LAG(avg_temp_c) OVER (ORDER BY day), LAG(avg_temp_c) OVER (ORDER BY day)), 2) AS avg_temp_pct_change,
    ROUND(AVG(avg_temp_c) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS rolling_7d_avg_temp_c
  FROM daily_agg
)

SELECT
  day,
  hours_observed,
  avg_temp_c,
  rolling_7d_avg_temp_c,
  avg_temp_change_c,
  avg_temp_pct_change,
  temp_stddev_c,
  total_precip_mm,
  max_wind_kmh,
  high_risk_hours,
  pct_high_risk_hours,
  avg_risk_score,
  top_risk_timestamp,
  top_risk_score
FROM daily_final
ORDER BY day DESC
LIMIT 365;
