from db_utils.load_data_to_db import process_data
from extraction_utils.write_to_csv import save_daily_data, save_hourly_data
from logging_config import LOGGER
from proj_var import ENGINE, LIST_OF_CITIES, DAYS, DIRECTORIES
from db_utils.execute_queries import create_views

if __name__ == "__main__":
    LOGGER.info("Starting data retrieval process.")

    LOGGER.info("Saving future daily data.")
    save_daily_data(LIST_OF_CITIES, DAYS, future=True)

    LOGGER.info("Saving future hourly data.")
    save_hourly_data(LIST_OF_CITIES, DAYS, future=True)

    LOGGER.info("Saving historical daily data.")
    save_daily_data(LIST_OF_CITIES, DAYS, future=False)

    LOGGER.info("Saving historical hourly data.")
    save_hourly_data(LIST_OF_CITIES, DAYS, future=False)

    LOGGER.info("Data retrieval process completed.")

    LOGGER.info("Loading data to the database.")
    process_data(DIRECTORIES)

    create_views()
    ENGINE.dispose()


