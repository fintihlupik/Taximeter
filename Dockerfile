FROM python:3.9-slim

WORKDIR /app

COPY . /app

ENV PYTHONIOENCODING=UTF-8

CMD ["python", "OOP_Taximeter/main.py"]





