FROM python:3.9.5-slim-buster
COPY . /app
COPY requirements.txt requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]