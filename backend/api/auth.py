from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token
from datetime import datetime
from schemas.auth import RegisterSchema
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = RegisterSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify(msg='Email already registered'), 400

    user = User(
        email=data['email'],
        full_name=data['full_name'],
        qualification=data.get('qualification'),
        dob=data.get('dob')
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(msg='User registered'), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    if not data.get('email') or not data.get('password'):
        return jsonify(msg='Email and password required'), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify(msg='Bad credentials'), 401
    token = create_access_token(identity=str(user.id),
                                additional_claims={'role': user.role})
    return jsonify(access_token=token), 200
