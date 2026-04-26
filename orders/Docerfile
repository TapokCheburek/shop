FROM python:3.13-slim


RUN pip install --no-cache-dir poetry==2.0.0

WORKDIR /products

COPY pyproject.toml poetry.lock ./
COPY ./products .

RUN poetry install --no-root
