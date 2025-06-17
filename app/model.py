from . import db 


from enum import Enum



class SexeEnum(Enum):
    HOMME = "HOMME"
    FEMME = "FEMME"

# Association table for Personne <-> Repas (many-to-many)
personne_repas = db.Table('personne_repas',
    db.Column('personne_id', db.Integer, db.ForeignKey('personnes.id'), primary_key=True),
    db.Column('repas_id', db.Integer, db.ForeignKey('repas.id'), primary_key=True)
)

# Association table for Repas <-> Ingredient (many-to-many)
repas_ingredients = db.Table('repas_ingredients',
    db.Column('repas_id', db.Integer, db.ForeignKey('repas.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
)

class Personne(db.Model):
    __tablename__ = 'personnes'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    sexe = db.Column(db.Enum(SexeEnum), nullable=False)

    repas = db.relationship('Repas', secondary=personne_repas, back_populates='personnes')
    reactions = db.relationship('ReactionNegative', back_populates='personne', cascade='all, delete-orphan')

class Repas(db.Model):
    __tablename__ = 'repas'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    origine = db.Column(db.String(100))

    personnes = db.relationship('Personne', secondary=personne_repas, back_populates='repas')
    images = db.relationship('Image', back_populates='repas', cascade='all, delete-orphan')
    ingredients = db.relationship('Ingredient', secondary=repas_ingredients, back_populates='repas')
    reactions = db.relationship('ReactionNegative', back_populates='repas', cascade='all, delete-orphan')

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    chemin = db.Column(db.String(255), nullable=False)

    repas_id = db.Column(db.Integer, db.ForeignKey('repas.id'))
    repas = db.relationship('Repas', back_populates='images')

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)

    repas = db.relationship('Repas', secondary=repas_ingredients, back_populates='ingredients')

class ReactionNegative(db.Model):
    __tablename__ = 'reactions_negatives'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))

    personne_id = db.Column(db.Integer, db.ForeignKey('personnes.id'))
    repas_id = db.Column(db.Integer, db.ForeignKey('repas.id'))

    personne = db.relationship('Personne', back_populates='reactions')
    repas = db.relationship('Repas', back_populates='reactions')
