# Weather Data System

The objective of this project is to automate the acquisition, storage, and analysis of hourly weather data for the twenty largest cities in Europe.

## Key Tasks

1. **Data Acquisition:**
    - Retrieve hourly weather data from an external API for the twenty largest cities in Europe.
    - Collect both historical and forecasted weather data to ensure comprehensive coverage.

2. **Data Processing:**
    - Process and clean the retrieved data to ensure accuracy and consistency.
    - Create views and aggregate functions within the database for efficient data analysis.

3. **Data Storage:**
    - Store the acquired weather data in a structured SQL database.
    - Design and maintain database tables to effectively manage and query the data.

4. **Task Scheduling:**
    - Implement a task scheduler to run the data acquisition and processing scripts at scheduled intervals.
    - Ensure the automation of data retrieval and storage to keep the database up-to-date with the latest weather information.

## Project Workflow

1. **Setup Environment:**
    - Set up the necessary Python environment and dependencies.
    - Configure the SQL database connection.

2. **Data Retrieval:**
    - Utilize Python scripts to fetch weather data from the API.
    - Parse and extract relevant information from the API responses.

3. **Data Ingestion:**
    - Load the extracted data into the SQL database.
    - Ensure data integrity and handle potential errors during the ingestion process.

4. **Automation:**
    - Schedule the Python scripts to run automatically at specified times using task scheduling tools.
    - Ensure the scheduler is correctly configured to handle different time intervals for historical and forecasted data.

## Setup Instructions

Follow these steps to set up and run the project:

1. Clone the Repository:
    ```bash
    git clone https://github.com/TuringCollegeSubmissions/rgaldi-DE2v2.2.5
    ```
2. Navigate to the project directory:
    ```bash
    cd rgaldi-DE2v2.2.5
    ```
3. Set Up Database Connection Settings:
    - Create a file named `db_conn_settings.py` in the root directory of the project.
    - Inside this file, define the following variables with your database connection details:

    ```python
    # db_conn_settings.py
    DB_USERNAME = "your_database_username"
    DB_PASSWORD = "your_database_password"
    DB_HOST = "your_database_host"
    DB_PORT = "your_database_port"
    DB_NAME = "your_database_name"
    ```

4. Define project variables:
    ```python
    # proj_var.py
    import os
    from db_conn_settings import DB_NAME, DB_PORT, DB_HOST, DB_PASSWORD, DB_USERNAME
    from sqlalchemy import create_engine

    ENGINE = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    DAYS = 7
    BASE_PATH = 'YOUR_PATH/rgaldi-DE2v2.2.5'

    WEATHER_H_URL = 'http://api.weatherapi.com/v1/history.json'
    WEATHER_F_URL = 'http://api.weatherapi.com/v1/forecast.json'
    W_API_KEY = 'YOUR_API_KEY'

    DIRECTORIES = {
        "daily_forecast": os.path.join(BASE_PATH, 'daily_data', 'forecast'),
        "daily_historical": os.path.join(BASE_PATH, 'daily_data', 'historical'),
        "hourly_forecast": os.path.join(BASE_PATH, 'hourly_data', 'forecast'),
        "hourly_historical": os.path.join(BASE_PATH, 'hourly_data', 'historical'),
    }

    LIST_OF_CITIES = [
        'Istanbul', 'London', 'Saint Petersburg', 'Berlin', 'Madrid', 'Kyiv', 'Rome', 'Bucharest',
        'Paris', 'Minsk', 'Vienna', 'Warsaw', 'Hamburg', 'Budapest', 'Belgrade', 'Barcelona',
        'Munich', 'Kharkiv', 'Milan'
    ]
    ```

5. Install Dependencies:
    - Ensure you have Python and pip installed.
    - Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Run the `main.py` script to execute the project:
    ```bash
    python main.py
    ```

7. Set up logging in `logging_config.py`.

8. Follow the instructions and messages printed to the logging file for further guidance.

## ERD
![ERD](Images/Screenshot1.png)

## Views
![Views](Images/Screenshot2.png)

## Task Scheduler Set-up

1. **Create Task:**
    ![Create Task](Images/Screenshot3.png)

2. **Name the Task:**
    ![Name Task](Images/Screenshot4.png)

3. **Schedule the Task:**
    ![Schedule Task](Images/Screenshot5.png)

4. **Find your Python Path:**
    ![Python Path](Images/Screenshot6.png)

5. **Configure the Task:**
    - Enter your Python path (program/script).
    - Enter the path to `main.py` (Add arguments).
    ![Configure Task](Images/Screenshot7.png)
