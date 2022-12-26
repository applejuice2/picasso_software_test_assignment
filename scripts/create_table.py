from sys import path
from os import path as os_path, getenv
import logging

import psycopg2
from dotenv import load_dotenv

from context_manager.program_time import ProgramExecutionTime

env_path = os_path.join(path[0], '..', 'infra','.env')
load_dotenv(env_path)

DB_HOST = getenv('HOST_ADRESS')
DB_PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')
POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
TABLE_NAME = getenv('TABLE_NAME')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('create_table.log', mode='a')
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)


def check_parameters(host, port, name, user, password):
    """
    Проверяет доступность переменных окружения.
    (которые необходимы для подключения к БД).
    """
    logger.info('Начинаю проверку переменных окружения')
    if all([host, port, name, user, password]):
        logger.info('Наличие переменных окружения проверено успешно')
        return host, port, name, user, password
    else:
        raise Exception('Необходимо проверить наличие переменных'
                        'окружения для подключения к БД')


def connect_to_db(host, port, name, user, password):
    """Создаёт подключение к БД с автокоммитом."""
    logger.info('Подключаюсь к БД')
    try:
        connection = psycopg2.connect(host=host,
                                      port=port,
                                      database=name,
                                      user=user,
                                      password=password)
        connection.autocommit = True
        logger.info('Подключение к БД создано')
        return connection
    except Exception as error:
        raise Exception(f'Ошибка при подключении к БД: {error}')


def create_table(connection):
    """Создаёт таблицу в БД."""
    logger.info('Начинаю создание таблицы в БД')
    try:
        with connection.cursor() as cursor:
            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                id                       INTEGER,
                original_crime_type_name VARCHAR(50) NOT NULL,
                report_date              TIMESTAMP   NOT NULL,
                call_date                TIMESTAMP   NOT NULL,
                offense_date             TIMESTAMP   NOT NULL,
                call_time                TIME        NOT NULL,
                call_date_time           TIMESTAMP   NOT NULL,
                disposition              VARCHAR(12) NOT NULL,
                adress                   VARCHAR(50) NOT NULL,
                city                     VARCHAR(50),
                state                    VARCHAR(50) NOT NULL,
                agency_id                INTEGER,
                adress_type              VARCHAR(50) NOT NULL,
                common_location          VARCHAR(50),
                                         CONSTRAINT PK_{TABLE_NAME}_id        PRIMARY KEY (id),
                                         CONSTRAINT VALID_NUMBER_{TABLE_NAME}_id
                                         CHECK (id BETWEEN 1 AND 999999999)
                                       /*CONSTRAINT FK_{TABLE_NAME}_id FOREIGN KEY (agency_id)*/
            );
            ''')

        logger.info('Таблица в БД создана успешно')
        return connection
    except Exception as error:
        raise Exception(f'Ошибка при создании таблицы: {error}')


def main():
    """Основная логика работы скрипта по созданию таблицы в БД."""
    with ProgramExecutionTime() as timer:
        try:
            connection = False
            host, port, name, user, password = check_parameters(
                DB_HOST,
                DB_PORT,
                DB_NAME,
                POSTGRES_USER,
                POSTGRES_PASSWORD
                )
            connection = connect_to_db(host, port, name, user, password)
            connection = create_table(connection)

        except Exception as error:
            logger.error(f'{error}')

        finally:
            if connection:
                connection.close()
                logger.info('Подключение к БД завершено')
    logger.info(f'Время работы скрипта: {timer.time_of_program}')


if __name__ == '__main__':
    main()
