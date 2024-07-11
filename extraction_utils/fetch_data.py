from datetime import datetime, timedelta
from typing import Any, Dict, List, Union
from extraction_utils.data_extraction import extract_data
from extraction_utils.get_responses import get_h_response, get_f_response
from logging_config import LOGGER


def get_weather_data(city: str, days: int, future: bool = False) -> \
        List[Dict[str, Union[Dict[str, Any], List[Dict[str, Any]]]]]:
    today = datetime.now()
    all_data = []

    try:
        if future:
            date = days
            response = get_f_response(city, date)
            if response:
                LOGGER.info(f"Forecast response for {city} on {date} received.")
                extracted_data = extract_data(response)
                LOGGER.info(f"Extracted forecast data for {city} on {date}: {extracted_data}")
                all_data.extend(extracted_data)
            else:
                LOGGER.warning(f"No forecast data found for {city} on {date}")
        else:
            for i in range(1, days + 1):  # Start from 1 to exclude today
                date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
                response = get_h_response(city, date)
                if response:
                    LOGGER.info(f"Historical response for {city} on {date} received.")
                    extracted_data = extract_data(response)
                    LOGGER.info(f"Extracted historical data for {city} on {date}: {extracted_data}")
                    all_data.extend(extracted_data)
                else:
                    LOGGER.warning(f"No historical data found for {city} on {date}")

    except Exception as e:
        LOGGER.error(f"Error in fetching weather data: {e}")

    return all_data
