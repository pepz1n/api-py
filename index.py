from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.settings import Config
from config.database import db
from routes.user_route import auth_bp
from routes.predict_route import predict_bp
import logging

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)  
    CORS(app)  

    logging.basicConfig(level=logging.INFO)

    db.init_app(app)
    
    JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(predict_bp, url_prefix='/predict')

    @app.errorhandler(404)
    def page_not_found(e):
        return {"error": "Rota não encontrada"}, 404

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  
    app.run(host='0.0.0.0', port=3333, debug=True)
