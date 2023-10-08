FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

RUN adduser \
    --disabled-password \
    --no-create-home \
    fastapi-user

USER fastapi-user
