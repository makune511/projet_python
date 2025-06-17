from flask import Blueprint, request, jsonify
from ..model import db, ReactionNegative, Repas

reaction_bp = Blueprint('reaction_bp', __name__)

@reaction_bp.route('/reactions', methods=['POST'])
def create_reaction():
    data = request.get_json()
    reaction = ReactionNegative(
        description=data.get('description'),
        personne_id=data['personne_id'],
        repas_id=data['repas_id']
    )
    db.session.add(reaction)
    db.session.commit()
    return jsonify({'message': 'Réaction enregistrée', 'id': reaction.id}), 201

@reaction_bp.route('/reactions', methods=['GET'])
def get_reactions():
    reactions = ReactionNegative.query.all()
    return jsonify([{
        'id': r.id, 'description': r.description,
        'personne_id': r.personne_id, 'repas_id': r.repas_id
    } for r in reactions])

@reaction_bp.route('/reactions/personne/<int:personne_id>', methods=['GET'])
def get_reactions_by_person(personne_id):
    reactions = ReactionNegative.query.filter_by(personne_id=personne_id).all()
    result = []
    for r in reactions:
        result.append({
            'id': r.id,
            'description': r.description,
            'repas_id': r.repas_id
        })
    return jsonify(result)

@reaction_bp.route('/personne/<int:personne_id>/allergies', methods=['GET'])
def detect_allergies(personne_id):
    # 1. Récupère les repas avec réactions négatives de la personne
    reactions = ReactionNegative.query.filter_by(personne_id=personne_id).all()
    repas_ids = [r.repas_id for r in reactions]

    if len(repas_ids) == 0:
        return jsonify({'message': 'Aucune réaction enregistrée pour cette personne', 'allergies': []})

    # 2. Compte la fréquence de chaque ingrédient dans ces repas
    ingredient_freq = {}

    for repas_id in repas_ids:
        repas = Repas.query.get(repas_id)
        if repas:
            for ingr in repas.ingredients:
                if ingr.nom in ingredient_freq:
                    ingredient_freq[ingr.nom] += 1
                else:
                    ingredient_freq[ingr.nom] = 1

    # 3. Garde les ingrédients apparaissant dans au moins 2 repas
    suspects = [nom for nom, count in ingredient_freq.items() if count >= 2]

    return jsonify({
        'personne_id': personne_id,
        'allergies_suspectées': suspects,
        'message': "Les ingrédients listés apparaissent dans au moins 2 repas avec réactions négatives."
    })

