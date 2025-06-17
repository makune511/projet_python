from flask import Blueprint, request, jsonify
from ..model import db, Image, Repas

image_bp = Blueprint('image_bp', __name__)

@image_bp.route('/images', methods=['POST'])
def create_image():
    data = request.get_json()
    image = Image(chemin=data['chemin'], repas_id=data['repas_id'])
    db.session.add(image)
    db.session.commit()
    return jsonify({'message': 'Image ajoutée', 'id': image.id}), 201

@image_bp.route('/images', methods=['GET'])
def get_images():
    images = Image.query.all()
    return jsonify([{
        'id': i.id, 'chemin': i.chemin, 'repas_id': i.repas_id
    } for i in images])

# ROUTE POUR AJOUTER UNE IMAGE À UN REPAS
@image_bp.route('/repas/<int:repas_id>/images', methods=['POST'])
def add_image_to_repas(repas_id):
    repas = Repas.query.get_or_404(repas_id)
    data = request.get_json()
    image = Image(chemin=data['chemin'], repas_id=repas.id)
    db.session.add(image)
    db.session.commit()
    return jsonify({'message': f"Image ajoutée au repas '{repas.nom}'", 'id': image.id}), 201
