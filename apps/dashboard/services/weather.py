import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


WEATHER_CODE_LABELS = {
    0: "Ceu limpo",
    1: "Principalmente limpo",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Neblina",
    48: "Neblina com geada",
    51: "Garoa leve",
    53: "Garoa moderada",
    55: "Garoa intensa",
    61: "Chuva fraca",
    63: "Chuva moderada",
    65: "Chuva forte",
    80: "Pancadas leves",
    81: "Pancadas moderadas",
    82: "Pancadas fortes",
    95: "Temporal",
}


def get_current_weather():
    """Fetch current weather from Open-Meteo.

    The public dashboard should remain useful even if the external API is down,
    so callers receive a small fallback object instead of an exception.
    """
    weather_settings = settings.WEATHER
    params = {
        "latitude": weather_settings["latitude"],
        "longitude": weather_settings["longitude"],
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "timezone": weather_settings["timezone"],
    }

    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=5)
        response.raise_for_status()
        payload = response.json()
        current = payload.get("current", {})
        code = current.get("weather_code")
        return {
            "available": True,
            "city": weather_settings["city"],
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "description": WEATHER_CODE_LABELS.get(code, "Condicao indisponivel"),
            "updated_at": current.get("time"),
        }
    except (requests.RequestException, ValueError) as exc:
        logger.warning("Could not fetch weather data from Open-Meteo: %s", exc)
        return {
            "available": False,
            "city": weather_settings["city"],
            "temperature": None,
            "humidity": None,
            "wind_speed": None,
            "description": "Clima indisponivel",
            "updated_at": None,
        }
