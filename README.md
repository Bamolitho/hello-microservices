# **Hello Microservices**

Ce projet contient deux microservices Flask indépendants, **User Service** et **Product Service**, chacun ayant son propre environnement, tests, et pipeline CI/CD.
Un `docker-compose.yml` orchestre leur exécution simultanée.

------

## Structure du projet

```bash
hello-microservices/
├── .github/workflows/           # Pipelines CI/CD
│   ├── ci-user.yml
│   ├── cd-user.yml
│   ├── ci-product.yml
│   ├── cd-product.yml
│   └── deploy.yml
│
├── docker-compose.yml           # Lancement global des microservices
├── Makefile                     # Commandes globales
│
├── user-service/                # Microservice utilisateur
│   ├── app/app.py               # Code Flask (routes /health, /user/<id>)
│   ├── tests/test_user.py       # Tests unitaires Pytest
│   ├── Dockerfile               # Image Docker du service
│   ├── requirements.txt         # Dépendances de production
│   ├── requirements-dev.txt     # Dépendances de développement
│   ├── pytest.ini               # Configuration de tests
│   ├── Makefile                 # Commandes locales (build, test, clean, etc.)
│   ├── ci.yml / cd.yml          # Workflows CI/CD spécifiques
│
└── product-service/             # Microservice produit
    ├── app/app.py               # Code Flask (routes /health, /product/<id>)
    ├── tests/test_product.py    # Tests unitaires Pytest
    ├── Dockerfile               # Image Docker du service
    ├── requirements.txt         # Dépendances de production
    ├── requirements-dev.txt     # Dépendances de développement
    ├── pytest.ini               # Configuration de tests
    ├── Makefile                 # Commandes locales (build, test, clean, etc.)
    ├── ci.yml / cd.yml          # Workflows CI/CD spécifiques
```

------

## Fonctionnement des services

## Fonctionnement

### 🧍‍♂️ User Service

- Fournit des informations utilisateur simulées.
- Routes :
  - `GET /health` → vérifie que le service est en ligne
  - `GET /user/<id>` → retourne un utilisateur fictif

### 📦 Product Service

- Fournit des informations produit simulées.
- Routes :
  - `GET /health` → vérifie que le service est en ligne
  - `GET /product/<id>` → retourne un produit fictif
  - `GET /product/<id>/user` → communique avec le **User Service** pour récupérer le propriétaire du produit

------

## Guide d’utilisation

### 1️⃣ Cloner le projet

```bash
git clone https://github.com/ton-utilisateur/hello-microservices.git
cd hello-microservices
```

## Tester chaque microservice indépendamment

### **User Service**

```bash
cd user-service
pip install -r requirements.txt
python app/app.py
```

Vérifie :

- `http://localhost:5201/health` → `{"status": "ok", "service": "user-service"}`
- `http://localhost:5201/user/1` → `{"id": 1, "name": "Alice", "email": "alice@example.com"}`

Tester avec `pytest` :

```bash
pytest -v
```

------

### **Product Service**

```bash
cd product-service
pip install -r requirements.txt
python app/app.py
```

Vérifie :

- `http://localhost:5202/health` → `{"status": "ok", "service": "product-service"}`
- `http://localhost:5202/product/1` → `{"id": 1, "name": "Laptop", "price": 1200}`

Tester avec `pytest` :

```bash
pytest -v
```

------

## Communication entre les microservices

Tu peux lancer les **deux services localement** dans **deux terminaux séparés**.

### **Terminal 1 : lancer le User Service**

```bash
cd user-service
python app/app.py
```

### **Terminal 2 : lancer le Product Service**

```bash
cd product-service
export USER_SERVICE_URL=http://localhost:5201
python app/app.py
```

Le Product Service peut alors **appeler le User Service** via HTTP :

#### Exemple :

### 🔍 Vérifie les routes :

```shell
curl http://localhost:5202/health
curl http://localhost:5202/product/1
```

------

### 2️⃣ Construire et lancer tous les services

**🐳 Utilisation avec Docker Compose**

Tout peut être lancé d’un coup :

```bash
docker compose up --build -d
```

- `user-service` → [http://localhost:5201](http://localhost:5201/)
- `product-service` → [http://localhost:5202](http://localhost:5202/)

Pour tout arrêter :

```bash
docker-compose down
```

### 3️⃣ Tester un service individuellement

```bash
cd user-service
pytest -v
```

ou

```bash
cd product-service
pytest -v
```

### 🔍 Vérifie les routes :

```shell
curl http://localhost:5202/health
curl http://localhost:5202/product/1
curl http://localhost:5202/product/1/user
```

Résultat attendu pour la dernière :

```json
{
  "owner": {
    "email": "alice@example.com",
    "id": 1,
    "name": "Alice"
  },
  "product": {
    "id": 1,
    "name": "Laptop",
    "owner_id": 1,
    "price": 1200
  }
}
```

### 4️⃣ Lancer les tests pour tous les services (via Makefile global)

```bash
make test-all
```

### 5️⃣ Nettoyer les environnements

```bash
make clean-all
```

------

## CI/CD

Chaque service a :

- Un pipeline **CI** (`ci.yml`) pour les tests unitaires et le linting.
- Un pipeline **CD** (`cd.yml`) pour le déploiement automatique sur Render ou autre plateforme.
- Un fichier `deploy.yml` gère le déploiement global.





**Status badge** : 

[![CI-USER](https://github.com/Bamolitho/hello-microservices/actions/workflows/ci-user.yml/badge.svg)](https://github.com/Bamolitho/hello-microservices/actions/workflows/ci-user.yml)

# RÉFÉRENCES