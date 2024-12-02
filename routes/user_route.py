from flask import Blueprint
from controllers.user_controller import register, login, decode_user_token, get_user_images

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/register', methods=['POST'])(register)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/decode-token', methods=['GET'])(decode_user_token)
auth_bp.route('/get-image-token', methods=['GET'])(get_user_images)
