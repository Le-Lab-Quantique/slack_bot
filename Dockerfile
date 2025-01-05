FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1

LABEL authors="Le Lab Quantique"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3100

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:3100/health || exit 1

CMD ["gunicorn", "run:setup_web_app", "-c", "gunicorn.conf.py"]
