FROM python:3.15.5
LABEL authors="Kayky"

WORKDIR /app

COPY . .

EXPOSE 5000

RUN pip install uv && uv sync && python /backend/routes.py



