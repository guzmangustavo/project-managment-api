FROM python:3.12-slim

WORKDIR /app

RUN apt-get clean && apt-get update && apt-get install -y --no-install-recommends \ 
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 8000