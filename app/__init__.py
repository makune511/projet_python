# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.controller.image_route import image_bp
    from app.controller.personne_route import personne_bp
    from app.controller.reaction_negatives_route import reaction_bp
    from app.controller.repas_route import repas_bp
    from app.controller.ingredient_route import ingredient_bp

    app.register_blueprint(image_bp)
    app.register_blueprint(personne_bp)
    app.register_blueprint(reaction_bp)
    app.register_blueprint(repas_bp)
    app.register_blueprint(ingredient_bp)

    return app
