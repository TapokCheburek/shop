FROM python:3.13-slim


RUN pip install --no-cache-dir poetry==2.0.0

WORKDIR /orders

COPY pyproject.toml poetry.lock ./
COPY ./orders .

RUN poetry install --no-root
