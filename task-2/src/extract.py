import logging
from typing import Dict, Any

import requests


logger = logging.getLogger(__name__)


def fetch_weather_data(latitude: float, longitude: float, start_date: str, end_date: str, timezone: str) -> Dict[str, Any]:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m",
        "timezone": timezone,
    }

    logger.info("Requesting Open-Meteo data", extra={"params": params})

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        logger.exception("API request failed")
        raise RuntimeError(f"Failed to fetch weather data: {exc}") from exc

    if "hourly" not in data:
        raise ValueError("Unexpected API response: missing 'hourly' field")

    return data
