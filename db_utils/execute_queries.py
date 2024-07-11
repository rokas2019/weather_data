import os
from sqlalchemy import text
from proj_var import ENGINE
from logging_config import LOGGER


def execute_sql_file(engine, file_path):
    """
    Execute the SQL commands in the specified file.

    :param engine: SQLAlchemy engine object
    :param file_path: Path to the SQL file
    """
    with open(file_path, 'r') as file:
        sql_commands = file.read()

    with engine.connect() as connection:
        trans = connection.begin()
        try:
            for command in sql_commands.split(';'):
                command = command.strip()
                if command:
                    LOGGER.debug(f"Executing command: {command}")
                    connection.execute(text(command))
            trans.commit()
            LOGGER.info("Transaction committed successfully.")
        except Exception as e:
            trans.rollback()
            LOGGER.error(f"Error executing command: {command}\n{e}")
        finally:
            engine.dispose()


def create_views():
    """
    Create all the views by executing the SQL file.
    """
    try:
        sql_file_path = os.path.join(os.path.dirname(__file__), 'create_views.sql')
        execute_sql_file(ENGINE, sql_file_path)
        LOGGER.info('Views created successfully.')
    except Exception as e:
        LOGGER.error(f"Error creating views: {e}")
