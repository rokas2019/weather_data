import csv
import os
from typing import List, Any
from extraction_utils.fetch_data import get_weather_data
import logging

# Get the logger
logger = logging.getLogger()


def save_to_csv(filename: str, headers: List[str], rows: List[List[Any]]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
    logger.info(f"Data saved to {filename}")


def save_hourly_data(cities: List[str], days: int, future: bool = False) -> None:
    data_type = "forecast" if future else "historical"
    folder = "hourly_data"

    for city in cities:
        data = get_weather_data(city, days, future=future)

        if data:
            rows = []
            for day in data:
                for hour in day['hourly']:
                    rows.append([
                        hour['time'],
                        hour['temp_celsius'],
                        hour['condition'],
                        hour['wind_speed_kph'],
                        hour['wind_direction'],
                        hour['humidity'],
                        hour['will_it_rain']
                    ])

            csv_filename = f"{folder}/{data_type}/{city}_hourly_{data_type}.csv".lower()
            headers = ['date_and_time', 'temp_celsius', 'condition', 'wind_speed_kph', 'wind_direction', 'humidity',
                       'will_it_rain']
            logger.info(f"Saving hourly data for {city} ({data_type}) to {csv_filename}")
            save_to_csv(csv_filename, headers, rows)
        else:
            logger.warning(f"No hourly data to save for {city} ({data_type})")


def save_daily_data(cities: List[str], days: int, future: bool = False) -> None:
    data_type = "forecast" if future else "historical"
    folder = "daily_data"

    for city in cities:
        data = get_weather_data(city, days, future=future)

        if data:
            rows = []
            for day in data:
                daily_data = day['daily']
                rows.append([
                    daily_data['date'],
                    daily_data['maxtemp_c'],
                    daily_data['mintemp_c'],
                    daily_data['avgtemp_c']
                ])

            csv_filename = f"{folder}/{data_type}/{city}_daily_{data_type}.csv".lower()
            headers = ['date', 'max_temp_celsius', 'min_temp_celsius', 'avg_temp_celsius']
            logger.info(f"Saving daily data for {city} ({data_type}) to {csv_filename}")
            save_to_csv(csv_filename, headers, rows)
        else:
            logger.warning(f"No daily data to save for {city} ({data_type})")
