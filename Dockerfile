FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN apt update && apt install -y build-essential

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./provet ./provet

EXPOSE 8000

CMD python provet/manage.py migrate && \
    python provet/manage.py runserver 0.0.0.0:8000