# API Gestion Réservations de Salles

## 📋 Description

API REST pour gérer les réservations de salles dans un établissement. Cette application implémente un système de gestion avec les fonctionnalités suivantes :

- **Gestion des salles** : CRUD complet (création, lecture, mise à jour, suppression)
- **Gestion des réservations** : Création et consultation avec gestion des conflits
- **Filtrage intelligent** : Recherche par disponibilité des salles
- **Architecture robuste** : Tests d'intégration, migrations de base de données, documentation API

## 🏗️ Architecture

### Stack Technique

- **Framework** : FastAPI 0.104.1
- **Base de données** : SQLite avec SQLAlchemy 2.0.23
- **Migrations** : Alembic 1.13.0
- **Tests** : Pytest 7.4.3
- **Documentation** : Générée automatiquement par FastAPI (Swagger et ReDoc)

### Structure du Projet

```
GVI-TP/
├── app/
│   ├── core/                # Configuration base de données et modèles
│   ├── database/            # Initialisation DB
│   ├── reservations/        # Module de réservations (controller, schema, service)
│   ├── salles/              # Module de salles (controller, schema, service)
│   └── main.py              # Point d'entrée de l'application
├── tests/                   # Tests d'intégration
├── alembic/                 # Migrations de base de données
├── data/                    # Données SQLite
└── run.py                   # Script de démarrage
```

## 🚀 Installation et Démarrage

### Prérequis

- Python 3.9+
- pip ou poetry

### Installation

```bash
# Cloner le repository
git clone <url-du-repo>
cd GVI-TP

# Créer et activer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données (si utilisation d'alembic)
alembic upgrade head
```

### Démarrage Rapide

```bash
# Option 1: Utiliser le script run.py
python run.py

# Option 2: Démarrage manuel
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur http://localhost:8000

### Documentation API

- **Interface Swagger** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 📊 Modèle de Données

### Salle

| Champ        | Type    | Description                 |
| ------------ | ------- | --------------------------- |
| id           | string  | Identifiant unique (UUID)   |
| nom          | string  | Nom de la salle (unique)    |
| capacite     | integer | Nombre maximal de personnes |
| localisation | string  | Description du bâtiment     |
| disponible   | boolean | État de disponibilité       |

### Réservation

| Champ       | Type   | Description                   |
| ----------- | ------ | ----------------------------- |
| id          | string | Identifiant unique (UUID)     |
| salle_id    | string | Référence vers une salle (FK) |
| date        | date   | Date de la réservation        |
| heure       | time   | Heure de début                |
| utilisateur | string | Nom de l'utilisateur          |

## 🔌 API Endpoints

### Salles

- `GET /api/v1/salles` - Liste des salles (avec filtres)
- `POST /api/v1/salles` - Créer une salle
- `GET /api/v1/salles/{id}` - Détails d'une salle
- `PUT /api/v1/salles/{id}` - Modifier une salle
- `DELETE /api/v1/salles/{id}` - Supprimer une salle

### Réservations

- `GET /api/v1/reservations` - Liste des réservations
- `POST /api/v1/reservations` - Créer une réservation
- `GET /api/v1/reservations/{id}` - Détails d'une réservation
- `GET /api/v1/reservations/salle/{salle_id}` - Réservations d'une salle

### Filtres Disponibles

- `GET /api/v1/salles?disponible=true` - Filtrer par disponibilité
- `GET /api/v1/salles?skip=0&limit=10` - Pagination

## 🧪 Tests

```bash
# Exécuter tous les tests
pytest tests/ -v

# Tests spécifiques
pytest tests/test_salles.py -v
pytest tests/test_reservations.py -v
```

### Couverture des Tests

- ✅ Tests d'intégration API pour les salles
- ✅ Tests d'intégration API pour les réservations
- ✅ Tests de validation des contraintes métier (unicité des noms de salles, etc.)
- ✅ Tests de gestion des erreurs

## 🗄️ Base de Données

### Migrations (si utilisation d'alembic)

```bash
# Créer une nouvelle migration
alembic revision --autogenerate -m "Description du changement"

# Appliquer les migrations
alembic upgrade head
```

### Contraintes Métier

- **Unicité** : Pas de doublons de noms de salles
- **Intégrité** : Vérification de l'existence des salles lors des réservations
- **Disponibilité** : Gestion de la disponibilité des salles

## Débogage et Développement

### Logs

```bash
# Logs détaillés
uvicorn app.main:app --log-level debug

# Logs des tests
pytest tests/ -v -s
```

## 📄 Licence

Ce projet est développé dans le cadre du TP GVI - Gestion de Versions et Intégration.
