from typing import Dict, Any
import requests
from proj_var import WEATHER_H_URL, W_API_KEY, WEATHER_F_URL
from logging_config import LOGGER


def get_h_response(city: str, date: str) -> Dict[str, Any]:
    try:
        req = f'{WEATHER_H_URL}?key={W_API_KEY}&q={city}&dt={date}'
        LOGGER.info(f"Fetching historical data: {req}")
        response = requests.get(req)
        response.raise_for_status()
        LOGGER.info(f"Response received for historical data: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        LOGGER.error(f"Error fetching historical data: {e}")
    return {}


def get_f_response(city: str, date: int) -> Dict[str, Any]:
    try:
        req = f'{WEATHER_F_URL}?key={W_API_KEY}&q={city}&days={date}&aqi=no&alerts=no'
        LOGGER.info(f"Fetching forecast data: {req}")
        response = requests.get(req)
        response.raise_for_status()
        LOGGER.info(f"Response received for forecast data: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        LOGGER.error(f"Error fetching forecast data: {e}")
    return {}
