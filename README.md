# VetoMemo

Plateforme de suivi de santé vétérinaire pour animaux de compagnie, articulée autour de deux piliers : une application web de gestion et un module de fouille de données.

Projet de fin d'année, Licence 3 Informatique, Institut d'Enseignement à Distance, Université Paris 8.

## Présentation

VetoMemo permet de tenir un carnet de santé numérique pour ses animaux (visites, vaccinations, traitements, pesées), de générer automatiquement des rappels de soins, de partager l'accès à un animal entre plusieurs utilisateurs selon des rôles distincts, et de recevoir des notifications en temps réel. Un module d'analyse exploite les données produites : détection d'anomalies de poids, projection de tendance, et regroupement des animaux par profils au moyen d'un clustering k-means.

## Pile technique

- Backend : FastAPI (Python)
- Base de données : PostgreSQL
- Cache et diffusion temps réel : Redis (publication/abonnement)
- Frontend : Next.js, TypeScript, Tailwind CSS
- Analyse de données : scikit-learn, pandas, numpy
- Correspondance objet-relationnel et migrations : SQLAlchemy, Alembic
- Orchestration : Docker Compose
- Exploration de données : Jupyter

## Prérequis

- Docker et Docker Compose
- Node.js (version 18 ou superieure) pour le frontend

## Installation et demarrage

### 1. Recuperer le depot

```bash
git clone https://github.com/yousrakdc/vetomemo_V2.git
cd vetomemo_V2
```

### 2. Configuration du backend

Le backend lit sa configuration depuis un fichier `.env` situe a la racine du projet, non versionne pour des raisons de securite. Creer ce fichier a la racine avec le contenu suivant :

```env
POSTGRES_USER=vetomemo
POSTGRES_PASSWORD=devpassword
POSTGRES_DB=vetomemo
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

JWT_SECRET=Xxxxxxx
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Demarrer le backend et les services

Depuis la racine du projet, lancer l'ensemble des services (API, base de donnees, cache et diffusion, et l'environnement d'exploration) par une commande unique :

```bash
docker compose up --build
```

La premiere execution telecharge les images et installe les dependances ; les suivantes sont plus rapides.

Une fois les services demarres :

- l'API est accessible sur http://localhost:8000
- la verification d'etat repond sur http://localhost:8000/health
- la documentation interactive de l'API est sur http://localhost:8000/docs

### 4. Appliquer les migrations de la base de donnees

Le schema de la base est gere par Alembic. Pour creer les tables, appliquer les migrations depuis un second terminal, le backend etant demarre :

```bash
docker compose exec backend alembic upgrade head
```

### 5. Demarrer le frontend

Le frontend se lance separement. Depuis le repertoire `frontend`, installer les dependances puis demarrer le serveur de developpement :

```bash
cd frontend
npm install
npm run dev
```

Le frontend lit l'adresse de l'API depuis un fichier `.env.local` situe dans le repertoire `frontend`. Creer ce fichier avec le contenu suivant :

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

L'application est alors accessible sur http://localhost:3000

## Tests

La suite de tests porte sur la logique metier critique (calcul des echeances de rappel, detection d'anomalies, projection de tendance, affectation de profil). Pour l'executer, le backend etant demarre :

```bash
docker compose exec backend pytest -v
```

Les tests sont egalement executes automatiquement a chaque depot de code, par la chaine d'integration continue definie dans `.github/workflows/tests.yml`.

## Module de fouille de donnees

L'exploration des donnees est realisee dans un notebook Jupyter, accessible via le service du meme nom une fois les conteneurs demarres, sur http://localhost:8888 (jeton d'acces : `vetomemo`).

Le notebook `notebooks/clustering_chats_kmeans.ipynb` contient l'ensemble de la demarche : chargement et preparation des donnees, normalisation, determination du nombre de groupes par la methode du coude et le score de silhouette, application du clustering k-means, et interpretation des profils. Le jeu de donnees utilise se trouve dans `backend/data/cats_dataset.csv`.

## Structure du depot

```
vetomemo_V2/
├── docker-compose.yml
├── .github/workflows/        # integration continue (tests.yml)
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/              # migrations de la base
│   ├── app/
│   │   ├── core/             # configuration, base, securite, dependances, temps reel
│   │   ├── models/           # tables (SQLAlchemy)
│   │   ├── schemas/          # validation (Pydantic)
│   │   ├── routers/          # points d'entree HTTP et WebSocket
│   │   └── services/         # logique metier et acces aux donnees
│   ├── data/                 # jeu de donnees du clustering
│   └── tests/                # tests automatises
├── frontend/
│   ├── app/                  # pages (Next.js App Router)
│   ├── components/           # composants d'interface
│   └── lib/                  # client API, contexte d'auth, types, hooks
└── notebooks/
    └── clustering_chats_kmeans.ipynb
```

## Roles et controle d'acces

L'application distingue trois roles, definis au niveau du foyer : proprietaire (tous les droits, y compris la gestion des membres et la suppression), membre du foyer (lecture et ecriture sur les animaux et leurs donnees), et veterinaire en lecture seule (consultation uniquement).