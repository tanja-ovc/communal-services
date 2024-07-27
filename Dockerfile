FROM python:3.12-slim

RUN mkdir /app

COPY requirements.txt /app

RUN apt-get update

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY communal_services/ /app

WORKDIR /app

CMD ["gunicorn", "communal_services.wsgi:application", "--bind", "0:8000" ]