FROM python:3.13-slim

WORKDIR /auth

COPY ./auth/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./auth .
