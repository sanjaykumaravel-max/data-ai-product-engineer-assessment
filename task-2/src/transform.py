import pandas as pd


def transform_weather_data(raw_data: dict) -> pd.DataFrame:
    hourly = raw_data.get("hourly", {})

    df = pd.DataFrame(
        {
            "timestamp_utc": hourly.get("time", []),
            "temperature_c": hourly.get("temperature_2m", []),
            "precipitation_mm": hourly.get("precipitation", []),
            "wind_speed_kmh": hourly.get("wind_speed_10m", []),
            "relative_humidity_pct": hourly.get("relative_humidity_2m", []),
        }
    )

    if df.empty:
        raise ValueError("No hourly data returned from API")

    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], errors="coerce")
    numeric_cols = ["temperature_c", "precipitation_mm", "wind_speed_kmh", "relative_humidity_pct"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["timestamp_utc"]).fillna(0)

    # Derived fields for basic analytics value.
    df["is_rain_hour"] = (df["precipitation_mm"] > 0).astype(int)
    df["temperature_band"] = pd.cut(
        df["temperature_c"],
        bins=[-100, 15, 25, 35, 100],
        labels=["cool", "mild", "warm", "hot"],
    ).astype(str)

    return df
