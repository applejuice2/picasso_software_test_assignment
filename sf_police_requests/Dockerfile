FROM python:3.9-slim
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev build-essential
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["python3", "manage.py", "runserver", "0:8000"]