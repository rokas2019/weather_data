from typing import Any, Dict, List, Union
from logging_config import LOGGER


def extract_data(json_response: Dict[str, Any]) -> List[Dict[str, Union[Dict[str, Any], List[Dict[str, Any]]]]]:
    """
    Extract daily and hourly forecast information from the API response.
    :param json_response: Dictionary representing the API response.
    :return: List of dictionaries containing extracted data.
    """

    # Validate the structure of json_response
    try:
        if 'forecast' not in json_response or 'forecastday' not in json_response['forecast']:
            LOGGER.error("Missing 'forecast' or 'forecastday' key in JSON response.")
            return []

        extracted_data = []

        for day_forecast in json_response['forecast']['forecastday']:
            daily_data = {
                'date': day_forecast['date'],
                'maxtemp_c': day_forecast['day'].get('maxtemp_c'),
                'mintemp_c': day_forecast['day'].get('mintemp_c'),
                'avgtemp_c': day_forecast['day'].get('avgtemp_c'),
            }

            hourly_data = []

            for hour_forecast in day_forecast['hour']:
                hour_info = {
                    'time': hour_forecast.get('time'),
                    'temp_celsius': hour_forecast.get('temp_c'),
                    'condition': hour_forecast['condition'].get('text'),
                    'wind_speed_kph': hour_forecast.get('wind_kph'),
                    'wind_direction': hour_forecast.get('wind_dir'),
                    'humidity': hour_forecast.get('humidity'),
                    'will_it_rain': hour_forecast.get('will_it_rain'),
                }

                hourly_data.append(hour_info)

            day_info = {
                'daily': daily_data,
                'hourly': hourly_data,
            }

            extracted_data.append(day_info)

        return extracted_data

    except KeyError as e:
        LOGGER.error(f"KeyError in JSON response: {e}")
        return []
