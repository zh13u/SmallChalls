FROM python:3.8-slim

RUN useradd -ms /bin/bash web

WORKDIR /app

RUN pip install --no-cache-dir Flask asyncio aiohttp uuid

COPY . ./app

RUN chmod +x /app/*
RUN chmod 5 /app/app.py

EXPOSE 4505

CMD ["python", "./app/app.py"]
