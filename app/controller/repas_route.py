from flask import Blueprint, request, jsonify
from ..model import db, Repas, Ingredient

repas_bp = Blueprint('repas_bp', __name__)

@repas_bp.route('/repas', methods=['POST'])
def create_repas():
    data = request.get_json()
    repas = Repas(nom=data['nom'], description=data.get('description'), origine=data.get('origine'))
    db.session.add(repas)
    db.session.commit()
    return jsonify({'message': 'Repas ajouté', 'id': repas.id}), 201

@repas_bp.route('/repas', methods=['GET'])
def get_repas():
    repas = Repas.query.all()
    return jsonify([{
        'id': r.id, 'nom': r.nom, 'description': r.description, 'origine': r.origine
    } for r in repas])

@repas_bp.route('/repas/<int:id>', methods=['PUT'])
def update_repas(id):
    repas = Repas.query.get_or_404(id)
    data = request.get_json()
    repas.nom = data.get('nom', repas.nom)
    repas.description = data.get('description', repas.description)
    repas.origine = data.get('origine', repas.origine)
    db.session.commit()
    return jsonify({'message': 'Repas modifié'})

@repas_bp.route('/repas/<int:id>', methods=['DELETE'])
def delete_repas(id):
    repas = Repas.query.get_or_404(id)
    db.session.delete(repas)
    db.session.commit()
    return jsonify({'message': 'Repas supprimé'})

# ROUTE POUR ASSOCIER UN INGRÉDIENT À UN REPAS
@repas_bp.route('/repas/<int:repas_id>/ingredients', methods=['POST'])
def add_ingredient_to_repas(repas_id):
    repas = Repas.query.get_or_404(repas_id)
    data = request.get_json()
    ingredient = Ingredient.query.filter_by(nom=data['nom']).first()
    if not ingredient:
        return jsonify({'message': 'Ingrédient non trouvé'}), 404

    if ingredient not in repas.ingredients:
        repas.ingredients.append(ingredient)
        db.session.commit()

    return jsonify({'message': f"Ingrédient '{ingredient.nom}' ajouté au repas '{repas.nom}'"}), 200
