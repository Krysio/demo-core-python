FROM python:3.11

WORKDIR /app

RUN pip install pytest-watch coincurve

CMD ptw -p