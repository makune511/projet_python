import json
import os
import requests

BASE_URL = "http://localhost:5000"
DATA_FILE = "peuplement.json"

ingredient_posted = set()
repas_posted = set()
image_posted = set()
personne_emails = set()

def api_get(endpoint):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erreur GET {endpoint} : {e}")
    return []

def post_personnes(personnes):
    existants = {p["email"] for p in api_get("/personnes")}
    for p in personnes:
        if p["email"] in existants:
            print(f"Personne déjà existante : {p['email']}")
            continue
        response = requests.post(f"{BASE_URL}/personnes", json=p)
        if response.status_code == 201:
            data = response.json()
            print(f"Personne ajoutée : {p['prenom']} {p['nom']} (ID={data.get('id')})")
        else:
            print(f"Erreur ajout {p['prenom']} {p['nom']} : {response.text}")

def post_ingredient(nom):
    nom_normalise = nom.strip().lower()
    if nom_normalise in ingredient_posted:
        return
    response = requests.post(f"{BASE_URL}/ingredients", json={"nom": nom})
    if response.status_code == 201:
        print(f"Ingrédient ajouté : {nom}")
    else:
        print(f"Ingrédient {nom} déjà existant ou erreur : {response.text}")
    ingredient_posted.add(nom_normalise)

def associate_ingredient_to_repas(repas_id, ingredient_nom):
    url = f"{BASE_URL}/repas/{repas_id}/ingredients"
    response = requests.post(url, json={"nom": ingredient_nom})
    if response.status_code in (200, 201):
        print(f"   ↳ Ingrédient associé : {ingredient_nom}")
    else:
        print(f"  Erreur association ingrédient : {response.text}")

def post_images(repas_id, repas_nom, images):
    for img in images:
        chemin = os.path.join("static", "images", "gabon", repas_nom, img)
        if chemin in image_posted:
            continue
        response = requests.post(f"{BASE_URL}/repas/{repas_id}/images", json={"chemin": chemin})
        if response.status_code in (200, 201):
            print(f"   ↳ Image ajoutée : {chemin}")
        else:
            print(f"   Erreur image : {response.text}")
        image_posted.add(chemin)

def post_reaction(repas_id, reaction):
    payload = {
        "personne_id": reaction["personne_id"],
        "repas_id": repas_id,
        "description": reaction["description"]
    }
    response = requests.post(f"{BASE_URL}/reactions", json=payload)
    if response.status_code in (200, 201):
        print(f"   ↳ Réaction ajoutée pour personne {reaction['personne_id']}")
    else:
        print(f"  Erreur réaction : {response.text}")

def post_repas(repas_list):
    existants = {r["nom"] for r in api_get("/repas")}
    for r in repas_list:
        if r["nom"] in existants:
            print(f"Repas déjà existant : {r['nom']}")
            continue
        payload = {
            "nom": r["nom"],
            "description": r.get("description"),
            "origine": r.get("origine")
        }
        response = requests.post(f"{BASE_URL}/repas", json=payload)
        if response.status_code == 201:
            data = response.json()
            repas_id = data.get("id")
            print(f" Repas ajouté : {r['nom']} (ID={repas_id})")

            for ing in r.get("ingredients", []):
                post_ingredient(ing)
                associate_ingredient_to_repas(repas_id, ing)

            post_images(repas_id, r["nom"], r.get("images", []))

            if "reactions" in r:
                for reaction in r["reactions"]:
                    post_reaction(repas_id, reaction)
        else:
            print(f" Erreur ajout repas {r['nom']} : {response.text}")

def main():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Erreur chargement {DATA_FILE} : {e}")
        return

    print("Insertion des personnes...")
    post_personnes(data.get("personnes", []))

    print("\n Insertion des repas et des éléments associés...")
    post_repas(data.get("repas", []))

if __name__ == "__main__":
    main()
