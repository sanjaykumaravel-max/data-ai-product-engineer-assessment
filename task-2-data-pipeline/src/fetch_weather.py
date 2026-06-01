"""
Simple, beginner-friendly script to fetch weather data from Open-Meteo.

Features:
- Uses `requests`
- Parameterized latitude and longitude (via function and CLI)
- Proper error handling and logging
- Returns structured JSON data

See `__main__` example for usage.
"""

import argparse
import json
import logging
from typing import Any, Dict, Optional

import requests

# Basic logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def fetch_weather(latitude: float, longitude: float, hourly: Optional[str] = "temperature_2m", timezone: str = "UTC") -> Dict[str, Any]:
    """Fetch weather data from Open-Meteo API.

    Args:
        latitude: Latitude of the location (e.g., 51.5072).
        longitude: Longitude of the location (e.g., -0.1276).
        hourly: Comma-separated hourly variables to request (default: "temperature_2m").
        timezone: The timezone for the timestamps returned by the API (default: "UTC").

    Returns:
        A dictionary with structured weather data.

    Raises:
        requests.exceptions.RequestException on network-related errors.
        ValueError on unexpected API responses.
    """
    base_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly,
        "timezone": timezone,
    }

    logger.info("Requesting weather for lat=%s lon=%s hourly=%s", latitude, longitude, hourly)

    try:
        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        logger.error("Network or HTTP error when calling Open-Meteo: %s", exc)
        raise

    try:
        payload = resp.json()
    except ValueError as exc:
        logger.error("Failed to parse JSON response: %s", exc)
        raise

    # Basic validation of expected fields
    if not isinstance(payload, dict) or "hourly" not in payload:
        logger.error("Unexpected API response structure: missing 'hourly' field")
        raise ValueError("Unexpected API response structure")

    structured = {
        "request": {"latitude": latitude, "longitude": longitude, "hourly": hourly, "timezone": timezone},
        "metadata": {k: payload.get(k) for k in ("generationtime_ms", "utc_offset_seconds", "timezone", "timezone_abbreviation") if k in payload},
        "hourly": payload.get("hourly", {}),
    }

    logger.info("Successfully fetched weather data; hourly keys: %s", list(structured["hourly"].keys()))

    return structured


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch weather data from Open-Meteo API")
    parser.add_argument("--lat", "-a", type=float, required=True, help="Latitude, e.g., 51.5072")
    parser.add_argument("--lon", "-o", type=float, required=True, help="Longitude, e.g., -0.1276")
    parser.add_argument("--hourly", "-h", type=str, default="temperature_2m", help="Hourly fields (comma separated). Default: temperature_2m")
    parser.add_argument("--timezone", "-t", type=str, default="UTC", help="Timezone (default: UTC)")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    try:
        result = fetch_weather(latitude=args.lat, longitude=args.lon, hourly=args.hourly, timezone=args.timezone)
    except Exception as e:
        logger.error("Failed to fetch weather: %s", e)
        raise SystemExit(1)

    # Print nicely formatted JSON to stdout so callers can capture the output
    print(json.dumps(result, indent=2))
