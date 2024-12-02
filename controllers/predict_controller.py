from flask import jsonify, request
from PIL import Image
import numpy as np
import base64
from models.model_loader import model
from models.Item_user import ItemUser  
from config.database import db
from flask_jwt_extended import decode_token
from io import BytesIO

def preprocessImage(image, targetSize=(224, 224)):
    image = image.resize(targetSize)
    image = np.array(image) / 255.0
    if len(image.shape) == 2:
        image = np.stack((image,) * 3, axis=-1)
    elif image.shape[-1] == 4:
        image = image[..., :3]
    return np.expand_dims(image, axis=0)

def get_user_id_from_token(token):
        payload = decode_token(token)
        print(payload["sub"]["id"])
        return payload["sub"]["id"]

def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")  # Codifica para Base64
    return img_str

def predict_image():
    if not model:
        return jsonify({"error": "Modelo não carregado no servidor"}), 500

    if 'image' not in request.files:
        return jsonify({"error": "Nenhuma imagem enviada"}), 400

    file = request.files['image']
    if not file.content_type.startswith('image/'):
        return jsonify({"error": "Arquivo enviado não é uma imagem válida"}), 400

    try:
        image = Image.open(file)
    except Exception as e:
        return jsonify({"error": f"Erro ao abrir a imagem: {str(e)}"}), 400

    processedImage = preprocessImage(image)

    token = request.headers.get('Authorization')
    if token:
        token = token.split(" ")[1]  
    else:
        return jsonify({"error": "Token não fornecido"}), 401

    id_user = get_user_id_from_token(token)
    if not id_user:
        return jsonify({"error": "Token inválido ou expirado"}), 401

    try:
        prediction = model.predict(processedImage)
        predictionClass = np.argmax(prediction, axis=-1)[0]

        image_base64 = convert_image_to_base64(image)

        new_item = ItemUser(
            label=f"Prediction: {predictionClass}",
            percentage=str(np.max(prediction)),
            image=image_base64,  
            id_user=id_user
        )
        db.session.add(new_item)
        db.session.commit()

    except Exception as e:
        return jsonify({"error": f"Erro ao fazer a predição ou salvar no banco: {str(e)}"}), 500

    return jsonify({
        "prediction": prediction.tolist(),
        "predictedClass": int(predictionClass)
    })
