from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, decode_token
from models.User import User
from models.Item_user import ItemUser  
from config.database import db

def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not (name and email and password):
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Usuário já cadastrado"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso"}), 201


def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = create_access_token(identity={"id": user.id, "name": user.name})
    return jsonify({"token": token}), 200


def decode_user_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token não fornecido"}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded_token = decode_token(token)
        user_name = decoded_token["sub"]["name"]
        return jsonify({"user_name": user_name}), 200
    except Exception as e:
        return jsonify({"error": f"Token inválido: {str(e)}"}), 401


def get_user_images():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token não fornecido"}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded_token = decode_token(token)
        user_id = decoded_token["sub"]["id"]

        items = ItemUser.query.filter_by(id_user=user_id).order_by(ItemUser.id.desc()).all()
        print(items)
        images = [
            {
                "label": item.label,
                "percentage": item.percentage,
                "image": item.image  
            }
            for item in items
        ]

        return jsonify({"images": images}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao processar o token ou recuperar as imagens: {str(e)}"}), 401
