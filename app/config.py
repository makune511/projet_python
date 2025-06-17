import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "postgresql://postgres:9069765@localhost/alimentation"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
