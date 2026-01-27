FROM python:3.11-slim

# чтобы логи сразу писались в stdout
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем код и ключ
COPY bot.py .
COPY creds.json .

# команда запуска
CMD ["python", "bot.py"]
