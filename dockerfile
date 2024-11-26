FROM python:3.13-slim
#FROM alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV ENV_FILE_PATH=/.env

CMD ["python", "src/main.py"]
