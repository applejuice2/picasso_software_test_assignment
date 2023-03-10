
### Тестовое задание для Picasso Software.
Задача - разработать API, для получения информации об инцидентах из базы данных.

### Реализовано
 - Команда для создания базы данных на основе CSV файла
 - Эндпоинт для получения информации о всех инцидентах, а также добавления нового
 - Фильтрация по Report Date (параметры date_from и date_to) и возможность ограничивать кол-во результатов по 20 шт. на страницу (параметр page)
 - Python-скрипт, загружающий данные из CSV в базу данных, создающий LOG-файл с выводом результата     работы скрипта
 - Кэширование страниц (скорость загрузки страницы увеличена в ~10 раз)
 - Подготовлен конфиг `docker-compose.yml` для развертывания контейнеров одной командой

### Технические детали
Технологии: Python, Django REST Framework, PostgreSQL (Django ORM), Redis, Docker / docker-compose. 

Пользователь может получить информацию об инцидентах `GET /api/v1/incidents/` и добавить новый инцидент `POST /api/v1/incidents/`. 

### Развертывание

Локальное развертывание в Linux (требует установленный Python 3.9, алгоритм может меняться в зависимости от ОС):

1. Склонировать репозиторий 
```
git clone https://github.com/applejuice2/picasso_software_test_assignment.git
```
2. Создать виртуальную среду и установить зависимости
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```
3. Создать файл **.env** в директории **infra** для использования переменных окружения(*пример .env файла в файле .env.example*)

4. Поднять контейнеры
```
docker-compose up
```
5. Запустить скрипт для загрузки данных в БД
```
cd scripts
```
```
python3 import_csv.py
```
6. Перейти в http://127.0.0.1:8000/
