FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --system

COPY . /app/

# Add args to be able to collectstatic as 
# heroku config vars not available during build time

ARG SECRET_KEY
ARG DEBUG
ARG JWT_ALGORITHM
ARG JWT_SECRET_KEY
ARG REDIS_URL

RUN python manage.py collectstatic --noinput