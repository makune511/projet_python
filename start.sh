#!/bin/bash

echo "Démarrage de l’API Flask…"
python running.py &

# Attendre que l'API soit accessible
echo "Attente que l’API soit prête…"
until curl -s http://localhost:5000/personnes > /dev/null; do
  sleep 1
done

echo "L'API est disponible. Vérification du contenu de la base…"

# Vérifier si la base est vide (aucune personne enregistrée)
NB_PERSONNES=$(curl -s http://localhost:5000/personnes | jq length)

if [ "$NB_PERSONNES" -eq 0 ]; then
  echo "La base est vide. Lancement du script de peuplement…"
  python script.py
else
  echo "La base est déjà peuplée ($NB_PERSONNES personnes). Aucun peuplement nécessaire."
fi

# Garder le processus principal actif (pour Docker)
wait
