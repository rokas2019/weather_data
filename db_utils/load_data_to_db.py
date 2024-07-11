import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from db_utils.models import CityDailyWeather, CityHourlyWeather, Base
from proj_var import ENGINE
from logging_config import LOGGER

# Setup SQLAlchemy session
Session = sessionmaker(bind=ENGINE)
session = Session()

# Ensure the tables are created
Base.metadata.create_all(ENGINE)


def load_daily_data(file_path: str, city: str) -> None:
    """
    Loads daily weather data from a CSV file into the database.

    :param file_path: Path to the CSV file containing daily weather data.
    :param city: Name of the city for which the data is being loaded.
    """
    try:
        df = pd.read_csv(file_path)
        daily_records = [
            CityDailyWeather(
                city=city,
                date=row['date'],
                maxtemp_c=row['max_temp_celsius'],
                mintemp_c=row['min_temp_celsius'],
                avgtemp_c=row['avg_temp_celsius']
            ) for _, row in df.iterrows()
        ]
        session.bulk_save_objects(daily_records)
        session.commit()
    except Exception as e:
        session.rollback()
        LOGGER.error(f"Error loading daily data from {file_path}: {e}")


def load_hourly_data(file_path: str, city: str) -> None:
    """
    Loads hourly weather data from a CSV file into the database.

    :param file_path: Path to the CSV file containing hourly weather data.
    :param city: Name of the city for which the data is being loaded.
    """
    try:
        df = pd.read_csv(file_path)
        hourly_records = [
            CityHourlyWeather(
                city=city,
                date=row['date_and_time'].split(' ')[0],
                hour=int(row['date_and_time'].split(' ')[1].split(':')[0]),
                temp_celsius=row['temp_celsius'],
                condition=row['condition'],
                wind_speed_kph=row['wind_speed_kph'],
                wind_direction=row['wind_direction'],
                humidity=row['humidity'],
                will_it_rain=row['will_it_rain']
            ) for _, row in df.iterrows()
        ]
        session.bulk_save_objects(hourly_records)
        session.commit()
    except Exception as e:
        session.rollback()
        LOGGER.error(f"Error loading hourly data from {file_path}: {e}")


def process_category_data(category: str, folder: str) -> None:
    """
    Processes data in a specified category and loads it into the database.

    :param category: Category of data (e.g., daily_forecast, hourly_forecast).
    :param folder: Path to the directory containing data files.
    """
    if not os.path.exists(folder):
        LOGGER.error(f"The directory '{folder}' does not exist.")
        return

    LOGGER.info(f"Processing {category} data in folder: {folder}")

    for file in os.listdir(folder):
        if file.endswith('.csv'):
            file_path = os.path.join(folder, file)
            city = file.split('_')[0]
            LOGGER.info(f"Processing file: {file} for city: {city}")

            if category.startswith('daily'):
                load_daily_data(file_path, city)
            elif category.startswith('hourly'):
                load_hourly_data(file_path, city)
            else:
                LOGGER.warning(f"Unknown category: {category}")


def process_data(directories: dict) -> None:
    """
    Processes directories containing weather data and loads it into the database.

    :param directories: Dictionary containing the paths to directories with weather data files.
    """
    for category in ["daily_forecast", "daily_historical", "hourly_forecast", "hourly_historical"]:
        folder = directories.get(category)
        if not folder:
            LOGGER.error(f"No directory specified for category: {category}")
            continue

        process_category_data(category, folder)

    LOGGER.info("Data loading completed.")