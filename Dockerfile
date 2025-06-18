# Utiliser une image Python officielle comme base
FROM python:3.11-slim

# Installer curl pour les healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code source de l'application
COPY . .

# Créer le répertoire pour la base de données
RUN mkdir -p /app/data

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Variables d'environnement
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Commande pour initialiser la base de données et démarrer l'application
CMD ["sh", "-c", "python -m alembic upgrade head && python run.py"]
