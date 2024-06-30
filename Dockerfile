FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p /app/db

EXPOSE 8080

CMD ["python", "main.py"]
