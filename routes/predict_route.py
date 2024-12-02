from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.predict_controller import predict_image

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
@jwt_required()  
def predict():
    return predict_image()

@predict_bp.route('/teste', methods=['GET'])
@jwt_required() 
def teste():
    return {"message": "oi"}
