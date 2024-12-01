from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from flask_cors import CORS
from keras_cv.losses import FocalLoss
from PIL import Image
import numpy as np
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

try:
    model = load_model("model1_finetunning2.keras", custom_objects={"FocalLoss": FocalLoss})
    logging.info("Modelo carregado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao carregar o modelo: {e}")
    model = None

def preprocessImage(image, targetSize=(224, 224)):
    image = image.resize(targetSize) 
    image = np.array(image) / 255.0   
    if len(image.shape) == 2:         
        image = np.stack((image,) * 3, axis=-1)
    elif image.shape[-1] == 4:       
        image = image[..., :3]
    return np.expand_dims(image, axis=0)

@app.route('/predict', methods=['POST'])
def predict():
    
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

    try:
        prediction = model.predict(processedImage)
        predictionClass = np.argmax(prediction, axis=-1)[0]  
    except Exception as e:
        return jsonify({"error": f"Erro ao fazer a predição: {str(e)}"}), 500

    return jsonify({
        "prediction": prediction.tolist(),  
        "predictedClass": int(predictionClass)  
    })

@app.route('/teste', methods=['GET'])
def teste():
    return jsonify({"message": "oi"})

@app.errorhandler(404)
def pageNotFound(e):
    return jsonify({"error": "Rota não encontrada"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333, debug=True)
