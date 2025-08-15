import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///ticketing.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

class DevConfig(Config):
    Debug = True

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-jwt-secret"
    SECRET_KEY = "test-secret"

class ProductionConfig(Config):
    DEBUG = False

def get_config(name=None):
    env = name or os.getenv("FLASK_ENV", "development")
    mapping = {
        "development": DevConfig,
        "testing": TestConfig,
        "production": ProductionConfig
    }
    return mapping.get(env, DevConfig)