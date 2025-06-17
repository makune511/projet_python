# projet_python
projet de suivi de l'alimentation de la population gabonaise réalisé en python 
# 🥗 API Flask - Suivi de l'Alimentation

Ce projet est une API web backend développée avec **Flask** permettant de gérer des personnes, leurs repas, les ingrédients associés, les images des repas, ainsi que les réactions négatives aux repas afin de détecter d'éventuelles allergies.

## 📦 Fonctionnalités principales

- CRUD pour les entités suivantes :
  - Personnes
  - Repas
  - Ingrédients
  - Images
  - Réactions négatives
- Association de plusieurs ingrédients à un repas
- Association de plusieurs images à un repas
- Suivi des repas consommés par une personne
- Système de détection d’allergie basé sur les réactions enregistrées
- Récupération des réactions d’une seule personne

## 🛠️ Technologies utilisées

- Python 3.10
- Flask
- SQLAlchemy
- Flask-Migrate
- PostgreSQL
- Docker
- Postman (pour les tests)
- Visual Studio Code

## 🗂️ Structure générale du projet

```
appli/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── model/
│   ├── controller/
│   └── static/images/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── running.py
└── README.md
```

## 🚀 Lancement de l'application

## Cloner le dépôt

git clone https://github.com/makune511/projet_python.git
cd projet_python

## Construire et lancer avec Docker Compose

Pour construire les images et démarrer les conteneurs (base de données + API Flask) :

docker compose up --build


## Gérer les conflits de ports

Si tu as une erreur comme :

failed to bind port 0.0.0.0:5000/tcp: bind: address already in use

Cela signifie que le port 5000 est déjà utilisé sur ta machine (par exemple par un processus Python local).

Pour voir quel processus utilise ce port :

sudo lsof -i :5000

Pour stopper ce processus (remplace <PID> par le numéro de processus) :

kill -9 <PID>

Puis relancer :

docker compose up --build


###  Tester avec Postman

Utilisez Postman pour tester les routes suivantes :
- `POST /personnes/`, `GET /personnes/`, etc.
- `POST /repas/`, `GET /repas/`
- `POST /reactions/`, `GET /reactions/personne/<id>`
- `GET /personnes/<id>/allergies`

## ✍️ Auteur

- Makune Kougoum Bijoël – Licence 2 Informatique – Université de Yaoundé 1

## 📄 Licence

Ce projet est à usage académique et personnel.
