from flask import request, jsonify

from services.user_service import UserService
from base.base_blueprint import BaseBlueprint, OK
from utils.auth import auth_required

index_bp = BaseBlueprint('index', __name__)


@index_bp.route('/')
def index():
    return 'Hello, Performa!'


@index_bp.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.parsed_data
    email = data.get('email')
    UserService.send_otp(email)
    return OK


@index_bp.route("/login", methods=["POST"])
def login():
    """ user login """
    data = request.parsed_data
    email, otp = data.get('email'), data.get('otp')
    jwt_token = UserService.validate_otp(email, otp)
    return {"token": jwt_token}


@index_bp.route('/ping', methods=['GET'])
def ping_pong():
    return "pong"


@index_bp.route('/test_auth', methods=['GET'])
@auth_required("STUDENT")
# @auth_required("ADMIN")
def test_auth():
    user = request.auth_user
    print(user)
    return user
