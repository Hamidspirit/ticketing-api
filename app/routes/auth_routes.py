from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models import db, User
from ..utils.validators import require_json_keys, validate_username, validate_password
from ..utils.errors import ConflictError, UnauthorizedError

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    require_json_keys(data=data, keys=["username", "password"])

    username = data.get("username", "").strip()
    password = data.get("password", "")

    validate_username(username)
    validate_password(password)

    if User.query.filter_by(username=username).first():
        raise ConflictError("Username already exists")
    
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User Registered", "user": user.to_dict()}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    require_json_keys(data, ["username", "password"])
    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        raise UnauthorizedError("Invalid Username or pasword")
    
    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token, "user": user.to_dict()}), 200