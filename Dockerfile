FROM python:3.9.2
WORKDIR /code
COPY ./ordermanager .
COPY ./requirements.txt .
RUN pip install -r /code/requirements.txt
CMD gunicorn ordermanager.wsgi:application --bind 0.0.0.0:8000
