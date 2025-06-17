from flask import Blueprint, request, jsonify
from ..model import db, Personne, SexeEnum

personne_bp = Blueprint('personne_bp', __name__)

@personne_bp.route('/personnes', methods=['POST'])
def create_personne():
    data = request.get_json()
    personne = Personne(
        nom=data['nom'],
        prenom=data['prenom'],
        age=data['age'],
        email=data['email'],
        sexe=SexeEnum[data['sexe'].upper()]
    )
    db.session.add(personne)
    db.session.commit()
    return jsonify({'message': 'Personne ajoutée', 'id': personne.id}), 201

@personne_bp.route('/personnes', methods=['GET'])
def get_personnes():
    personnes = Personne.query.all()
    return jsonify([{
        'id': p.id, 'nom': p.nom, 'prenom': p.prenom, 'age': p.age,
        'email': p.email, 'sexe': p.sexe.value
    } for p in personnes])


@personne_bp.route('/personnes/<int:person_id>', methods=['GET'])
def get_personne(person_id):
    #p = Personne.query.filter_by(id = person_id).first()
    p = Personne.query.get_or_404(person_id)
    return jsonify({
        'id': p.id, 'nom': p.nom, 'prenom': p.prenom, 'age': p.age,
        'email': p.email, 'sexe': p.sexe.value
    } )



@personne_bp.route('/personnes/<int:id>', methods=['PUT'])
def update_personne(id):
    personne = Personne.query.get_or_404(id)
    data = request.get_json()
    personne.nom = data.get('nom', personne.nom)
    personne.prenom = data.get('prenom', personne.prenom)
    personne.age = data.get('age', personne.age)
    personne.email = data.get('email', personne.email)
    if 'sexe' in data:
        personne.sexe = SexeEnum[data['sexe'].upper()]
    db.session.commit()
    return jsonify({'message': 'Personne modifiée'})

@personne_bp.route('/personnes/<int:id>', methods=['DELETE'])
def delete_personne(id):
    personne = Personne.query.get_or_404(id)
    db.session.delete(personne)
    db.session.commit()
    return jsonify({'message': 'Personne supprimée'})
