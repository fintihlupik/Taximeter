FROM python:3.9-slim

# Install xdg-utils
RUN apt-get update && apt-get install -y xdg-utils

WORKDIR /app

COPY . /app

ENV PYTHONIOENCODING=UTF-8

CMD ["python", "OOP_Taximeter/main.py"]





