import logging
from tensorflow.keras.models import load_model
from keras_cv.losses import FocalLoss

model = None

try:
    model = load_model("model1_finetunning2.keras", custom_objects={"FocalLoss": FocalLoss})
    logging.info("Modelo carregado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao carregar o modelo: {e}")
