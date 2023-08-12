FROM python:3.11 as base

WORKDIR /app

COPY . .

RUN pip install pytest-watch coincurve
