from flask import Flask, jsonify
from .config import get_config
from .models import db
from .utils.errors import register_error_handlers
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__) # name of the module
    app.config.from_object(get_config())

    # Initialize Extentions
    db.init_app(app)
    JWTManager(app)

    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.ticket_routes import ticket_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(ticket_bp)

    # Error handlers
    register_error_handlers(app)

    # Create tables demo/dev 
    with app.app_context():
        db.create_all()

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200
    
    return app
