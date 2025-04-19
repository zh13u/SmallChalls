FROM python:3.8-slim

RUN useradd -ms /bin/bash web

WORKDIR /app

RUN pip install --no-cache-dir Flask cryptography pyjwt

COPY . ./app

RUN chmod +x /app/*
RUN chmod 5 /app/app-backend.py

EXPOSE 5000

CMD ["python", "./app-backend.py"]
