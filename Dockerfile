FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
CMD ["python3", "main.py"]
