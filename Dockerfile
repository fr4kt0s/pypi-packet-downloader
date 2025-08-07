FROM python:3.10-slim

# Systemabhängigkeiten für bandersnatch
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis setzen
WORKDIR /app

# Projektdateien kopieren
COPY . /app

# Abhängigkeiten installieren
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Port öffnen (Flask default)
EXPOSE 5000

# Startbefehl
CMD ["python3", "main.py"]