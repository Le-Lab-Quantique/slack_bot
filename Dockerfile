FROM python:slim-buster AS build
ENV PYTHONUNBUFFERED 1

LABEL authors="Le Lab Quantique"

WORKDIR  /app

ENV ENV=production
ENV FLASK_APP=src


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5005

CMD ["gunicorn", "run:app" ,"-c" ,"gunicorn.conf.py" ]