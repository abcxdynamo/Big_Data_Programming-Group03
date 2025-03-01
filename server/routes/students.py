from flask import request, jsonify

from services.user_service import UserService
from base.base_blueprint import BaseBlueprint, OK
from utils.auth import auth_required

students_bp = BaseBlueprint('students', __name__)


@students_bp.route('/list', methods=['GET'])
def get_students():
    print("get_students")
    return OK

@students_bp.route('/<int:student_id>', methods=['GET'])
# @auth_required()
def get_student(student_id):
    print(f"get_student: {student_id}")
    return OK

