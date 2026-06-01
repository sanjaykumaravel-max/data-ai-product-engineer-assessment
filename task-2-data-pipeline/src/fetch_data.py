"""Simple Open-Meteo weather fetch script.

This script is intentionally beginner-friendly:
- uses requests
- logs what it is doing
- validates inputs
- handles common API errors
- returns structured JSON data
"""

import argparse
import json
import logging
from typing import Any, Dict

import requests


API_URL = "https://api.open-meteo.com/v1/forecast"

# Basic logging setup for visibility when running the script.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def fetch_weather_data(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
    timezone: str = "auto",
) -> Dict[str, Any]:
    """Fetch weather data from Open-Meteo and return structured JSON.

    Args:
        latitude: Decimal latitude (between -90 and 90).
        longitude: Decimal longitude (between -180 and 180).
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
        timezone: Timezone for returned timestamps. Default is "auto".

    Returns:
        A dictionary parsed from the API JSON response.
    """
    if not (-90 <= latitude <= 90):
        raise ValueError("latitude must be between -90 and 90")
    if not (-180 <= longitude <= 180):
        raise ValueError("longitude must be between -180 and 180")

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m",
        "timezone": timezone,
    }

    logger.info("Calling Open-Meteo API", extra={"latitude": latitude, "longitude": longitude})

    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.Timeout as exc:
        logger.exception("Request timed out")
        raise RuntimeError("Open-Meteo request timed out") from exc
    except requests.RequestException as exc:
        logger.exception("Request failed")
        raise RuntimeError(f"Open-Meteo request failed: {exc}") from exc
    except json.JSONDecodeError as exc:
        logger.exception("Invalid JSON returned by API")
        raise RuntimeError("Open-Meteo returned invalid JSON") from exc

    # Validate expected structure before returning.
    if "hourly" not in data:
        raise ValueError("Unexpected API response: missing 'hourly' field")

    logger.info("Weather data fetched successfully")
    return data


def main() -> None:
    """Run from command line with configurable coordinates."""
    parser = argparse.ArgumentParser(description="Fetch weather data from Open-Meteo")
    parser.add_argument("--latitude", type=float, required=True, help="Latitude (e.g., 12.9716)")
    parser.add_argument("--longitude", type=float, required=True, help="Longitude (e.g., 77.5946)")
    parser.add_argument("--start-date", type=str, required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end-date", type=str, required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--timezone", type=str, default="auto", help="Timezone (default: auto)")
    args = parser.parse_args()

    weather_json = fetch_weather_data(
        latitude=args.latitude,
        longitude=args.longitude,
        start_date=args.start_date,
        end_date=args.end_date,
        timezone=args.timezone,
    )

    # Print a small preview to confirm the response shape.
    logger.info("Top-level response keys: %s", list(weather_json.keys()))


if __name__ == "__main__":
    main()
