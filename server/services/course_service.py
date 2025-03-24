from models import User, UserRole, Enrollment, Term, Program, TermProgramCourse, Course, Grade
from models import UserToken
from utils.common import send_email
from utils.auth import generate_jwt_token, decode_jwt_token
from utils.time import utcnow


class CourseService:

    @staticmethod
    def get_student_enrollment(student_id):
        return (Enrollment.query
                .filter_by(student_id=student_id, status=1)
                .first())

    @staticmethod
    def get_term(term_id):
        return Term.query.filter_by(id=term_id).first()

    @staticmethod
    def get_program(program_id):
        return Program.query.filter_by(id=program_id).first()

    @staticmethod
    def get_term_program_course_list(term_id, program_id):
        return (TermProgramCourse.query
                .filter_by(term_id=term_id, program_id=program_id)
                .all())

    @staticmethod
    def get_course(course_id):
        return Course.query.filter_by(id=course_id).first()

    @staticmethod
    def query_course_list(query=None):
        if query is None:
            query = {}
        ids = query.get('ids')
        if not ids or len(ids) == 0:
            return []
        if isinstance(ids, str):
            # ids = list(map(int, ids.split(',')))
            ids = [int(x.strip()) for x in ids.split(',')]
        elif isinstance(ids, list):
            pass
        else:
            raise TypeError('ids must be a string or a list of ints')

        return Course.query.filter(Course.id.in_(ids)).all()

    @staticmethod
    def query_grades(term_id, program_id, student_id=None, course_id=None):
        filters = {
            "term_id": term_id,
            "program_id": program_id,
        }
        if student_id is not None:
            filters["student_id"] = student_id
        if course_id is not None:
            filters["course_id"] = course_id

        return Grade.query.filter_by(**filters).all()

    # @staticmethod
    # def get_student_enrollment_info(student_id):
    #     enrollment = (Enrollment.query
    #                   .filter_by(student_id=student_id, status=1)
    #                   .first())
    #     term_id = enrollment.term_id
    #     program_id = enrollment.program_id
    #     term = Term.query.filter_by(id=term_id).first()
    #     program = Program.query.filter_by(id=program_id).first()
    #     courses = (TermProgramCourse.query
    #      .filter_by(term_id=term_id, program_id=program_id)
    #      .all())
