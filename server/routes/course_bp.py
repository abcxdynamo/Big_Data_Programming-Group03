from flask import request, jsonify

from services.course_service import CourseService
from base.base_blueprint import BaseBlueprint, OK
from utils.auth import auth_required
from utils.model import to_dict_list

course_bp = BaseBlueprint('courses', __name__)


@course_bp.route('/enrollment/<int:student_id>', methods=['GET'])
def get_student_enrollment(student_id):
    return CourseService.get_student_enrollment(student_id).dict(include_relationships=True)


@course_bp.route('/terms/<int:term_id>', methods=['GET'])
def get_term_info(term_id):
    return CourseService.get_term(term_id).dict()


@course_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_info(course_id):
    return CourseService.get_course(course_id).dict()


@course_bp.route('/courses/list', methods=['POST'])
def query_course_list():
    return to_dict_list(CourseService.query_course_list(request.parsed_data))


@course_bp.route('/programs/<int:program_id>', methods=['GET'])
def get_program_info(program_id):
    return CourseService.get_program(program_id).dict()


@course_bp.route('/term_program_courses/<int:term_id>/<int:program_id>', methods=['GET'])
def get_term_program_course_list(term_id, program_id):
    return to_dict_list(CourseService.get_term_program_course_list(term_id, program_id))


@course_bp.route('/grades/<int:term_id>/<int:program_id>', methods=['GET'])
def query_grades(term_id, program_id):
    return CourseService.query_grades(term_id,
                                      program_id,
                                      request.args.get('student_id'),
                                      request.args.get('course_id'))


@course_bp.route('/instructor/courses/<int:instructor_id>', methods=['GET'])
def get_instructor_courses(instructor_id):
    return CourseService.query_instructor_courses({"instructor_id": instructor_id})


@course_bp.route('/instructor/courses', methods=['GET'])
def query_instructor_courses():
    return CourseService.query_instructor_courses(request.args.to_dict())


@course_bp.route('/instructor/student_grades/<int:instructor_id>', methods=['GET'])
def get_instructor_student_grades():
    return CourseService.query_student_grades({"instructor_id": request.args.get('instructor_id')})


@course_bp.route('/grades/list', methods=['GET'])
def query_student_grades():
    return CourseService.query_student_grades(request.args.to_dict())


@course_bp.route('/grades/<int:grade_id>/feedback', methods=['POST'])
def save_grade_feedback(grade_id):
    data = request.parsed_data
    feedback = data.get('feedback')
    CourseService.save_grade_feedback(grade_id, feedback)
    return OK
