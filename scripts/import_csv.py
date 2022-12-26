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
CSV_FILE_NAME = getenv('CSV_FILE_NAME')
PATH_TO_CSV = f'/var/lib/postgresql/{CSV_FILE_NAME}'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('import_csv.log', mode='a')
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


def import_csv_to_db(connection, path_to_csv):
    """Импортирует данные из CSV в БД."""
    logger.info('Начинаю импорт CSV-файла в БД')
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SET TIMEZONE TO UTC;""")

            cursor.execute(f"""SELECT COUNT(*)
                                FROM {TABLE_NAME};""")
            start_number_of_records = cursor.fetchone()[0]

            cursor.execute(f"""COPY {TABLE_NAME}
                                   FROM '{path_to_csv}'
                                      (FORMAT 'csv',
                                       DELIMITER ',',
                                       NULL '',
                                       QUOTE '"',
                                       HEADER);
                        """)

            cursor.execute(f"""SELECT COUNT(*)
                               FROM {TABLE_NAME};""")

            imported_number_of_records = cursor.fetchone()[0] - start_number_of_records
        logger.info('CSV-файл импортирован в БД успешно. '
                    f'Количество созданных записей: {imported_number_of_records}')
        return connection
    except Exception as error:
        raise Exception(f'Ошибка при импорте CSV-файла в таблицу: {error}')


def main():
    """Основная логика работы скрипта по импорту из CSV в БД."""
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
            connection = import_csv_to_db(connection, PATH_TO_CSV)

        except Exception as error:
            logger.error(f'{error}')

        finally:
            if connection:
                connection.close()
                logger.info('Подключение к БД завершено')
    logger.info(f'Время работы скрипта: {timer.time_of_program}')


if __name__ == '__main__':
    main()
