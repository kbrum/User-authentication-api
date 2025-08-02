FROM python:3.13.5
LABEL authors="Kayky"

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv && uv sync

COPY . .

EXPOSE 5000

CMD ["python", "routes.py"]

