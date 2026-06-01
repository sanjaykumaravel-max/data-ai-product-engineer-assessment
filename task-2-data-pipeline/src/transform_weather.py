"""
Transform Open-Meteo JSON into a clean pandas DataFrame.

Usage:
    python task-2-data-pipeline/src/transform_weather.py --input sample.json

Functions:
- `transform_weather(json_data)`: core transformer, returns `pd.DataFrame`.
- CLI reads a JSON file (the structured output from `fetch_weather.py`) and prints a small preview.

The script keeps logic simple so it's easy to explain to beginners.
"""

from typing import Dict, Any, Optional
import argparse
import json
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def temperature_category(temp_c: Optional[float]) -> str:
    """Categorize temperature in Celsius into readable buckets.

    Rules (simple, easy to explain):
    - cold: temp <= 0
    - cool: 0 < temp <= 10
    - mild: 10 < temp <= 20
    - warm: 20 < temp <= 30
    - hot: temp > 30
    - unknown: if temp is None or NaN
    """
    if temp_c is None or (isinstance(temp_c, float) and pd.isna(temp_c)):
        return "unknown"
    try:
        t = float(temp_c)
    except (TypeError, ValueError):
        return "unknown"

    if t <= 0:
        return "cold"
    if t <= 10:
        return "cool"
    if t <= 20:
        return "mild"
    if t <= 30:
        return "warm"
    return "hot"


def weather_risk(row: pd.Series) -> str:
    """Derive a simple risk level based on temperature and common weather variables.

    - 'high' if heavy precipitation or very strong winds or extreme temperature
    - 'medium' for moderate precipitation, strong winds, or hot/cold
    - 'low' otherwise

    This function checks for common keys (precipitation, rain, snowfall, windspeed_10m).
    """
    # default
    risk = "low"

    # extreme temperature increases risk
    if row.get("temperature_category") in {"hot", "cold"}:
        risk = "medium"

    # precipitation checks
    precip_cols = [c for c in row.index if c.lower() in {"precipitation", "rain", "rain_sum", "snowfall", "snow_depth"}]
    for c in precip_cols:
        try:
            v = float(row.get(c))
        except Exception:
            continue
        if v > 5:
            return "high"
        if v > 0.5:
            risk = "medium"

    # wind check
    for wind_col in ("windspeed_10m", "wind_speed_10m", "windgusts_10m"):
        if wind_col in row.index:
            try:
                w = float(row.get(wind_col))
                if w > 20:
                    return "high"
                if w > 10 and risk != "high":
                    risk = "medium"
            except Exception:
                pass

    return risk


def transform_weather(json_data: Dict[str, Any]) -> pd.DataFrame:
    """Flatten and clean Open-Meteo structured JSON into a tidy DataFrame.

    Expects `json_data` to contain an `hourly` key with arrays (as returned
    by `fetch_weather.py`). The function will:
      - convert the hourly dict into a DataFrame
      - parse times to `datetime`
      - coerce numeric columns to proper numeric dtypes
      - handle nulls by using pandas `NA` and filling or preserving as needed
      - add `temperature_category` and `weather_risk_level`

    Returns a cleaned pandas DataFrame.
    """
    if not isinstance(json_data, dict):
        raise ValueError("json_data must be a dict")

    hourly = json_data.get("hourly")
    if not hourly or not isinstance(hourly, dict):
        raise ValueError("json_data must contain an 'hourly' dict with arrays")

    # Create DataFrame from the hourly dictionary of arrays
    df = pd.DataFrame(hourly)

    # Basic validation: ensure 'time' column exists
    if "time" not in df.columns:
        raise ValueError("Expected 'time' column in hourly data")

    # Parse time to datetime
    df["time"] = pd.to_datetime(df["time"], errors="coerce")

    # Convert all other columns to numeric when possible
    for col in df.columns:
        if col == "time":
            continue
        # Coerce to numeric; non-convertible values become NaN
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Handle nulls: for this simple pipeline we'll leave NaN where data is missing,
    # but we'll add an indicator column for rows that have missing temperature.
    df["temperature_missing"] = df.get("temperature_2m").isna()

    # Derived column: temperature_category based on `temperature_2m`
    df["temperature_category"] = df.get("temperature_2m").apply(temperature_category)

    # Derived column: weather_risk_level using row-wise rule function
    df["weather_risk_level"] = df.apply(weather_risk, axis=1)

    # Reorder columns for readability: time first, main weather cols, derived
    cols = ["time"] + [c for c in df.columns if c != "time" and c not in {"temperature_category", "weather_risk_level"}] + ["temperature_category", "weather_risk_level"]
    # Preserve only existing columns in that order
    cols = [c for c in cols if c in df.columns]
    df = df[cols]

    # Final small cleanup: sort by time if possible
    if not df["time"].isna().all():
        df = df.sort_values("time").reset_index(drop=True)

    logger.info("Transformed weather data: %d rows, %d columns", df.shape[0], df.shape[1])

    return df


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Transform Open-Meteo JSON into a clean DataFrame")
    p.add_argument("--input", "-i", required=True, help="Path to JSON file (structured output from fetch_weather.py)")
    p.add_argument("--preview", "-p", action="store_true", help="Print a small preview of the transformed DataFrame")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    with open(args.input, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    try:
        df = transform_weather(raw)
    except Exception as e:
        logger.error("Failed to transform weather data: %s", e)
        raise SystemExit(1)

    if args.preview:
        print(df.head().to_string(index=False))
    else:
        # Print a compact JSON-friendly representation of the first 5 rows
        print(df.head().to_json(orient="records", date_format="iso"))
