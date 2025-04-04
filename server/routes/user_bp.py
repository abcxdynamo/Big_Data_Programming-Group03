from flask import request

from base.base_blueprint import BaseBlueprint, OK
from services import UserService
from utils.model import to_dict_list
from utils.auth import auth_required

user_bp = BaseBlueprint('users', __name__)


@user_bp.route('/info/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    return UserService.get_user_by_id(user_id).dict()


@user_bp.route('/list', methods=['POST'])
def query_user_list():
    return to_dict_list(UserService.query_user_list(request.parsed_data))


@user_bp.route('/<int:student_id>', methods=['GET'])
# @auth_required()
def get_student(student_id):
    print(f"get_student: {student_id}")
    return OK


@user_bp.route('toggle_active/<int:user_id>', methods=['POST'])
@auth_required("ADMIN")
def toggle_active(user_id):
    UserService.toggle_active(user_id)
    return OK
