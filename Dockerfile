FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src

RUN mkdir -p /app/logs

EXPOSE 8000

CMD ["uvicorn","src.main:app","--host","0.0.0.0","--port","8000"]