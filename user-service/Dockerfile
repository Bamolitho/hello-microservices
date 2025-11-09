# ==============================
# Dockerfile - user-service
# ==============================
FROM python:3.10-slim

WORKDIR /app

# Installer les dépendances principales
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app/ app/

# Exposer le port Flask
EXPOSE 5201

# Commande de démarrage
ENTRYPOINT [ "python" ]
CMD ["app/app.py"]
