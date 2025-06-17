from flask import Blueprint, request, jsonify
from ..model import db, Ingredient

ingredient_bp = Blueprint('ingredient_bp', __name__)

@ingredient_bp.route('/ingredients', methods=['POST'])
def create_ingredient():
    data = request.get_json()
    ingr = Ingredient(nom=data['nom'])
    db.session.add(ingr)
    db.session.commit()
    return jsonify({'message': 'Ingrédient ajouté', 'id': ingr.id}), 201

@ingredient_bp.route('/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    return jsonify([{'id': i.id, 'nom': i.nom} for i in ingredients])
