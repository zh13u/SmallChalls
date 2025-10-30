FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/
COPY templates/ /app/templates/
COPY static/ /app/static/
COPY flag.txt /flag.txt

RUN apt-get update \
 && apt-get install -y --no-install-recommends iputils-ping \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask
EXPOSE 2001
CMD ["python", "app.py"]